# ========================================================================================
# 
#  Description:
# 
#     Compiles Hack ASM (assembly) code to Hack BIN (binary) code
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistributions and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================


# == Imports =================================================

# Built ins
import re
import os

# Hack computer
from Components._0__globalConstants import *


# == Helpers =================================================

def _toBinary( N, x ):
	return bin( x )[ 2 : ].zfill( N )


# == Main ====================================================


'''
	Instruction - 0123456789ABCDEF

		0 -> opCode

		if opCode == 0, address instruction

			123456789ABCDEF -> address

		else, computation instruction

			1   -> comp, xor
			2   -> comp, bitshift
			3   -> y = A (0) | M (1)
			4   -> comp, zero_x  
			5   -> comp, not_x  
			6   -> comp, zero_y  
			7   -> comp, not_y  
			8   -> comp, and (0) | add (1)  
			9   -> comp, negate_out
			ABC -> destination
			DEF -> jump

			comp(utation) bits are sent to ALU
'''


# -- Lookup tables ---------------------------------

lookup_comp = {

	# fub1, fub0, ySel, zx, nx, zy, ny, f, no
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

	'D^M'  : '101000000',
	'M^D'  : '101000000',  # order doesn't matter
	'D^A'  : '100000000',
	'A^D'  : '100000000',  # order doesn't matter
	'D<<M' : '011000000',
	'D>>M' : '001000000',
	# 'D<<A' : '010000000',  # not used, can omit to free instruction code
	# 'D>>A' : '000000000',  # not used, can omit to free instruction code

	# 'TUAA' : '111111111',  # toggle upper address access  ... TODO consider ALU out

	'MBANK0' : '000000000',
	'MBANK1' : '000000001',
	# 'MBANK2' : '000000010',
	# 'MBANK3' : '000000011',
}

lookup_dest = {
	
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
}

lookup_jmp = {
	
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

lookup_globalAddresses = {

	'@SCREEN' : '@' + str( SCREEN_MEMORY_MAP ),
	'@KBD'    : '@' + str( KBD_MEMORY_MAP ),

	'@R0'     : '@0',   # SP
	'@R1'     : '@1',   # ARG
	'@R2'     : '@2',   # LCL
	'@R3'     : '@3',   # THIS
	'@R4'     : '@4',   # THAT
	'@R5'     : '@5',   # TEMP
	'@R6'     : '@6',   # TEMP
	'@R7'     : '@7',   # TEMP
	'@R8'     : '@8',   # TEMP
	'@R9'     : '@9',   # TEMP
	'@R10'    : '@10',  # TEMP
	'@R11'    : '@11',  # TEMP
	'@R12'    : '@12',  # TEMP
	'@R13'    : '@13',  # GP
	'@R14'    : '@14',  # GP
	'@R15'    : '@15',  # GP

	'@SP'     : '@0',
	'@LCL'    : '@1',
	'@ARG'    : '@2',
	'@THIS'   : '@3',
	'@THAT'   : '@4',
	'@TEMP'   : '@5',
	'@GP'     : '@13',
	# '@STATIC' : '@16',
	# '@STACK'  : '@256',
	# '@HEAP'   : '@2048',
}

static_segment_start = 16
static_segment_end   = 255
static_segment_size = static_segment_end - static_segment_start + 1

# largest_int = 2 ** N_BITS - 1
memory_bank_size = 2 ** ( N_BITS - 1 )  # 2^(N-1) because first instruction bit is reserved for use as opcode
largest_addressable_int = memory_bank_size - 1



# -- Extraction -------------------------------------

# With regex --

# Select everything that is not a comment
cmdPattern = '''
	^                # from beginning of string
	.*?              # select all characters until
	(?=\/\/|[\r\n])  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )


def extractCmd( line ):

	line = line.replace( ' ', '' )   # remove spaces
	line = line.replace( '\t', '' )  # remove tabs
	line = line.upper()              # upper case everything

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment

	if found:

		cmd = found.group( 0 )
		# cmd = cmd.strip()   # remove leading and trailing whitespace
		return cmd.upper()  # upper case everything

	else:

		return None


# Without regex --

	# extract non commment
	# remove spaces and tabs
	# capitalize


def extractCmds( inputFile ):

	commands = []

	with open( inputFile, 'r' ) as input_file:
		
		for line in input_file:

			cmd = extractCmd( line )

			if cmd:

				commands.append( cmd )

	return commands



# -- Translation -------------------------------------


def addMemoryBank_stage1( cmdList ):

	''' Support for programs >= 2^(N_BITS - 1) lines long

		-> Adds memory bank selection placeholders.
		   Default is MBANK0
	'''

	# Get function names

	labels = []

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '(':

			label = cmd[ 1 : - 1 ]  # get the label

			labels.append( '@{}'.format( label ) )


	# Count number of insertions to be made. (Helper for Array.new)

	count = 0

	for label in labels:

		for i in range( len( cmdList ) ):

			if cmdList[ i ] == label:

				count += 1

	print( 'Assembled program contains {} functions'.format( count ) )


	# For every @functionName, precede with 'MBANK0' command

	expandedCmdList = []

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd == label:

			expandedCmdList.append( 'MAD=MBANK0;JMP' )  # 1 000000000 000 000

		expandedCmdList.append( cmd )


	return expandedCmdList


def handleLabels( cmdList ):

	''' Replace labels (function declarations) with integer addresses '''

	trimmedCmdList = []

	knownAddresses_ProgramMemory = {}

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '(':

			label = cmd[ 1 : - 1 ]    # get the label

			addr = i - len( knownAddresses_ProgramMemory )    # and the corresponding address

			knownAddresses_ProgramMemory[ '@{}'.format( label ) ] = '@{}'.format( addr )  # add it to dict of knownAddresses_ProgramMemory

		else:

			trimmedCmdList.append( cmd )   # not a label so include it

	return( trimmedCmdList, knownAddresses_ProgramMemory )


def addMemoryBank_stage2( cmdList, knownAddresses_ProgramMemory ):

	''' Support for programs >= 2 ^ ( N_BITS - 1 ) lines long

		-> Replaces placeholders with appropriate values.
		   MBANK0 with MBANKX
	'''

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		s = 'MAD=MBANK0;JMP'

		if cmd == s:

			label = cmdList[ i + 1 ]

			addr = knownAddresses_ProgramMemory[ label ]

			addr = int( addr[ 1 : ] )

			if addr > largest_addressable_int:

				bank, newAddr = divmod( addr, memory_bank_size )

				cmdList[ i ] = 'MAD=MBANK{};JMP'.format( bank )

				cmdList[ i + 1 ] = '@{}'.format( newAddr )

				knownAddresses_ProgramMemory[ label ] = '@{}'.format( newAddr )

	return ( cmdList, knownAddresses_ProgramMemory )


def handleVariables( cmdList, knownAddresses_ProgramMemory ):

	''' Replace variable names with integer addresses '''

	freeAddress = static_segment_start

	knownAddresses_DataMemory = {}
	knownAddresses_DataMemory.update( lookup_globalAddresses )  # fill with global addresses
	

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '@':

			# Refers to an integer
			if cmd[ 1 : ].isdigit(): continue  # skip

			# Refers to a known function
			elif cmd in knownAddresses_ProgramMemory:

				cmdList[ i ] = knownAddresses_ProgramMemory[ cmd ]

			# Refers to a known variable
			elif cmd in knownAddresses_DataMemory:

				cmdList[ i ] = knownAddresses_DataMemory[ cmd ]
			
			# Allocate it
			else:  
					
				if freeAddress > static_segment_end:

					raise Exception( 'Ran out of static memory' )

				newAddr = '@{}'.format( freeAddress )       # create new address

				knownAddresses_DataMemory[ cmd ] = newAddr  # add it to dict of knownAddresses_DataMemory

				cmdList[ i ] = newAddr                      # and set it

				freeAddress += 1 	# register is no longer unallocated

	print( 'Assembled program uses {} global variables. Maximum is {}.'.format( freeAddress - static_segment_start, static_segment_size ) )

	if freeAddress > static_segment_end:

		# print( 'Assembled program exceeds static segment size by {}'.format( freeAddress - static_segment_end ) )
		print( 'Assembled program exceeds maximum number global variables' )

	return cmdList


def translateInstructions( cmdList ):

	''' Translate assembly instructions to binary '''

	for i in range( len( cmdList ) ):

		#
		cmd_s = cmdList[ i ]
		cmd_b = None


		# A instruction
		if cmd_s[0] == '@':

			opcode = '0'
			addr = int( cmd_s[ 1 : ] )
			addr = _toBinary( N_BITS - 1, addr )
			cmd_b = opcode + addr


		# C instruction
		else:
			
			opcode = '1'
			nUnusedBits = ( N_BITS - 16 )  # 16 bits used to encode opcode(1), dest(3), comp( 2 + 1 + 6 ), jmp(3)
			header = opcode + '1' * nUnusedBits
			
			dest, comp, jmp = [ None ] * 3

			if '=' in cmd_s and ';' in cmd_s:
				dest, comp, jmp = re.split( '=|;', cmd_s )

			elif '=' in cmd_s:
				dest, comp = re.split( '=', cmd_s )

			elif ';' in cmd_s:
				comp, jmp = re.split( ';', cmd_s )

			# print(dest, comp, jmp)

			dest = lookup_dest[dest] if dest else lookup_dest[ 'NULL' ]
			jmp = lookup_jmp[jmp] if jmp else lookup_jmp[ 'NULL' ]
			comp = lookup_comp[comp]

			cmd_b = header + comp + dest + jmp


		#
		cmdList[ i ] = cmd_b

	return cmdList


def translateCmds( cmdList ):

	''' Translate assembly to binary '''

	# cmdList = handleLabels( cmdList )
	# cmdList = handleVariables( cmdList[0], cmdList[1] )
	# binCmdList = translateInstructions( cmdList )

	# Support for programs >= 2 ^ ( N_BITS - 1 ) lines long
	cmdList = addMemoryBank_stage1( cmdList )
	cmdList = handleLabels( cmdList )
	cmdList = addMemoryBank_stage2( cmdList[0], cmdList[1] )
	cmdList = handleVariables( cmdList[0], cmdList[1] )
	binCmdList = translateInstructions( cmdList )

	return binCmdList



# -- Output --------------------------------------


def writeToOutputFile( binCmdList, outputFile ):

	''' Generate an output file containing the binary commands '''

	with open( outputFile, 'w' ) as output_file:

		firstLine = True # workaround to avoid extra blank line at end of output file, http://stackoverflow.com/a/18139440
		
		for cmd_binary in binCmdList:
				
			if firstLine: firstLine = False
			else: output_file.write( '\n' )

			output_file.write( cmd_binary )



# -- Run ------------------------------------------


def asm_to_bin( inputFile, outputFile ):

	# Read
	cmds_assembly = extractCmds( inputFile )

	# Translate
	cmds_binary = translateCmds( cmds_assembly )

	print( 'Assembled program has {} lines. Maximum is {}.'.format( len( cmds_binary ), PROGRAM_MEMORY_SIZE ) )

	# Check size
	if len( cmds_binary ) > PROGRAM_MEMORY_SIZE:

		# raise Exception( 'Assembled program exceeds maximum length by {} lines'.format( len( cmds_binary ) - PROGRAM_MEMORY_SIZE ) ) )
		# print( 'Assembled program exceeds maximum length by {} lines'.format( len( cmds_binary ) - PROGRAM_MEMORY_SIZE ) )
		print( 'Assembled program exceeds maximum length' )

	# Write
	writeToOutputFile( cmds_binary, outputFile )

	# print( 'Done' )

def genBINFile( inputDirPath ):

	fileNames = os.listdir( inputDirPath )

	for fileName in fileNames:

		if fileName[ -3 : ] == 'asm' or fileName[ -4 : ] == 'hasm':

			inputFilePath = inputDirPath + '/' + fileName

			break  # Translate only first encountered in directory

	outputFilePath = inputDirPath + '/Main.bin'

	asm_to_bin( inputFilePath, outputFilePath )
