# ========================================================================================
#
# Description:
#	Compiles Hack ASM (assembly) code to Hack BIN (binary) code
#
# Attribution:
# 	Code by www.jk-quantized.com
#
# Redistributions and use of this code in source and binary forms must retain
# the above attribution notice and this condition.
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
	'A+D'  : '110000010',  # hmm..., can I add this?
	'D-A'  : '110010011',
	'A-D'  : '110000111',
	'D&A'  : '110000000',
	'A&D'  : '110000000',  # hmm..., can I add this?
	'D|A'  : '110010101',
	'A|D'  : '110010101',  # hmm..., can I add this?
	'M'    : '111110000',
	'!M'   : '111110001',
	'-M'   : '111110011',
	'M+1'  : '111110111',
	'M-1'  : '111110010',
	'D+M'  : '111000010',
	'M+D'  : '111000010',  # hmm..., can I add this?
	'D-M'  : '111010011',
	'M-D'  : '111000111',
	'D&M'  : '111000000',
	'M&D'  : '111000000',  # hmm..., can I add this?
	'D|M'  : '111010101',
	'M|D'  : '111010101',  # hmm..., can I add this?

	'D<<A' : '010000000',
	'D<<M' : '011000000',
	'D>>A' : '000000000',
	'D>>M' : '001000000',
	'D^A'  : '100000000',
	'A^D'  : '100000000',  # hmm..., can I add this?
	'D^M'  : '101000000',	
	'M^D'  : '101000000'   # hmm..., can I add this?	
}

lookup_dest = {
	
	# d3, d2, d1
	'NULL' : '000',
	'M'    : '001',
	'D'    : '010',
	'MD'   : '011',
	'A'    : '100',
	'AM'   : '101',
	'AD'   : '110',
	'AMD'  : '111'
}

lookup_jmp = {
	
	# j3, j2, j1
	'NULL' : '000',
	'JGT'  : '001',
	'JEQ'  : '010',
	'JGE'  : '011',
	'JLT'  : '100',
	'JNE'  : '101',
	'JLE'  : '110',
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

static_segment_end = 255  # 16..255



# -- Extraction -------------------------------------


# Select everything that is not a comment
cmdPattern = '''
	^                # from beginning of string
	[^\/]            # that does not start with a comment
	.*?              # select all characters until,
	(?=\/\/|[\r\n])  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )


def extractCmd( line ):
	
	''' Extract symbolic command from line of source code '''

	line = line.replace( ' ', '' )   # remove whitespaces
	line = line.replace( '\t', '' )  # remove tabs
	line = line.upper()              # upper case everything

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment

	if found != None:

		return found.group( 0 )

	else:

		return None


def extractCmds( inputFile ):

	''' Extract symbolic commands from source code '''

	commands = []

	with open( inputFile, 'r' ) as input_file:
		
		for line in input_file:

			cmd = extractCmd( line )

			if cmd:

				commands.append( cmd )

	return commands



# -- Translation -------------------------------------


def handle_Labels( cmdList ):

	''' Replace labels with integer addresses '''

	trimmedCmdList = []

	knownAddresses_ROM = {}

	for i in range( len( cmdList ) ):

		if cmdList[ i ][ 0 ] == '(':

			label = cmdList[ i ][ 1 : - 1 ]    # get the label

			ROM_addr = i - len( knownAddresses_ROM )    # and the corresponding ROM address

			knownAddresses_ROM[ '@' + label ] = '@' + str( ROM_addr )   # add it to dict of knownAddresses_ROM

		else:

			trimmedCmdList.append( cmdList[ i ] )   # not a label so include it

	return( trimmedCmdList, knownAddresses_ROM )


def handle_Variables( cmdList, knownAddresses_ROM ):

	''' Replace variable names with integer addresses '''

	freeAddress = 16  # 16..255 (static)

	knownAddresses_RAM = {}
	knownAddresses_RAM.update( lookup_globalAddresses )  # fill with global addresses
	

	for i in range( len( cmdList ) ):

		if cmdList[ i ][ 0 ] == '@':

			# Is the address an integer? ---

			try:
				int( cmdList[ i ][ 1 : ] )
			

			except ValueError:

				# No? Must be a variable.			
			
				# Check known variables ---

				try:
					cmdList[ i ] = knownAddresses_ROM[ cmdList[ i ] ]

				except KeyError:

					try:
						cmdList[ i ] = knownAddresses_RAM[ cmdList[ i ] ]


					# Otherwise, create a new address ---	
					
					except KeyError:					
					
						if freeAddress > static_segment_end:

							raise Exception( 'Ran out of static memory' )

						newAddr = '@' + str( freeAddress )          # create new address

						knownAddresses_RAM[ cmdList[ i ] ] = newAddr  # add it to dict of knownAddresses_RAM

						cmdList[ i ] = newAddr                        # and set it

						freeAddress += 1 	# register is no longer unallocated

	return cmdList


def translate_Instructions( cmdList ):

	''' Translate symbolic instructions to binary '''

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

	''' Translate symbolic commands to binary '''

	cmdList = handle_Labels( cmdList )
	cmdList = handle_Variables( cmdList[0], cmdList[1] )
	binCmdList = translate_Instructions( cmdList )

	return binCmdList



# -- Output --------------------------------------


def writeToOutputFile( binCmdList, outputFile ):

	''' generate an output file containing the binary commands '''

	with open( outputFile, 'w' ) as output_file:

		firstLine = True # workaround to avoid extra blank line at end of output file, http://stackoverflow.com/a/18139440
		
		for cmd_binary in binCmdList:
				
			if firstLine: firstLine = False
			else: output_file.write( '\n' )

			output_file.write( cmd_binary )



# -- Run ------------------------------------------


def asm_to_bin( inputFile, outputFile ):

	''' Translate the symbolic code in inputFile to binary code,
	     and generate an outputFile containing the translated code '''

	# Read
	cmds_assembly = extractCmds( inputFile )

	# Check size
	exceedsSizeLimit = len( cmds_assembly ) - 2 ** ( N_BITS - 1 )
	if exceedsSizeLimit > 0:

		raise Exception( 'Assembled program exceeds maximum length by {} lines'.format( exceedsSizeLimit ) )

	# Translate
	cmds_binary = translateCmds( cmds_assembly )

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
