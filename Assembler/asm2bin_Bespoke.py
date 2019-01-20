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
		14    -> unused
		13    -> hasImmediate
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

		'r0'       : 0,
		'r1'       : 1,
		'r2'       : 2,
		'r3'       : 3,
		'r4'       : 4,
		'r5'       : 5,
		'r6'       : 6,
		'r7'       : 7,
		'r8'       : 8,
		'r9'       : 9,
		'r10'      : 10,
		'r11'      : 11,
		'r12'      : 12,
		'r13'      : 13,
		'r14'      : 14,
		'r15'      : 15,

		'rStatus'  : 13,
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

	'op' : {},

	'opJump' : {},

	'opStandalone' : {

		'HLT' : '',
	}
}



# == Helpers =================================================

namePattern = '''
	\w+            # letter|number|underscore sequence
	(\.\w+)*       # dot followed by w+
'''
namePattern = re.compile( namePattern, re.X )

def isValidName( name ):

	return re.fullmatch( namePattern, name )



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
	\w+   |  # word or digit sequence
	//    |  # start of comment
	\(|\) |  # label wrappers
	\{|\}    # address wrappers
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

			# Check for length
			if len( cmdRaw ) == 2 or len( cmdRaw ) == 3:

				cmd[ 'op' ] = cmdRaw[ 0 ]

				if len( cmdRaw ) == 2:

					cmd[ 'address' ] = cmdRaw[ 1 ]

				else:

					cmd[ 'rX' ]      = cmdRaw[ 1 ]
					cmd[ 'address' ] = cmdRaw[ 2 ]

			else:

				raiseError()

		# Type 4 - op
		elif len( cmdRaw ) == 1:

			c = cmdRaw[ 0 ].upper()

			if c in LT[ 'opStandalone' ]:

				cmd[ 'op' ] = c

			else:

				raiseError()

		# Type5 & Type6 - op rX rY immediate, op rX rY
		else:

			if len( cmdRaw ) == 3:

				cmd[ 'op' ] = cmdRaw[ 0 ]
				cmd[ 'rX' ] = cmdRaw[ 1 ]
				cmd[ 'rY' ] = cmdRaw[ 2 ]

			elif len( cmdRaw ) == 4:

				cmd[ 'op' ]        = cmdRaw[ 0 ]
				cmd[ 'rX' ]        = cmdRaw[ 1 ]
				cmd[ 'rY' ]        = cmdRaw[ 2 ]
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

	# trimmedCmdList = []

	# nImmediates = 0  # track as affects ultimate position

	# for i in range( len( cmdList ) ):

	# 	cmd = cmdList[ i ]

	# 	if cmd[ 0 ] == '(':

	# 		label = cmd[ 1 : - 1 ]  # get the label

	# 		if not isValidName( label ):

	# 			raise Exception( 'Invalid name - {}'.format( cmd ) )

	# 		addr = i + nImmediates - len( knownAddresses_ProgramMemory )  # and the corresponding address
	# 		                                                              # Note, subtraction is for '(label)' statements which will later be removed

	# 		knownAddresses_ProgramMemory[ label ] = addr  # add it to dict of knownAddresses_ProgramMemory

	# 	else:

	# 		trimmedCmdList.append( cmd )  # not a label so include it

	# 		# check if has immediate (just count args and assume validity is checked later)
	# 		if len( cmd ) == 4:

	# 			nImmediates += 1


	# return trimmedCmdList

	pass










# def translateCmds( cmdList, debug ):

# 	''' Translate assembly to binary '''

# 	cmdList    = handleLabels( cmdList )
# 	cmdList    = handleVariables( cmdList )
# 	binCmdList = translateInstructions( cmdList )

# 	if debug: debugStuff( cmdList )

# 	return binCmdList



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

	# # Translate
	# cmds_binary = translateCmds( cmds_assembly, debug )

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


