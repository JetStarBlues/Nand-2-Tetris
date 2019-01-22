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

		15    -> unused
		14    -> has32BitImmediate
		13    -> has16BitImmediate
		12..8 -> fxSel
		7..4  -> xSel
		3..0  -> ySel

'''


# == Imports =================================================

# Built ins
import re
import os

# Hack computer
import Components._0__globalConstants as GC
from commonHelpers import *



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

		'RSTATUS'  : 13,
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

	'op' : {

		'MOV'  : 0,
		'STO'  : 1,
		'LD'   : 2,
		'ADD'  : 3,
		'SUB'  : 4,
		'AND'  : 5,
		'OR'   : 6,
		'XOR'  : 7,
		'LSR'  : 8,
		'LSL'  : 9,
		'MUL'  : 10,
		'DIV'  : 11,
		'NOT'  : 12,
		'NEG'  : 13,
		'JMP'  : 14,
		'JZ'   : 15,
		'JNZ'  : 16,
		'JC'   : 17,
		'JNC'  : 18,
		'JNG'  : 19,
		'JZP'  : 20,
		'SWI'  : 21,
		'RTI'  : 22,
		'IORD' : 23,
		'IOWR' : 24,
		'IODR' : 25,
		'HLT'  : 26,
		'NOP'  : 27,
	},

	'opJump' : {

		'JMP'  : 14,
		'JZ'   : 15,
		'JNZ'  : 16,
		'JC'   : 17,
		'JNC'  : 18,
		'JNG'  : 19,
		'JZP'  : 20,
	},

	'opStandalone' : {

		'HLT' : 26,
	}
}


for k, v in LT[ 'registers' ].items():

	LT[ 'registers' ][ k ] = toBinary( v, 4 )

for k, v in LT[ 'op' ].items():

	LT[ 'op' ][ k ] = toBinary( v, 5 )

for k, v in LT[ 'opJump' ].items():

	LT[ 'opJump' ][ k ] = toBinary( v, 5 )

for k, v in LT[ 'opStandalone' ].items():

	LT[ 'opStandalone' ][ k ] = toBinary( v, 5 )



# == Helpers =================================================

namePattern = '''
	\w+            # letter|number|underscore sequence
	(\.\w+)*       # dot followed by w+
'''
namePattern = re.compile( namePattern, re.X )

def isValidName( name ):

	return re.fullmatch( namePattern, name )



# == Debug ===================================================

def debugStuff( cmdList ):

	# Print final assembly
	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		label =   # lookup i

		op = cmd[ 'op' ]

		if 'rX' in cmd:

			rX = cmd[ 'rX' ]

		else:

			None

		if 'rY' in cmd:

			rY = cmd[ 'rY' ]

		else:

			None

		if op:

			print( '{:<5} - {} {} {} {}'.format( 

				i,
				'( ' + label + ' )' if label else '',
				op,
				rX                  if rX    else '',
				rY                  if rY    else '',
			) )

		elif 'immediate' in cmd:  ... ??

			print( '{:<5} - {}'.format(

				i,
				cmd[ 'immediate' ]
			) )

		elif 'address' in cmd:  ... ??  # { wHi, wLo }, { imm, rY }

			print( '{:<5} - {}'.format(

				i,
				cmd[ 'address' ]
			) )

		else:

			print( '{:<5} - ??? ... {}'.format( cmd ) )

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



# == Main ====================================================


# -- Constants -------------------------------------

# nBits = GC.N_BITS
nBits = 16

static_segment_start = GC.STATIC_START
static_segment_end   = GC.STATIC_END
static_segment_size  = static_segment_end - static_segment_start + 1

largest_immediate = 2 ** nBits - 1
largest_address   = 2 ** 32 - 1



# -- Extraction -------------------------------------

cmdPattern = '''
	//    |       # start of comment
	\'    |       # char wrappers
	\(|\) |       # label wrappers
	\{|\} |       # address wrappers
	\w+           # word or digit sequence
'''
cmdPattern = re.compile( cmdPattern, re.X )

def extractCmd( line ):

	# DRY
	def raiseError ():

		raise Exception( 'Invalid command - {}'.format( line.rstrip() ) )

	# Extract words from command (i.e. ignore whitespace)
	cmdRaw = re.findall( cmdPattern, line )
	cmd = {}

	# Ignore comment
	if '//' in cmdRaw:

		cmdRaw = cmdRaw[ 0 : cmdRaw.index( '//' ) ]


	if cmdRaw :  # wasn't just a comment


		# Handle char, merge into one
		if "'" in cmdRaw:

			i = cmdRaw.index( "'" )

			# Check for closing quote
			if cmdRaw[ i + 2 ] != "'":

				raiseError()

			# stackoverflow.com/a/1142879
			cmdRaw[ i : i + 3 ] = [ ''.join( cmdRaw[ i : i + 3 ] ) ]


		# Type1 - (label)
		if '(' in cmdRaw:

			cmdRaw.remove( '(' )

			# Check for and remove closing parenthesis
			try:

				cmdRaw.remove( ')' )

			except:

				raiseError()

			# Check for length
			if len( cmdRaw ) == 1:

				cmd[ 'label' ] = cmdRaw[ 0 ]

			else:

				raiseError()


		# Type2 & Type3 - op rX {address}, op {address}
		elif '{' in cmdRaw:

			cmdRaw.remove( '{' )

			# Check for and remove closing bracket
			try:

				cmdRaw.remove( '}' )

			except:

				raiseError()

			op = cmdRaw[ 0 ].upper()

			# Check for length
			if len( cmdRaw ) == 2 or len( cmdRaw ) == 3:

				cmd[ 'op' ] = op

				if len( cmdRaw ) == 2:

					# Check validity
					if op not in LT[ 'opJump' ]:

						raiseError()

					cmd[ 'address' ] = cmdRaw[ 1 ]

				else:

					# Check validity
					if ( op not in LT[ 'opJump' ] ) and ( op not in [ 'LD', 'STO' ] ):

						raiseError()

					cmd[ 'rX' ]      = cmdRaw[ 1 ].upper()
					cmd[ 'address' ] = cmdRaw[ 2 ]

			else:

				raiseError()


		# Type 4 - op
		elif len( cmdRaw ) == 1:

			op = cmdRaw[ 0 ].upper()

			# Check validity
			if op not in LT[ 'opStandalone' ]:

				raiseError()
			
			cmd[ 'op' ] = op


		# Type5 & Type6 - op rX rY immediate, op rX rY
		else:

			if len( cmdRaw ) == 3:

				cmd[ 'op' ] = cmdRaw[ 0 ].upper()
				cmd[ 'rX' ] = cmdRaw[ 1 ].upper()
				cmd[ 'rY' ] = cmdRaw[ 2 ].upper()

			elif len( cmdRaw ) == 4:

				cmd[ 'op' ]        = cmdRaw[ 0 ].upper()
				cmd[ 'rX' ]        = cmdRaw[ 1 ].upper()
				cmd[ 'rY' ]        = cmdRaw[ 2 ].upper()
				cmd[ 'immediate' ] = cmdRaw[ 3 ]

			else:

				raiseError()

		print( '{} -> {}'.format( line.rstrip(), cmd ) )

	return cmd


def extractCmds( inputFile ):

	commands = []

	with open( inputFile, 'r' ) as file:
		
		for line in file:

			cmd = extractCmd( line )

			if cmd:

				commands.append( cmd )

	return commands



# -- Translation -------------------------------------

knownAddresses_ProgramMemory = {}
knownAddresses_DataMemory = {}
knownAddresses_DataMemory.update( LT[ 'dataMemoryAddresses' ] )  # fill with global addresses


def handleLabels( cmdList ):

	''' Remove labels and store their integer addresses '''

	trimmedCmdList = []

	nImmediates = 0  # track as affects ultimate position

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if 'label' in cmd:

			label = cmd[ 'label' ]  # get the label

			if not isValidName( label ):

				raise Exception( 'Invalid name - {}'.format( cmd ) )

			addr = i + nImmediates - len( knownAddresses_ProgramMemory )  # and the corresponding address
			                                                              # Note, subtraction is for '(label)' statements which will later be removed

			knownAddresses_ProgramMemory[ label ] = addr  # add it to dict of knownAddresses_ProgramMemory

		else:

			trimmedCmdList.append( cmd )  # not a label so include it

			# check if has immediate (just count args and assume validity is checked later)
			if 'immediate' in cmd:

				nImmediates += 1

			elif 'address' in cmd:

				nImmediates += 2

	return trimmedCmdList


def decodeConstant( value, cmd, is32Bit = False ):

	words = []

	# Convert from string to integer

	# if value in knownAddresses_DataMemory:

	# 	value = knownAddresses_DataMemory[ value ]

	# TODO, check EQUs

	if value in knownAddresses_ProgramMemory:

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

	print( '-- {} -- {}'.format( value, words ) )

	return words


def translateInstructions( cmdList, debugCmdList ):

	''' Translate assembly instructions to binary '''

	binCmdList = []

	rZero = LT[ 'registers' ][ 'R0' ]

	for cmd in cmdList:

		op = LT[ 'op' ][ cmd[ 'op' ] ]

		# Type2 & Type3 - op rX {address}, op {address}
		if 'address' in cmd:

			if 'rX' in cmd:

				rX = LT[ 'registers' ][ cmd[ 'rX' ] ]

			else:

				rX = rZero

			has32BitImmediate = 1

			print( '--> 32 --> {}'.format( cmd ) )

			cmd_b = '0{}0{}{}{}'.format(

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

			cmd_b = '000{}{}{}'.format(

				op,
				rZero,
				rZero
			)

			binCmdList.append( cmd_b )


		# Type5 & Type6 - op rX rY immediate, op rX rY
		else:

			rX = LT[ 'registers' ][ cmd[ 'rX' ] ]
			rY = LT[ 'registers' ][ cmd[ 'rY' ] ]

			has16BitImmediate = 0

			if 'immediate' in cmd:

				has16BitImmediate = 1

			cmd_b = '00{}{}{}{}'.format(

				has16BitImmediate,
				op,
				rX,
				rY
			)

			binCmdList.append( cmd_b )

			# immediate
			if has16BitImmediate:

				print( '--> 16 --> {}'.format( cmd ) )

				binCmdList.extend(

					decodeConstant( cmd[ 'immediate' ], cmd, is32Bit = False )
				)

	return binCmdList


def translateCmds( cmdList, debug ):

	''' Translate assembly to binary '''

	debugCmdList = []
	cmdList      = handleLabels( cmdList )
	binCmdList   = translateInstructions( cmdList, debugCmdList )

	if debug: debugStuff( debugCmdList )

	return binCmdList



# -- Output --------------------------------------


def writeToOutputFile( binCmdList, outputFile ):

	''' Generate an output file containing the binary commands '''

	with open( outputFile, 'w' ) as file:

		for cmd_binary in binCmdList:

			file.write( cmd_binary )
			file.write( '\n' )



# -- Run ------------------------------------------


def asm_to_bin( inputFile, outputFile, debug = False ):

	# Read
	cmds_assembly = extractCmds( inputFile )

	# Translate
	cmds_binary = translateCmds( cmds_assembly, debug )

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
