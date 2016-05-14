''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys

# Computer files
sys.path.append('../Modules')
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _3__clock import *
from _4__flipFlops import *


''''''''''''''''''''''''' helpers '''''''''''''''''''''''''

def toString(array):
	return ''.join( map(str, array) )

def toDecimal(bitSeq):
	return int(bitSeq, 2)

def toBinary(N, x):
	return bin(x)[2:].zfill(N)


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

import re

def parseAsm( inputFile, outputFile ):

	# commands = []   # output to txt file instead??

	with open( inputFile, encoding='utf-8' ) as input_file, \
		 open( outputFile, mode='w', encoding='utf-8' ) as output_file:

			firstLine = True # workaround to avoid extra blank line at end of output file, http://stackoverflow.com/a/18139440
			
			for a_line in input_file:

				a_line = a_line.rstrip()   # remove trailing whitespace and carriage return

				# do the thing
				cmd_symbolic = extractCmd( a_line )
				# print(cmd_symbolic)
				cmd_binary = translateCmd( cmd_symbolic )

				# write to output file
				if cmd_binary: 
					# print( cmd_binary )
					
					if firstLine: firstLine = False
					else: output_file.write( '\n' )

					output_file.write( cmd_binary )


pattern = '''
	^   		# beginning of string
	[^\/]   	# that does not start with a comment
	.*?  		# select all characters until,
	(?=\/\/|$)  # reach start of a comment or the string's end
'''
pattern = re.compile( pattern, re.X )

def extractCmd( line ):
	
	''' Extract commands'''

	line = line.replace(' ', '')   # remove whitespaces
	line = line.replace('\t', '')  # remove tabs
	line = line.upper()			   # upper case everything

	found = re.search( pattern, line )

	if found != None:
		return found.group(0)
	else:
		return None


def translateCmd( cmd_s ):

	''' Convert to binary '''

	if cmd_s:

		cmd_b = None

		# A instruction
		if cmd_s[0] == '@':
			addr = int( cmd_s[1:] )
			cmd_b = toBinary( 16, addr )

		# C instruction
		else:
			header = '011'
			
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

		return cmd_b



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
	'JGT'   : '001',
	'JEQ'   : '010',
	'JGE'   : '011',
	'JLT'   : '100',
	'JNE'   : '101',
	'JLE'   : '110',
	'JMP'  : '111'
}








parseAsm( 'test1.hasm', 'test1.bin' )