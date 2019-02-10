# ========================================================================================
# 
#  Description:
# 
#     Compiles Hack ASM (assembly) code to Hack BIN (binary) code
#     Does not use the TECS specification
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================

'''
	--- Notes ---

	> Instruction (16)

		15    -> has32BitImmediate
		14    -> has16BitImmediate
		13..8 -> fxSel
		7..4  -> xSel
		3..0  -> ySel

'''

# TODO - test all op variants (are they all encoded correctly)


# == Imports =================================================

# Built ins
import re
import os

# Hack computer
import Components._0__globalConstants as GC
from commonHelpers import *



# == Helpers =================================================

def newDictFromKeys( baseDict, keys ):

	# stackoverflow.com/q/12117080
	return { k : baseDict[ k ] for k in keys }


def raiseError( line ):

	raise Exception( 'Invalid command - {}'.format( line ) )



# == Lookup Tables ===========================================

LT = {

	'registers' : {

		'R0'       : 0,
		'R1'       : 1,
		'R2'       : 2,
		'R3'       : 3,
		'R4'       : 4,
		'R5'       : 5,
		'R6'       : 6,
		'R7'       : 7,
		'R8'       : 8,
		'R9'       : 9,
		'R10'      : 10,
		'R11'      : 11,
		'R12'      : 12,
		'R13'      : 13,
		'R14'      : 14,
		'R15'      : 15,

		'RSTATUS'  : 15,
	},

	'registerPairs' : {

		# register pairs
		'R2R1'     : 0,
		'R4R3'     : 1,
		'R6R5'     : 2,
		'R8R7'     : 3,
		'R10R9'    : 4,
		'R12R11'   : 5,
		'R14R13'   : 6,
	},

	'dataMemoryAddresses' : {

		# VM structure
		# '@SP'       : '@0',
		# '@LCL'      : '@1',
		# '@ARG'      : '@2',
		# '@THIS'     : '@3',
		# '@THAT'     : '@4',
		# '@TEMP0'    : '@5',
		# '@TEMP1'    : '@6',
		# '@TEMP2'    : '@7',
		# '@TEMP3'    : '@8',
		# '@TEMP4'    : '@9',
		# '@TEMP5'    : '@10',
		# '@TEMP6'    : '@11',
		# '@TEMP7'    : '@12',
		# '@GP0'      : '@13',
		# '@GP1'      : '@14',
		# '@GP2'      : '@15',

		# IO
		'SCREEN'   : GC.SCREEN_MEMORY_MAP,
		'KEYBOARD' : GC.KEYBOARD_MEMORY_MAP,
		'MOUSE'    : GC.MOUSE_MEMORY_MAP,
	},

	# directives such as EQU not part of program count
	# 'dataMemoryAddresses' : [

	# 	'SCREEN   EQU {}'.format( GC.SCREEN_MEMORY_MAP ),
	# 	'KEYBOARD EQU {}'.format( GC.KEYBOARD_MEMORY_MAP ),
	# 	'MOUSE    EQU {}'.format( GC.MOUSE_MEMORY_MAP ),
	# ],

	'op' : {

		'STO'  : 0,
		'LD'   : 1,
		'LPM'  : 2,
		'MOV'  : 3,
		'ADD'  : 4,
		'SUB'  : 5,
		'AND'  : 6,
		'OR'   : 7,
		'XOR'  : 8,
		'LSR'  : 9,
		'LSL'  : 10,
		'MUL'  : 11,
		'DIV'  : 12,
		'NOT'  : 13,
		'NEG'  : 14,
		'CMP'  : 15,
		'JMP'  : 16,
		'JZ'   : 17,
		'JNZ'  : 18,
		'JC'   : 19,
		'JNC'  : 20,
		'JNG'  : 21,
		'JZP'  : 22,
		'JSR'  : 23,
		'RTS'  : 24,
		'LXH'  : 25,
		'SWI'  : 26,
		'RTI'  : 27,
		'IORD' : 28,
		'IOWR' : 29,
		'IODR' : 30,
		'HLT'  : 31,
		'NOP'  : 32,
	},

	'opJump'       : None,
	'opStandalone' : None
}

# Convert to binary string
for k, v in LT[ 'registers' ].items():

	LT[ 'registers' ][ k ] = toBinary( v, 4 )

for k, v in LT[ 'registerPairs' ].items():

	LT[ 'registerPairs' ][ k ] = toBinary( v, 4 )

for k, v in LT[ 'op' ].items():

	LT[ 'op' ][ k ] = toBinary( v, 6 )

# Create subsets
LT[ 'opJump' ] = newDictFromKeys( LT[ 'op' ],

	[
		'JMP',
		'JZ',
		'JNZ',
		'JC',
		'JNC',
		'JNG',
		'JZP',
		'JSR',
	]
)
LT[ 'opStandalone' ] = newDictFromKeys( LT[ 'op' ],

	[
		'RTS',
		'HLT',
		'NOP',
	]
)
LT[ 'opExtMemoryAccess' ] = [

	'STO',
	'LD',
	'LPM',
]

# Data definitions
dataDefinitions = {

	# 'DBYTE'   : 0,  # half a word
	'DWORD'   : 1,  # 1 word
	'DDOUBLE' : 2,  # 2 words
	'DQUAD'   : 4   # 4 words
}



# == Debug ===================================================

def getKeyByValue( value, d ):

	# stackoverflow.com/a/8023337

	for k, v in d.items():

		if v == value:

			return k

	return None


def getHex4( value ):

	return hex( int( value, 2 ) )[ 2 : ].zfill( 4 )


def printFinalAssembly( asmCmdList, binCmdList ):

	showBinary = False

	def getBinaryString():  # DRY

		s = ''

		if showBinary:

			s = '{:<4}  {:<16}  |    '.format(

				getHex4( binCmdList[ bIdx ] ),
				binCmdList[ bIdx ]
			)

		return s

	bIdx = 0

	for cmd in asmCmdList:

		label = getKeyByValue( bIdx, knownAddresses_ProgramMemory )

		op = cmd[ 'op' ]

		rX        = cmd.get( 'rX' )
		rY        = cmd.get( 'rY' )
		rPair     = cmd.get( 'rPair' )
		immediate = cmd.get( 'immediate' )
		address   = cmd.get( 'address' )

		'''
			op
			op {addr}
			op rPair
			op rX rY
			op rX {addr}
			op rX rPair
			op rX rY imm
		'''
		s_label = '( ' + label + ' )' if label else ''
		s_op    = op
		s_rX    = rX if rX else rPair if rPair else ''
		s_rY    = rY if rY else rPair if ( rX and rPair ) else ''

		if s_label : s_label += ' '
		if s_op    : s_op    += ' '
		if s_rX    : s_rX    += ' '
		if s_rY    : s_rY    += ' '

		print( '{}{:<6} -   {}{}{}{}'.format(

			getBinaryString(),
			bIdx,
			s_label,
			s_op,
			s_rX,
			s_rY

		) )

		if immediate or address:

			bIdx += 1

			wLo = int( binCmdList[ bIdx ], 2 )

			print( '{}{:<6} -   {}'.format(

				getBinaryString(),
				bIdx,
				wLo
			) )

		if address:

			bIdx += 1

			wHi = int( binCmdList[ bIdx ], 2 )

			# program address
			if ( op in LT[ 'opJump' ] ) or ( op == 'LXH' ):

				label = getKeyByValue( ( wHi << 16 ) | wLo, knownAddresses_ProgramMemory )

				if not label: label = '???'

			# data address
			elif op in LT[ 'opExtMemoryAccess' ]:

				label = getKeyByValue( ( wHi << 16 ) | wLo, knownAddresses_DataMemory )

			s_label = '   // {}'.format( label ) if label else ''

			print( '{}{:<6} -   {}{}'.format(

				getBinaryString(),
				bIdx, 
				wHi,
				s_label
			) )

		# update
		bIdx += 1
	

def debugStuff( asmCmdList, binCmdList ):

	print( '\n--\n' )

	# Print final assembly
	printFinalAssembly( asmCmdList, binCmdList )

	print( '\n--\n' )

	# Print labels
	for kv in sorted(

		knownAddresses_ProgramMemory.items(),
		key = lambda x : x[ 1 ]
	):		
		print( '{:<6}  {}'.format( kv[ 1 ], kv[ 0 ] ) )

	print( '\n--\n' )

	# Print variables
	for kv in sorted(

		knownAddresses_DataMemory.items(),
		key = lambda x : x[ 1 ]
	):
		print( '{:<6}  {}'.format( kv[ 1 ], kv[ 0 ] ) )

	print( '\n--\n' )



# == Main ====================================================


# -- ... -------------------------------------------

# nBits = GC.N_BITS
nBits = 16

static_segment_start = GC.STATIC_START
static_segment_end   = GC.STATIC_END
static_segment_size  = static_segment_end - static_segment_start + 1

largest_immediate = 2 ** nBits - 1
largest_address   = 2 ** 32 - 1

knownAliases = {}
knownAddresses_ProgramMemory = {}
knownAddresses_DataMemory = {}
knownAddresses_DataMemory.update( LT[ 'dataMemoryAddresses' ] )  # fill with global addresses




# -- ... --------------------------------------------

cmdPattern = '''
	//    |       # start of comment
	\'    |       # char wrappers
	\(|\) |       # label wrappers
	\[|\] |       # address wrappers
	\w+           # word or digit sequence
'''
cmdPattern = re.compile( cmdPattern, re.X )


def readInputFile( inputFile ):

	cmdList = []

	with open( inputFile, 'r' ) as file:

		for line in file:

			# Extract words from command
			cmd = re.findall( cmdPattern, line )

			# Ignore comment
			if '//' in cmd:

				cmd = cmd[ 0 : cmd.index( '//' ) ]

			# If not blank line or comment, add to list
			if cmd:

				cmdList.append( [ cmd, line.rstrip() ] )

	return cmdList



# -- Expand -----------------------------------------

def expandMACRO( cmdList ):

	expandedCmdList = []

	macros       = {}
	macroDefName = ''
	isMacroDef   = False

	for cmdEl in cmdList:

		cmdRaw = cmdEl[ 0 ]
		line   = cmdEl[ 1 ]

		op = cmdRaw[ 0 ].upper()

		# Start of macro defenition
		if op == 'MACRO':

			# No support for nested
			if isMacroDef:

				raise Exception( 'Nested MACRO definitions are currently unsupported\n->  {}'.format( line ) )

			# Check for parentheses
			if ( cmdRaw[ 2 ] != '(' ) or ( cmdRaw[ - 1 ] != ')' ):

				raiseError( line )

			#
			macroDefName = cmdRaw[ 1 ]
			parameters   = cmdRaw[ 3 : - 1 ]  # everything in between parentheses

			macros[ macroDefName ] = {

				'parameters' : parameters,
				'statements' : []
			}

			#
			isMacroDef = True

			continue


		# Rest of macro definition
		elif isMacroDef:

			# End of macro definition
			if op == 'ENDMACRO':

				# Check for length
				if len( cmdRaw ) != 1:

					raiseError( line )

				#
				isMacroDef = False
				macroDefName = ''


			# Collect macro body
			else:

				macros[ macroDefName ][ 'statements' ].append( cmdEl )

			continue


		# Call of macro
		elif cmdRaw[ 0 ] in macros:  # preserve case

			name = cmdRaw[ 0 ]

			# Check for parentheses
			if ( cmdRaw[ 1 ] != '(' ) or ( cmdRaw[ - 1 ] != ')' ):

				raiseError( line )

			# Get arguments
			parameters = macros[ name ][ 'parameters' ]

			arguments = cmdRaw[ 2 : - 1 ]  # everything in between parentheses

			if len( arguments ) != len( parameters ):

				raise Exception(

					'Invalid number of arguments, expected {} but got {}\n->  {}'.format(

						len( parameters ),
						len( arguments ),
						line
					)
				)

			argLookup = {}

			for i in range( len( parameters ) ):

				argLookup[ parameters[ i ] ] = arguments[ i ]

			# Add commands to list
			for statement in macros[ name ][ 'statements' ]:

				_cmdRaw = statement[ 0 ]
				_line   = statement[ 1 ]

				_cmdRaw2 = []

				# replace
				for w in _cmdRaw:

					if w in parameters:

						_cmdRaw2.append( argLookup[ w ] )

					else:

						_cmdRaw2.append( w )

				# add
				_cmdEl = [ _cmdRaw2, _line ]
				expandedCmdList.append( _cmdEl )

			#
			continue

		# Not a macro definition or call
		else:

			expandedCmdList.append( cmdEl )


	# Reached end without finding 'ENDMACRO'
	if isMacroDef:

		raise Exception( "Expected an 'ENDMACRO' statement" );


	return expandedCmdList


def handleEQU( cmdList ):

	global knownAliases

	trimmedCmdList = []

	for cmdEl in cmdList:

		cmdRaw = cmdEl[ 0 ]
		line   = cmdEl[ 1 ]

		op = cmdRaw[ 0 ].upper()

		# EQU definition
		if op == 'EQU':

			# Check for length
			if len( cmdRaw ) != 3:

				raiseError( line )

			#
			alias = cmdRaw[ 1 ]
			value = cmdRaw[ 2 ]

			knownAliases[ alias ] = value

			continue

		#
		else:

			# Replace aliases
			_cmdRaw = []

			for w in cmdRaw:

				if w in knownAliases:

					_cmdRaw.append( knownAliases[ w ] )

				else:

					_cmdRaw.append( w )

			# Add to list
			_cmdEl = [ _cmdRaw, line ]

			trimmedCmdList.append( _cmdEl )

	# Done
	return trimmedCmdList



# -- Tokenize ---------------------------------------

namePattern = '''
	\w+            # letter|number|underscore sequence
	(\.\w+)*       # dot followed by w+
'''
namePattern = re.compile( namePattern, re.X )


def isValidName( name ):

	return re.fullmatch( namePattern, name )


def tokenize( cmdList ):

	tokenizedCmdList = []

	for cmdEl in cmdList:

		cmdRaw = cmdEl[ 0 ]
		line   = cmdEl[ 1 ]

		op  = cmdRaw[ 0 ].upper()
		cmd = {}

		# Handle char, merge into one
		if "'" in cmdRaw:

			i = cmdRaw.index( "'" )

			# Check for closing quote
			if cmdRaw[ i + 2 ] != "'":

				raiseError( line )

			# stackoverflow.com/a/1142879
			cmdRaw[ i : i + 3 ] = [ ''.join( cmdRaw[ i : i + 3 ] ) ]


		# TypeD0 - ORG address
		if op == 'ORG':

			# Check for length
			if len( cmdRaw ) != 2:

				raiseError( line )

			cmd[ 'd_org' ] = cmdRaw[ 1 ]


		# TypeD1 - DDATA value
		elif op in dataDefinitions:

			# Check for length
			if len( cmdRaw ) != 2:

				raiseError( line )

			value = cmdRaw[ 1 ]
			nWords = dataDefinitions[ op ]

			cmd[ 'd_data' ] = {

				'value'  : value,
				'nWords' : nWords
			}


		# Type1 - [label]
		elif cmdRaw[ 0 ] == '[':

			cmdRaw.remove( '[' )

			# Check for and remove closing bracket
			try:

				cmdRaw.remove( ']' )

			except:

				raiseError( line )

			# Check for length
			if len( cmdRaw ) != 1:

				raiseError( line )

			cmd[ 'label' ] = cmdRaw[ 0 ]


		# Type2 & Type3 - op rX [address], op [address]
		elif '[' in cmdRaw:

			cmdRaw.remove( '[' )

			# Check for and remove closing bracket
			try:

				cmdRaw.remove( ']' )

			except:

				raiseError( line )

			# Check for length
			if len( cmdRaw ) == 2 or len( cmdRaw ) == 3:

				cmd[ 'op' ] = op

				# op [address]
				if len( cmdRaw ) == 2:

					# Check validity
					if op not in LT[ 'opJump' ]:

						raiseError( line )

					cmd[ 'address' ] = cmdRaw[ 1 ]

				# op rX [address]
				else:

					# Check validity
					if op not in LT[ 'opExtMemoryAccess' ]:

						raiseError( line )

					cmd[ 'rX' ]      = cmdRaw[ 1 ].upper()
					cmd[ 'address' ] = cmdRaw[ 2 ]

			else:

				raiseError( line )


		# Type 4 - op
		elif len( cmdRaw ) == 1:

			# Check validity
			if op not in LT[ 'opStandalone' ]:

				raiseError( line )

			cmd[ 'op' ] = op


		# Type5 - op rPair
		elif len( cmdRaw ) == 2:

			# Check validity
			if ( op not in LT[ 'opJump' ] ) and ( op != 'LXH' ):

				raiseError( line )

			cmd[ 'op' ] = op

			rPair = cmdRaw[ 1 ].upper()

			# Check validity
			if rPair not in LT[ 'registerPairs' ]:

				raiseError( line )

			cmd[ 'rPair' ] = rPair


		# Type6 - op rX rY, op rX rPair
		elif len( cmdRaw ) == 3:

			cmd[ 'op' ] = op
			cmd[ 'rX' ] = cmdRaw[ 1 ].upper()

			rY = cmdRaw[ 2 ].upper()

			# op rX rY
			if rY in LT[ 'registers' ]:

				cmd[ 'rY' ] = rY

			# op rX rPair
			elif rY in LT[ 'registerPairs' ]:

				# Check validity
				if op not in LT[ 'opExtMemoryAccess' ]:

					raiseError( line )

				cmd[ 'rPair' ] = rY

			else:

				raiseError( line )


		# Type7 - op rX rY immediate
		elif len( cmdRaw ) == 4:

			# Check validity
			if ( op in LT[ 'opStandalone' ] ) or ( op == 'LXH' ):

				raiseError( line )

			cmd[ 'op' ]        = op
			cmd[ 'rX' ]        = cmdRaw[ 1 ].upper()
			cmd[ 'rY' ]        = cmdRaw[ 2 ].upper()
			cmd[ 'immediate' ] = cmdRaw[ 3 ]


		# Unknown
		else:

			raiseError( line )

		# Debug
		# print( '{} -> {}'.format( line, cmd ) )

		# Add to list
		_cmdEl = [ cmd, line ]
		tokenizedCmdList.append( _cmdEl )

	# Done
	return tokenizedCmdList



# -- Label -------------------------------------------

def handleLabels( cmdList ):

	''' Remove labels and store their integer addresses '''

	locationCounter = 0

	trimmedCmdList = []

	waitingForBytePair = False

	for cmdEl in cmdList:

		cmd  = cmdEl[ 0 ]
		line = cmdEl[ 1 ]

		if 'label' in cmd:

			label = cmd[ 'label' ]  # get the label

			if not isValidName( label ):

				raise Exception( 'Invalid name - {}\n->  {}'.format( cmd, line ) )

			knownAddresses_ProgramMemory[ label ] = locationCounter  # add it to known addresses

		elif 'd_org' in cmd:

			newLoc = cmd[ 'd_org' ]  # TODO, convert to int (Raise error)

			if locationCounter <= newLoc:

				locationCounter = newLoc

			else:

				raise Exception(

					'Invalid ORG value {}. Expecting a value greater than the current location counter {}.\n->  {}',
					newLoc,
					locationCounter,
					line
				)

		else:

			# Not a label so include it
			trimmedCmdList.append( cmd )

			locationCounter += 1

			# Reserve space for immediates
			if 'd_data' in cmd:

				locationCounter += cmd[ 'd_data' ][ 'nWords' ] - 1

			elif 'immediate' in cmd:  # 16 bit immediate

				locationCounter += 1

			elif 'address' in cmd:    # 32 bit immediate

				locationCounter += 2


	return trimmedCmdList



# -- Encode ------------------------------------------

def decodeConstant( value, cmd, is32Bit = False ):

	words = []

	# Convert from string to integer

	if value in knownAddresses_DataMemory:

		value = knownAddresses_DataMemory[ value ]

	elif value in knownAddresses_ProgramMemory:

		value = knownAddresses_ProgramMemory[ value ]

	elif value[ 0 : 2 ].upper() == '0X':

		value = int( value, 16 )

	elif value[ 0 : 2 ].upper() == '0B':

		value = int( value, 2 )

	elif value[ 0 ] == "'":

		value = ord( value )

	else:

		value = int( value )


	# Extract words
	if is32Bit and value >= 0 and value <= largest_address:

		lo = value & 0xFFFF
		hi = value >> 16

		words.append( toBinary( lo, nBits ) )
		words.append( toBinary( hi, nBits ) )

	elif value >= 0 and value <= largest_immediate:

		words.append( toBinary( value, nBits ) )

	else:

		raise Exception( 'Invalid value - {} - in command - {}'.format( value, cmd ) )

	return words


def encodeInstructions( cmdList ):

	''' Translate assembly instructions to binary '''

	binCmdList = []

	rZero = LT[ 'registers' ][ 'R0' ]

	for cmd in cmdList:

		op = LT[ 'op' ][ cmd[ 'op' ] ]

		# Type2 & Type3 - op rX [address], op [address]
		if 'address' in cmd:

			if 'rX' in cmd:

				rX = LT[ 'registers' ][ cmd[ 'rX' ] ]

			else:

				rX = rZero

			has32BitImmediate = 1

			cmd_b = '{}0{}{}{}'.format(

				has32BitImmediate,
				op,
				rX,
				rZero
			)

			binCmdList.append( cmd_b )

			# address
			binCmdList.extend(

				decodeConstant( cmd[ 'address' ], cmd, is32Bit = True )
			)


		# Type 4 - op
		elif len( cmd ) == 1:

			cmd_b = '00{}{}{}'.format(

				op,
				rZero,
				rZero
			)

			binCmdList.append( cmd_b )


		# Type 5 - op rPair
		elif len( cmd ) == 2:

			rPair = LT[ 'registerPairs' ][ cmd[ 'rPair' ] ]

			isRegisterPair = '11'

			cmd_b = '{}{}{}{}'.format(

				isRegisterPair,
				op,
				rZero,
				rPair  # rPair encoded in rY slot
			)

			binCmdList.append( cmd_b )


		# Type6 - op rX rY, op rX rPair
		elif len( cmd ) == 3:

			rX = LT[ 'registers' ][ cmd[ 'rX' ] ]

			if 'rPair' in cmd:

				rY = LT[ 'registerPairs' ][ cmd[ 'rPair' ] ]

				isRegisterPair = '11'

				cmd_b = '{}{}{}{}'.format(

					isRegisterPair,
					op,
					rX,
					rY  # rPair encoded in rY slot
				)

			else:

				rY = LT[ 'registers' ][ cmd[ 'rY' ] ]

				cmd_b = '00{}{}{}'.format(

					op,
					rX,
					rY
				)

			binCmdList.append( cmd_b )


		# Type7 - op rX rY immediate
		elif len( cmd ) == 4:

			rX = LT[ 'registers' ][ cmd[ 'rX' ] ]
			rY = LT[ 'registers' ][ cmd[ 'rY' ] ]

			has16BitImmediate = 1

			cmd_b = '0{}{}{}{}'.format(

				has16BitImmediate,
				op,
				rX,
				rY
			)

			binCmdList.append( cmd_b )

			# immediate
			binCmdList.extend(

				decodeConstant( cmd[ 'immediate' ], cmd, is32Bit = False )
			)


		# Unknown
		else:

			raise Exception( "Shouldn't reach here!" )


	return binCmdList



# -- Main ----------------------------------------

def doTheThing( cmds_raw, debug ):

	''' Translate assembly to binary '''

	'''
		TODO:
		1) expand
		2) replace EQU
		3) spacefill DDATA?
		3) remove labels and ORG?
	'''

	# Expand MACROs
	cmds_assembly = expandMACRO( cmds_raw )
	for c in cmds_assembly: print( c[ 0 ] )
	# for c in cmds_assembly: print( c[ 0 ], "   ~~~   ", c[ 1 ] )
	print( '====\n' )

	# Replace EQUs
	cmds_assembly = handleEQU( cmds_assembly )
	for c in cmds_assembly: print( c[ 0 ] )
	print( '====\n' )

	# Tokenize
	cmds_assembly = tokenize( cmds_assembly )
	for c in cmds_assembly: print( c[ 0 ] )

	# # ?
	# cmds_assembly = handleLabels( cmds_assembly )
	# # handleDDATA, handleORG

	# # Encode
	# cmds_binary = encodeInstructions( cmds_assembly )

	# # Print debug
	# if debug: debugStuff( cmds_assembly, cmds_binary )

	# return cmds_binary



# -- Run ------------------------------------------

def writeToOutputFile( binCmdList, outputFile ):

	''' Generate an output file containing the binary commands '''

	with open( outputFile, 'w' ) as file:

		for cmd_binary in binCmdList:

			file.write( cmd_binary )
			file.write( '\n' )


def asm_to_bin( inputFile, outputFile, debug = False ):

	cmds_assembly = readInputFile( inputFile )

	cmds_binary = doTheThing( cmds_assembly, debug )

	# print( 'Assembled program has {} lines. Maximum is {}.'.format( len( cmds_binary ), largest_address ) )

	# # Check size
	# if len( cmds_binary ) > largest_address:

	# 	print( 'Assembled program exceeds maximum length by {} lines.'.format( len( cmds_binary ) - largest_address ) )

	# # Write
	# writeToOutputFile( cmds_binary, outputFile )

	# # print( 'Done' )


def genBINFile( inputDirPath, debug = False ):

	fileNames = os.listdir( inputDirPath )

	for fileName in fileNames:

		if fileName[ - 3 : ] == 'asm':

			inputFilePath = inputDirPath + '/' + fileName

			break  # Translate only first encountered in directory

	outputFilePath = inputDirPath + '/Main.bin'

	asm_to_bin( inputFilePath, outputFilePath, debug )
