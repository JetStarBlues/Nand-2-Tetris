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
import struct
import math

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
		'ADC'  : 5,
		'SUB'  : 6,
		'SBB'  : 7,
		'AND'  : 8,
		'OR'   : 9,
		'XOR'  : 10,
		'LSR'  : 11,
		'LSL'  : 12,
		'MUL'  : 13,
		'DIV'  : 14,
		'NOT'  : 15,
		'NEG'  : 16,
		'CMP'  : 17,
		'JMP'  : 18,
		'JEQ'  : 19,
		'JNE'  : 20,
		'JGT'  : 21,
		'JGE'  : 22,
		'JLT'  : 23,
		'JLE'  : 24,
		'JSR'  : 25,
		'RTS'  : 26,
		'LXH'  : 27,
		'SWI'  : 28,
		'RTI'  : 29,
		'IORD' : 30,
		'IOWR' : 31,
		'IODR' : 32,
		'HLT'  : 33,
		'NOP'  : 34,
	}
}

# Convert to binary string
for k, v in LT[ 'registers' ].items():

	LT[ 'registers' ][ k ] = toBinary( v, 4 )

for k, v in LT[ 'op' ].items():

	LT[ 'op' ][ k ] = toBinary( v, 6 )

# Create subsets
LT[ 'opJump' ] = newDictFromKeys( LT[ 'op' ],

	[
		'JMP',
		'JEQ',
		'JNE',
		'JGT',
		'JGE',
		'JLT',
		'JLE',
		'JSR',
	]
)
LT[ 'opStandalone' ] = newDictFromKeys( LT[ 'op' ],

	[
		'RTS',
		'RTI',
		'HLT',
		'NOP',
	]
)
LT[ 'opVanilla' ] = [

	op for op in LT[ 'op' ] if
	( op not in LT[ 'opJump' ] ) and
	( op not in LT[ 'opStandalone' ] ) and
	( op not in [ 'LXH', 'SWI' ] )
]

# Data definitions
dataDefinitions = {

	'DBYTE'   : 0.25,  # 1/4 word
	'DHALF'   : 0.5,   # 1/2 word
	'DWORD'   : 1,     # 1 word
	'DDOUBLE' : 2,     # 2 words
}



# == Debug ===================================================

def getKeyByValue( value, d ):

	# stackoverflow.com/a/8023337

	for k, v in d.items():

		if v == value:

			return k

	return None


def getHex8( value ):

	return hex( value )[ 2 : ].zfill( 8 )

def getASCII32( value ):

	c3 = ( value >> 24 ) & 0xFF
	c2 = ( value >> 16 ) & 0xFF
	c1 = ( value >>  8 ) & 0xFF
	c0 = value & 0xFF

	s = ''

	for c in [ c3, c2, c1, c0 ]:

		if c >= 32 and c <= 126:  # printable

			s += chr( c )

		else:

			s += '.'

	return s


def printFinalAssembly( asmCmdList, binCmdList ):

	showBinary = True

	def getBinaryString():  # DRY

		s = ''

		if showBinary:

			iVal = int( binCmdList[ bIdx ], 2 )

			# s = '{:<8}  {:<32}  |   '.format(

			# 	getHex8( iVal ),
			# 	binCmdList[ bIdx ]
			# )

			s = '{:<8}  {}  |   '.format(

				getHex8( iVal ),
				getASCII32( iVal )
			)

		return s

	bIdx = 0

	for cmdEl in asmCmdList:

		cmd  = cmdEl[ 0 ]
		line = cmdEl[ 1 ]

		label = getKeyByValue( bIdx, knownAddresses_ProgramMemory )

		# Data definition
		if 'd_data' in cmd:

			nWords  = cmd[ 'd_data' ][ 'nWords' ]
			nValues = len( cmd[ 'd_data' ][ 'values' ] )

			if nWords == 0.25:

				n = math.ceil( nValues / 4 )

			elif nWords == 0.5:

				n = math.ceil( nValues / 2 )

			elif nWords == 1:

				n = nValues

			elif nWords == 2:

				n = nValues * 2

			for _ in range( n ):

				w = int( binCmdList[ bIdx ], 2 )

				s_label = ':: {} '.format( label ) if label else ''

				print( '{}{:<11} -   {}{:<11}'.format(

					getBinaryString(),
					bIdx,
					s_label,
					w
				) )

				bIdx += 1

			continue


		# Everything else
		'''
			op
			op rX
			op immediate
			op rX rY
			op rX immediate
		'''
		op        = cmd.get( 'op' )
		rX        = cmd.get( 'rX' )
		rY        = cmd.get( 'rY' )
		immediate = cmd.get( 'immediate' )

		s_label = ':: {} '.format( label ) if label else ''
		s_op    =    '{} '.format( op )
		s_rX    =    '{} '.format( rX ) if rX else ''
		s_rY    =    '{} '.format( rY ) if rY else ''

		print( '{}{:<11} -   {}{}{}{}'.format(

			getBinaryString(),
			bIdx,
			s_label,
			s_op,
			s_rX,
			s_rY

		) )

		if immediate:

			bIdx += 1

			w = int( binCmdList[ bIdx ], 2 )

			# program address
			label = getKeyByValue( w, knownAddresses_ProgramMemory )

			# data address
			if not label:

				label = getKeyByValue( w, knownAddresses_DataMemory )

			# Jumping to unknown location
			if ( not label ) and ( op in LT[ 'opJump' ] ):

				label = '???'

			s_label = '   // {}'.format( label ) if label else ''

			print( '{}{:<11} -   {:<11}{}'.format(

				getBinaryString(),
				bIdx, 
				w,
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
nBits = 32

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
	//       |    # start of comment
	::       |    # label marker
	\(|\)    |    # macro argument wrappers
	".+"     |    # string
	\'.\'    |    # character
	\d+\.\d+ |    # float
	\w+           # word or digit sequence
'''
cmdPattern = re.compile( cmdPattern, re.X | re.ASCII )


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


def expandMACRO( cmdRaw, macros, expandedCmdList ):

	name = cmdRaw[ 0 ]

	# Get arguments
	parameters = macros[ name ][ 'parameters' ]

	arguments = cmdRaw[ 1 : ]

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


def handleMACRO( cmdList ):

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

			if isMacroDef:

				raise Exception( 'Invalid - MACRO definition inside a MACRO definition\n->  {}'.format( line ) )

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

				# If there is a call to another (already defined) macro within
				# this macro, expand it accordingly
				if cmdRaw[ 0 ] in macros:  # preserve case

					cmdEls = []

					expandMACRO( cmdRaw, macros, cmdEls )

					for cmdEl in cmdEls:

						macros[ macroDefName ][ 'statements' ].append( cmdEl )

				else:

					macros[ macroDefName ][ 'statements' ].append( cmdEl )

			continue


		# Call of macro
		elif cmdRaw[ 0 ] in macros:  # preserve case

			expandMACRO( cmdRaw, macros, expandedCmdList )

			continue

		# Not a macro definition or call
		else:

			expandedCmdList.append( cmdEl )


	# Reached end without finding 'ENDMACRO'
	if isMacroDef:

		raise Exception( "Expected an 'ENDMACRO' statement" )


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

			if alias in knownAliases:

				raise Exception( "EQU for '{}' is already defined - {}".format( alias, line ) )

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

		# print( cmdRaw )

		op  = cmdRaw[ 0 ].upper()
		cmd = {}


		# TypeD0 - DDATA value
		if op in dataDefinitions:

			# Check for length
			if len( cmdRaw ) < 2:

				raiseError( line )

			nWords  = dataDefinitions[ op ]
			values_ = cmdRaw[ 1 : ]
			values  = []
			
			for value in values_:

				if value[ 0 ] == '"':

					# ASCII strings only allowed for DBYTE
					if nWords != 0.25:

						raiseError( line )

					# Get characters from string
					chars = [ "'{}'".format( c ) for c in value[ 1 : - 1 ] ]

					values.extend( chars )

				else:

					values.append( value )

			# print( values, '-', cmdRaw )

			cmd[ 'd_data' ] = {

				'nWords' : nWords,
				'values' : values,
			}


		# Type1 - :: label
		elif cmdRaw[ 0 ] == '::':

			# Check for length
			if len( cmdRaw ) != 2:

				raiseError( line )

			cmd[ 'label' ] = cmdRaw[ 1 ]


		# Type2 - op
		elif len( cmdRaw ) == 1:

			# Check validity
			if op not in LT[ 'opStandalone' ]:

				raiseError( line )

			cmd[ 'op' ] = op


		# Type3 - op rX
		# Type4 - op immediate
		elif len( cmdRaw ) == 2:

			cmd[ 'op' ] = op

			rX = cmdRaw[ 1 ].upper()


			# Type3 - op rX
			if rX in LT[ 'registers' ]:

				# Check validity
				if op != 'LXH':

					raiseError( line )

				cmd[ 'rX' ] = rX


			# Type4 - op immediate
			else:

				# Check validity
				if op not in LT[ 'opJump' ] and ( op != 'SWI' ):

					raiseError( line )

				cmd[ 'immediate' ] = cmdRaw[ 1 ]  # preserve case


		# Type5 - op rX rY
		# Type6 - op rX immediate
		elif len( cmdRaw ) == 3:

			cmd[ 'op' ] = op
			cmd[ 'rX' ] = cmdRaw[ 1 ].upper()

			rY = cmdRaw[ 2 ].upper()


			# Type5 - op rX rY
			if rY in LT[ 'registers' ]:

				# Check validity
				if op not in LT[ 'opVanilla' ]:

					raiseError( line )

				cmd[ 'rY' ] = rY


			# Type6 - op rX immediate
			else:

				# Check validity
				if op not in LT[ 'opVanilla' ]:

					raiseError( line )

				cmd[ 'immediate' ] = cmdRaw[ 2 ]  # preserve case


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

		else:

			# Not a label so include it
			trimmedCmdList.append( cmdEl )

			locationCounter += 1

			# Reserve space for immediates
			if 'immediate' in cmd:

				locationCounter += 1

			elif 'd_data' in cmd:

				nWords  = cmd[ 'd_data' ][ 'nWords' ]
				nValues = len( cmd[ 'd_data' ][ 'values' ] )

				locationCounter -= 1  # one word will be on same line

				if nWords == 0.25:

					locationCounter += math.ceil( nValues / 4 )

				elif nWords == 0.5:

					locationCounter += math.ceil( nValues / 2 )

				elif nWords == 1:

					locationCounter += nValues

				elif nWords == 2:

					locationCounter += nValues * 2


	return trimmedCmdList



# -- Encode ------------------------------------------

def floatToInt( value, precision ):

	if precision == 1:

		s = struct.pack( '>f', float( value ) )

		i32 = struct.unpack( '>L', s )[ 0 ]

		return i32

	elif precision == 2:

		s = struct.pack( '>d', float( value ) )

		i64 = struct.unpack( '>Q', s )[ 0 ]

		return i64


def strToInt( value, nWords, line ):

	''' Convert from string to integer '''

	if value in knownAddresses_DataMemory:

		value = knownAddresses_DataMemory[ value ]

	elif value in knownAddresses_ProgramMemory:

		value = knownAddresses_ProgramMemory[ value ]

	elif value[ 0 ] == "'":

		value = ord( value[ 1 ] )

	elif value.count( '.' ) == 1:

		value = floatToInt( value, nWords )  # nWords doubles as precision

	else:

		# remove underscore used to visually space digits/letters
		value = value.replace( '_', '' )

		if value[ 0 : 2 ].upper() == '0X':

			value = int( value, 16 )

		elif value[ 0 : 2 ].upper() == '0B':

			value = int( value, 2 )

		else:

			value = int( value )

	#
	if value > 2 ** ( 32 * nWords ):

		raise Exception( 'Constant larger than defined size - {}\n->  {}'.format( value, line ) )


	return value


def decodeConstants( values, nWords, line ):

	# Extract words
	words = []

	if not isinstance( values, list ):

		values = [ values ]  # make it a list =p


	# 8 bit
	if ( nWords == 0.25 ):

		# Pad with zeros so that word aligned
		pad = len( values ) % 4

		if pad > 0:

			pad = 4 - pad

		for i in range( pad ):

			values.append( '0' )  # Big endian, so append to end (lsb)

		# Combine to form words
		for i in range( 0, len( values ), 4 ):

			b3 = strToInt( values[ i     ], nWords, line )
			b2 = strToInt( values[ i + 1 ], nWords, line )
			b1 = strToInt( values[ i + 2 ], nWords, line )
			b0 = strToInt( values[ i + 3 ], nWords, line )

			word = ( b3 << 24 ) | ( b2 << 16 ) | ( b1 << 8 ) | b0

			words.append( toBinary( word, nBits ) )


	# 16 bit
	elif ( nWords == 0.5 ):

		# Pad with zeros so that word aligned
		if len( values ) % 2 == 1:

			values.append( '0' )  # Big endian, so append to end (lsb)

		# Combine to form words
		for i in range( 0, len( values ), 2 ):

			hw1 = strToInt( values[ i     ], nWords, line )
			hw0 = strToInt( values[ i + 1 ], nWords, line )

			word = ( hw1 << 16 ) | hw0

			words.append( toBinary( word, nBits ) )


	# 32 bit
	elif ( nWords == 1 ):

		for value_ in values:

			value = strToInt( value_, nWords, line )

			words.append( toBinary( value, nBits ) )


	# 64 bit
	elif ( nWords == 2 ):

		for value_ in values:

			value = strToInt( value_, nWords, line )

			hi = value >> 32
			lo = value & 0xFFFFFFFF

			words.append( toBinary( hi, nBits ) )  # Big endian
			words.append( toBinary( lo, nBits ) )


	else:

		raise Exception( 'Invalid constant - {}\n->  {}'.format( value, line ) )

	return words


def encodeInstructions( cmdList ):

	''' Translate assembly instructions to binary '''

	binCmdList = []

	rZero = LT[ 'registers' ][ 'R0' ]

	for cmdEl in cmdList:

		cmd  = cmdEl[ 0 ]
		line = cmdEl[ 1 ]

		# TypeD0 - DDATA value
		if 'd_data' in cmd:

			values = cmd[ 'd_data' ][ 'values' ]
			nWords = cmd[ 'd_data' ][ 'nWords' ]


			binCmdList.extend(

				decodeConstants( values, nWords, line )
			)

			continue


		op = LT[ 'op' ][ cmd[ 'op' ] ]

		unusedHalf = '0000000000000000'

		# Type4 - op immediate
		# Type6 - op rX immediate
		if 'immediate' in cmd:

			if 'rX' in cmd:

				rX = LT[ 'registers' ][ cmd[ 'rX' ] ]

			else:

				rX = rZero

			hasImmediate = 1

			cmd_b = '{}0{}{}{}{}'.format(

				unusedHalf,
				hasImmediate,
				op,
				rX,
				rZero
			)

			binCmdList.append( cmd_b )

			# 32bit immediate
			binCmdList.extend(

				decodeConstants( cmd[ 'immediate' ], 1, line )
			)


		# Type2 - op
		elif len( cmd ) == 1:

			cmd_b = '{}00{}{}{}'.format(

				unusedHalf,
				op,
				rZero,
				rZero
			)

			binCmdList.append( cmd_b )


		# Type3 - op rX
		elif len( cmd ) == 2:

			rX = LT[ 'registers' ][ cmd[ 'rX' ] ]

			cmd_b = '{}00{}{}{}'.format(

				unusedHalf,
				op,
				rX,
				rZero
			)

			binCmdList.append( cmd_b )


		# Type5 - op rX rY
		elif len( cmd ) == 3:

			rX = LT[ 'registers' ][ cmd[ 'rX' ] ]
			rY = LT[ 'registers' ][ cmd[ 'rY' ] ]

			cmd_b = '{}00{}{}{}'.format(

				unusedHalf,
				op,
				rX,
				rY
			)

			binCmdList.append( cmd_b )


		# Unknown
		else:

			raise Exception( "Shouldn't reach here!" )


	return binCmdList



# -- Main ----------------------------------------

def doTheThing( cmds_raw, debug ):

	''' Translate assembly to binary '''

	# Expand MACROs
	cmds_assembly = handleMACRO( cmds_raw )
	# for c in cmds_assembly: print( c[ 0 ] )
	# for c in cmds_assembly: print( c[ 0 ], "   ~~~   ", c[ 1 ] )
	# print( '====\n' )

	# Replace EQUs
	cmds_assembly = handleEQU( cmds_assembly )
	# for c in cmds_assembly: print( c[ 0 ] )
	# print( '====\n' )

	# Tokenize
	cmds_assembly = tokenize( cmds_assembly )
	# for c in cmds_assembly: print( c[ 0 ] )
	# print( '====\n' )

	# Label
	cmds_assembly = handleLabels( cmds_assembly )
	# for c in cmds_assembly: print( c[ 0 ] )
	# print( '====\n' )

	# Encode
	cmds_binary = encodeInstructions( cmds_assembly )

	# Print debug
	if debug: debugStuff( cmds_assembly, cmds_binary )

	return cmds_binary



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

	print( 'Assembled program has {} lines. Maximum is {}.'.format( len( cmds_binary ), largest_address ) )

	# Check size
	if len( cmds_binary ) > largest_address:

		print( 'Assembled program exceeds maximum length by {} lines.'.format( len( cmds_binary ) - largest_address ) )

	# Write
	writeToOutputFile( cmds_binary, outputFile )

	# print( 'Done' )


def genBINFile( inputDirPath, debug = False ):

	fileNames = os.listdir( inputDirPath )

	for fileName in fileNames:

		if fileName[ - 3 : ] == 'asm':

			inputFilePath = inputDirPath + '/' + fileName

			break  # Translate only first encountered in directory

	outputFilePath = inputDirPath + '/Main.bin'

	asm_to_bin( inputFilePath, outputFilePath, debug )
