''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys
import re

# Computer files
sys.path.append('../../Components')
from _0__globalConstants import *


''''''''''''''''''''''''' helpers '''''''''''''''''''''''''

def toBinary(N, x):
	return bin(x)[2:].zfill(N)


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''


### --- Lookup tables ------------------------------

lookup_comp = {

	# zx, nx, zy, ny, f, no
	'0'   : '0101010',
	'1'   : '0111111',
	'-1'  : '0111010',
	'D'   : '0001100',
	'A'   : '0110000',
	'!D'  : '0001101',
	'!A'  : '0110001',
	'-D'  : '0001111',
	'-A'  : '0110011',
	'D+1' : '0011111',
	'A+1' : '0110111',
	'D-1' : '0001110',
	'A-1' : '0110010',
	'D+A' : '0000010',
	# 'A+D' : '0000010',  #hmm..., can I add this?
	'D-A' : '0010011',
	'A-D' : '0000111',
	'D&A' : '0000000',
	'D|A' : '0010101',
	'M'   : '1110000',
	'!M'  : '1110001',
	'-M'  : '1110011',
	'M+1' : '1110111',
	'M-1' : '1110010',
	'D+M' : '1000010',
	# 'M+D' : '1000010',  #hmm..., can I add this?
	'D-M' : '1010011',
	'M-D' : '1000111',
	'D&M' : '1000000',
	'D|M' : '1010101'
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

	'@R0'      : '@0',
	'@R1'      : '@1',
	'@R2'      : '@2',
	'@R3'      : '@3',
	'@R4'      : '@4',
	'@R5'      : '@5',
	'@R6'      : '@6',
	'@R7'      : '@7',
	'@R8'      : '@8',
	'@R9'      : '@9',
	'@R10'     : '@10',
	'@R11'     : '@11',
	'@R12'     : '@12',
	'@R13'     : '@13',
	'@R14'     : '@14',
	'@R15'     : '@15'
}



### --- Extraction ---------------------------------


# select everything that is not a comment
cmdPattern = '''
	^   		# from beginning of string
	[^\/]   	# that does not start with a comment
	.*?  		# select all characters until,
	(?=\/\/|$)  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )


def extractCmd( line ):
	
	''' Extract symbolic command from line of source code '''

	line = line.replace(' ', '')   # remove whitespaces
	line = line.replace('\t', '')  # remove tabs
	line = line.upper()            # upper case everything

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment

	if found != None:
		return found.group(0)
	else:
		return None


def extractCmds( inputFile ):

	''' Extract symbolic commands from source code '''

	commands = []

	with open( inputFile, encoding='utf-8' ) as input_file:
		
		for a_line in input_file:

			a_line = a_line.rstrip()   # remove trailing whitespace and carriage return

			cmd_symbolic = extractCmd( a_line )

			if cmd_symbolic:
				commands.append( cmd_symbolic )

	return commands



### --- Translation ---------------------------------


def handle_Labels( cmdList ):

	''' Replace labels with integer addresses '''

	trimmedCmdList = []

	knownAddresses_ROM = {}

	for i in range( len( cmdList ) ):

		if cmdList[i][0] == '(':

			label = cmdList[i][1:-1]    # get the label

			ROM_addr = i + 1            # and the corresponding ROM address

			knownAddresses_ROM[ '@' + label ] = '@' + str( ROM_addr )   # add it to dict of knownAddresses_ROM

		else:

			trimmedCmdList.append( cmdList[i] )   # not a label so include it


	return( trimmedCmdList, knownAddresses_ROM )


def handle_Variables( cmdList, knownAddresses_ROM ):

	''' Replace variable names with integer addresses '''

	freeAddress = 16

	knownAddresses_RAM = {}
	knownAddresses_RAM.update( lookup_globalAddresses )  # fill with global addresses
	

	for i in range( len( cmdList ) ):

		if cmdList[i][0] == '@':

			# Is the address an integer? ---

			try:
				int( cmdList[i][1:] )
			

			except ValueError:

				# No? Must be a variable.			
			
				# Check known variables ---

				try:
					cmdList[i] = knownAddresses_ROM[ cmdList[i] ]

				except KeyError:

					try:
						cmdList[i] = knownAddresses_RAM[ cmdList[i] ]


					# Otherwise, create a new address ---	
					
					except KeyError:					
					

						newAddr = '@' + str( freeAddress )          # create new address

						knownAddresses_RAM[ cmdList[i] ] = newAddr  # add it to dict of knownAddresses_RAM

						cmdList[i] = newAddr                        # and set it

						freeAddress += 1 	# register is no longer unallocated


	return cmdList


def translate_Instructions( cmdList ):

	''' Translate symbolic instructions to binary '''

	for i in range( len( cmdList ) ):

		#
		cmd_s = cmdList[i]
		cmd_b = None


		# A instruction
		if cmd_s[0] == '@':
			addr = int( cmd_s[1:] )
			cmd_b = toBinary( 16, addr )


		# C instruction
		else:
			header = '111'
			
			dest, comp, jmp = [None] * 3

			if '=' in cmd_s and ';' in cmd_s:
				dest, comp, jmp = re.split( '=|;', cmd_s )

			elif '=' in cmd_s:
				dest, comp = re.split( '=', cmd_s )

			elif ';' in cmd_s:
				comp, jmp = re.split( ';', cmd_s )

			# print(dest, comp, jmp)

			dest = lookup_dest[dest] if dest else lookup_dest['NULL']
			jmp = lookup_jmp[jmp] if jmp else lookup_jmp['NULL']
			comp = lookup_comp[comp]

			cmd_b = header + comp + dest + jmp


		#
		cmdList[i] = cmd_b


	return cmdList


def translateCmds( cmdList ):

	''' Translate symbolic commands to binary '''

	cmdList = handle_Labels( cmdList )
	cmdList = handle_Variables( cmdList[0], cmdList[1] )
	binCmdList = translate_Instructions( cmdList )

	return binCmdList



### --- Output -----------------------------------


def writeToOutputFile( binCmdList, outputFile ):

	''' generate an output file containing the binary commands '''

	with open( outputFile, mode='w', encoding='utf-8' ) as output_file:

			firstLine = True # workaround to avoid extra blank line at end of output file, http://stackoverflow.com/a/18139440
			
			for cmd_binary in binCmdList:
					
				if firstLine: firstLine = False
				else: output_file.write( '\n' )

				output_file.write( cmd_binary )



## --- Run -------------------------------------


def asm_to_bin( inputFile, outputFile ):

	''' Translate the symbolic code in inputFile to binary code,
	     and generate an outputFile containing the translated code '''

	cmds_symbolic = extractCmds( inputFile )
	cmds_binary = translateCmds( cmds_symbolic )
	writeToOutputFile( cmds_binary, outputFile )



''''''''''''''''''''''''''' run '''''''''''''''''''''''''''''

# asm_to_bin( 'test1.hasm', 'bin/test.bin' )


files = [
	'test1',
	'test2',
	'test3',
	'test4',
	'test5',
	'test6',
	'fill',
	'mult'
]
for file in files:
	print(file)
	in_ = file + '.hasm'
	out_ = 'bin/' + file + '.bin'
	asm_to_bin( in_, out_ )