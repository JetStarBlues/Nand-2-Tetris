# ========================================================================================
# 
#  Description:
# 
#     Compiles Hack ASM (assembly) code to Hack BIN (binary) code
#     Uses the vanilla TECS specification
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

	> Instruction

		Instruction - 0123456789ABCDEF

			0 -> opCode

			if opCode == 0, address instruction

				123456789ABCDEF -> address

			else, computation instruction

				1   -> unused
				2   -> unused
				3   -> y = A (0) | M (1)
				4   -> comp, zero_x  
				5   -> comp, not_x  
				6   -> comp, zero_y  
				7   -> comp, not_y  
				8   -> comp, and (0) | add (1)  
				9   -> comp, not_out
				ABC -> destination
				DEF -> jump

				comp(utation) bits are sent to ALU

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

	'globalAddresses' : {

		'@R0'       : '@0',
		'@R1'       : '@1',
		'@R2'       : '@2',
		'@R3'       : '@3',
		'@R4'       : '@4',
		'@R5'       : '@5',
		'@R6'       : '@6',
		'@R7'       : '@7',
		'@R8'       : '@8',
		'@R9'       : '@9',
		'@R10'      : '@10',
		'@R11'      : '@11',
		'@R12'      : '@12',
		'@R13'      : '@13',
		'@R14'      : '@14',
		'@R15'      : '@15',

		# VM structure
		'@SP'       : '@0',
		'@LCL'      : '@1',
		'@ARG'      : '@2',
		'@THIS'     : '@3',
		'@THAT'     : '@4',
		'@TEMP0'    : '@5',
		'@TEMP1'    : '@6',
		'@TEMP2'    : '@7',
		'@TEMP3'    : '@8',
		'@TEMP4'    : '@9',
		'@TEMP5'    : '@10',
		'@TEMP6'    : '@11',
		'@TEMP7'    : '@12',
		'@GP0'      : '@13',
		'@GP1'      : '@14',
		'@GP2'      : '@15',

		'@SCREEN'   : '@' + str( GC.SCREEN_MEMORY_MAP ),
		'@KEYBOARD' : '@' + str( GC.KEYBOARD_MEMORY_MAP ),
		'@MOUSE'    : '@' + str( GC.MOUSE_MEMORY_MAP ),
	},

	'comp' : {

		# ub1, ub0, ySel, zx, nx, zy, ny, f, no
		'0'    : '110101010',
		'1'    : '110111111',
		'-1'   : '110111010',
		'D'    : '110001100',
		'A'    : '110110000',
		'!D'   : '110001101',
		'!A'   : '110110001',
		'-D'   : '110001111',
		'-A'   : '110110011',
		'D+1'  : '110011111',
		'A+1'  : '110110111',
		'D-1'  : '110001110',
		'A-1'  : '110110010',
		'D+A'  : '110000010',
		'A+D'  : '110000010',  # order doesn't matter
		'D-A'  : '110010011',
		'A-D'  : '110000111',
		'D&A'  : '110000000',
		'A&D'  : '110000000',  # order doesn't matter
		'D|A'  : '110010101',
		'A|D'  : '110010101',  # order doesn't matter
		'M'    : '111110000',
		'!M'   : '111110001',
		'-M'   : '111110011',
		'M+1'  : '111110111',
		'M-1'  : '111110010',
		'D+M'  : '111000010',
		'M+D'  : '111000010',  # order doesn't matter
		'D-M'  : '111010011',
		'M-D'  : '111000111',
		'D&M'  : '111000000',
		'M&D'  : '111000000',  # order doesn't matter
		'D|M'  : '111010101',
		'M|D'  : '111010101',  # order doesn't matter
	},

	'dest' : {
		
		# d3, d2, d1
		'NULL' : '000',
		'M'    : '001',
		'D'    : '010',
		'A'    : '100',
		'DM'   : '011',
		'MD'   : '011',  # order doesn't matter
		'AM'   : '101',
		'MA'   : '101',  # order doesn't matter
		'AD'   : '110',
		'DA'   : '110',  # order doesn't matter
		'MDA'  : '111',
		'MAD'  : '111',  # order doesn't matter
		'AMD'  : '111',  # order doesn't matter
		'ADM'  : '111',  # order doesn't matter
		'DMA'  : '111',  # order doesn't matter
		'DAM'  : '111'   # order doesn't matter
	},

	'jump' : {
		
		# j3, j2, j1
		'NULL' : '000',
		'JGT'  : '001',
		'JEQ'  : '010',
		'JLT'  : '100',
		'JGE'  : '011',
		'JLE'  : '110',
		'JNE'  : '101',
		'JMP'  : '111'
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



# == Debug ===================================================

def debugStuff( cmdList ):

	# Print final assembly
	for c in cmdList:

		print( c )

	print( '\n--\n' )

	# Print labels
	for kv in sorted(

		knownAddresses_ProgramMemory.items(),
		key = lambda x : int( x[ 1 ][ 1 : ] ) 
	):		
		print( '{:<6}  {}'.format( kv[ 1 ], kv[ 0 ] ) )

	print( '\n--\n' )

	# Print variables
	for kv in sorted(

		knownAddresses_DataMemory.items(),
		key = lambda x : int( x[ 1 ][ 1 : ] )
	):
		print( '{:<6}  {}'.format( kv[ 1 ], kv[ 0 ] ) )



# == Main ====================================================


# -- Constants -------------------------------------

# nBits = GC.N_BITS
nBits = 16

static_segment_start = GC.STATIC_START
static_segment_end   = GC.STATIC_END
static_segment_size  = static_segment_end - static_segment_start + 1

largest_immediate = 2 ** ( nBits - 1 ) - 1
largest_address   = 2 ** 15 - 1



# -- Extraction -------------------------------------

# Select everything that is not a comment
cmdPattern = '''
	^                # from beginning of string
	.*?              # select all characters until
	(?=\/\/|[\r\n])  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )


def extractCmd( line ):

	line = line.replace( ' ', '' )         # remove spaces
	line = line.replace( '\t', '' )        # remove tabs

	found = re.search( cmdPattern, line )  # select everything that is not a comment

	if found:

		return found.group( 0 )

	else:

		return None


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
knownAddresses_DataMemory.update( LT[ 'globalAddresses' ] )  # fill with global addresses


def handleLabels( cmdList ):

	''' Remove labels and store their integer addresses '''

	trimmedCmdList = []

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '(':

			label = cmd[ 1 : - 1 ]  # get the label

			if not isValidName( label ):

				raise Exception( 'Invalid name - {}'.format( cmd ) )

			addr = i - len( knownAddresses_ProgramMemory )  # and the corresponding address
			                                                # Note, subtraction is for '(label)' statements which will later be removed

			knownAddresses_ProgramMemory[ '@{}'.format( label ) ] = '@{}'.format( addr )  # add it to dict of knownAddresses_ProgramMemory

		else:

			trimmedCmdList.append( cmd )  # not a label so include it

	return trimmedCmdList


def handleVariables( cmdList ):

	''' Replace label and variable names with integer addresses '''

	freeAddress = static_segment_start

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '@':

			# Refers to an integer
			if cmd[ 1 : ].isdigit():

				# Check that valid immediate
				if int( cmd[ 1 : ] ) > largest_immediate:

					raise Exception( 'Invalid integer - {}'.format( cmd ) )

				continue  # skip

			# Refers to a known label
			elif cmd in knownAddresses_ProgramMemory:

				cmdList[ i ] = knownAddresses_ProgramMemory[ cmd ]

			# Refers to a known variable
			elif cmd in knownAddresses_DataMemory:

				cmdList[ i ] = knownAddresses_DataMemory[ cmd ]
			
			# Allocate it
			else:  

				name = cmd[ 1 : ]

				if not isValidName( name ):

					raise Exception( 'Invalid name - {}'.format( cmd ) )

				if freeAddress > static_segment_end:

					raise Exception( 'Ran out of static memory' )

				newAddr = '@{}'.format( freeAddress )       # create new address

				knownAddresses_DataMemory[ cmd ] = newAddr  # add it to dict of knownAddresses_DataMemory

				cmdList[ i ] = newAddr                      # and set it

				freeAddress += 1 	# register is no longer unallocated

	print( 'Assembled program has {} global static variables. Maximum is {}.'.format(

		freeAddress - static_segment_start,
		static_segment_size
	) )

	# if freeAddress > static_segment_end:

	# 	print( 'Assembled program exceeds maximum number of global variables by {}.'.format( freeAddress - static_segment_end ) )

	return cmdList


def translateInstructions( cmdList ):

	''' Translate assembly instructions to binary '''

	binCmdList = []

	for i in range( len( cmdList ) ):

		#
		cmd_s = cmdList[ i ]
		cmd_b = None
		# print( cmd_s )


		# A instruction
		if cmd_s[0] == '@':

			opcode = '0'
			addr = int( cmd_s[ 1 : ] )
			addr = toBinary( addr, nBits - 1 )
			cmd_b = opcode + addr


		# HALT instruction (not vanilla TECS but useful)
		elif cmd_s.upper() == 'HALT':

			cmd_b = '1111110000000000'

		# C instruction
		else:
	
			opcode = '1'
			nUnusedBits = ( nBits - 16 )  # 16 bits used to encode opcode(1), dest(3), comp( 2 + 1 + 6 ), jump(3)
			header = opcode + '1' * nUnusedBits
			
			dest, comp, jump = [ None ] * 3

			if '=' in cmd_s and ';' in cmd_s:
				dest, comp, jump = re.split( '=|;', cmd_s )

			elif '=' in cmd_s:
				dest, comp = re.split( '=', cmd_s )

			elif ';' in cmd_s:
				comp, jump = re.split( ';', cmd_s )

			# print( dest, comp, jump )

			dest = LT[ 'dest' ][ dest.upper() ] if dest else LT[ 'dest' ][ 'NULL' ]
			jump = LT[ 'jump' ][ jump.upper() ] if jump else LT[ 'jump' ][ 'NULL' ]
			comp = LT[ 'comp' ][ comp.upper() ]

			cmd_b = header + comp + dest + jump


		#
		binCmdList.append( cmd_b )

	return binCmdList


def translateCmds( cmdList, debug ):

	''' Translate assembly to binary '''

	cmdList    = handleLabels( cmdList )
	cmdList    = handleVariables( cmdList )
	binCmdList = translateInstructions( cmdList )

	if debug: debugStuff( cmdList )

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
