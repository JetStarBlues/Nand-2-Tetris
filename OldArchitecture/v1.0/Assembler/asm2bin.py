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

				1   -> comp, xor
				2   -> comp, bitshift
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
import Assembler.lookupTables as LT
from commonHelpers import *


# == Helpers =================================================

def debugStuff( cmdList ):

	for c in cmdList:

		print( c )

	print( '\n--\n' )

	# for k, v in knownAddresses_ProgramMemory.items(): print( k, v )
	for kv in sorted(

		knownAddresses_ProgramMemory.items(),
		key = lambda x : int( x[ 1 ][ 1 : ] ) 
	):		
		print( '{:<6}  {}'.format( kv[ 1 ], kv[ 0 ] ) )

	print( '\n--\n' )

	# for k, v in knownAddresses_DataMemory.items(): print( k, v )
	for kv in sorted(

		knownAddresses_DataMemory.items(),
		key = lambda x : int( x[ 1 ][ 1 : ] )
	):
		print( '{:<6}  {}'.format( kv[ 1 ], kv[ 0 ] ) )



# == Main ====================================================


# -- ... -------------------------------------------

nBits = GC.N_BITS

static_segment_start = GC.STATIC_START
static_segment_end   = GC.STATIC_END
static_segment_size  = static_segment_end - static_segment_start + 1

largest_immediate = 2 ** ( nBits - 1 ) - 1
negative_one = 2 ** nBits - 1



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
	# line = line.upper()              # upper case everything

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment

	if found:

		return found.group( 0 )

	else:

		return None


# Without regex (Todo) --

	# extract non commment
	# remove spaces and tabs
	# capitalize


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
knownAddresses_DataMemory.update( LT.globalAddresses )  # fill with global addresses


def doubleLabels_P1( cmdList ):

	''' Allow for labels greater than largest_immediate.
		
		For example,

			@4301
			A = !A  // A = 61234

			@555
			A = A  // redundancy for simplicity

		Idea by @cadet1620
		  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Is-it-possible-to-have-programs-longer-than-32K-with-the-Hack-instruction-set-td4031378.html
	'''

	cmdList2 = []

	labels = []

	# Get labels
	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '(':

			label = cmd[ 1 : - 1 ]  # get the label

			labels.append( label )

	# Double references
	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		cmdList2.append( cmd )

		if cmd[ 0 ] == '@':

			if cmd[ 1 : ] in labels:

				cmdList2.append( 'A=A' )

	return cmdList2


def doubleLabels_P2( cmdList ):

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '@':

			addr = cmd[ 1 : ]

			if addr.isdigit():

				addr = int( addr )

				if addr > largest_immediate:

					n_addr = addr ^ negative_one  # flip bits

					cmdList[ i ] = '@{}'.format( n_addr )

					cmdList[ i + 1 ] = 'A=!A'

	return cmdList


def handleLabels( cmdList ):

	''' Replace labels (function declarations) with integer addresses '''

	trimmedCmdList = []

	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '(':

			label = cmd[ 1 : - 1 ]  # get the label

			addr = i - len( knownAddresses_ProgramMemory )  # and the corresponding address

			knownAddresses_ProgramMemory[ '@{}'.format( label ) ] = '@{}'.format( addr )  # add it to dict of knownAddresses_ProgramMemory

		else:

			trimmedCmdList.append( cmd )  # not a label so include it

	return trimmedCmdList


def handleVariables( cmdList ):

	''' Replace variable names with integer addresses '''

	freeAddress = static_segment_start

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

	# print( 'Assembled program has {} global variables.'.format( freeAddress - static_segment_start ) )
	print( 'Assembled program has {} global variables. Maximum is {}.'.format( freeAddress - static_segment_start, static_segment_size ) )

	if freeAddress > static_segment_end:

		# print( 'Assembled program exceeds maximum number of global variables.' )
		print( 'Assembled program exceeds maximum number of global variables by {}.'.format( freeAddress - static_segment_end ) )
		# print( 'Assembled program exceeds static segment size by {}.'.format( freeAddress - static_segment_end ) )

	return cmdList


def translateInstructions( cmdList ):

	''' Translate assembly instructions to binary '''

	binCmdList = []

	for i in range( len( cmdList ) ):

		#
		cmd_s = cmdList[ i ]
		cmd_b = None


		# A instruction
		if cmd_s[0] == '@':

			opcode = '0'
			addr = int( cmd_s[ 1 : ] )
			addr = toBinary( addr, nBits - 1 )
			cmd_b = opcode + addr


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

			dest = LT.dest[ dest.upper() ] if dest else LT.dest[ 'NULL' ]
			jump = LT.jump[ jump.upper() ] if jump else LT.jump[ 'NULL' ]
			comp = LT.comp[ comp.upper() ]

			cmd_b = header + comp + dest + jump


		#
		# cmdList[ i ] = cmd_b
		binCmdList.append( cmd_b )

	# return cmdList
	return binCmdList


def translateCmds( cmdList, debug ):

	''' Translate assembly to binary '''

	# cmdList = handleLabels( cmdList )
	# cmdList = handleVariables( cmdList )
	# binCmdList = translateInstructions( cmdList )

	# Support for programs greater than largest_immediate lines long
	cmdList = doubleLabels_P1( cmdList )
	cmdList = handleLabels( cmdList )
	cmdList = handleVariables( cmdList )
	cmdList = doubleLabels_P2( cmdList )
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

	print( 'Assembled program has {} lines. Maximum is {}.'.format( len( cmds_binary ), PROGRAM_MEMORY_SIZE ) )

	# Check size
	if len( cmds_binary ) > GC.PROGRAM_MEMORY_SIZE:

		# print( 'Assembled program exceeds maximum length.' )
		print( 'Assembled program exceeds maximum length by {} lines.'.format( len( cmds_binary ) - PROGRAM_MEMORY_SIZE ) )
		# raise Exception( 'Assembled program exceeds maximum length by {} lines.'.format( len( cmds_binary ) - PROGRAM_MEMORY_SIZE ) ) )

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
