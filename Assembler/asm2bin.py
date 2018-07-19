# ========================================================================================
#
#  Description:
# 
#    Compiles Hack ASM (assembly) code to Hack BIN (binary) code
#
#  Attribution:
# 
#    Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
#
# ========================================================================================

'''
	Instruction - FEDCBA9876543210  // msb to lsb
	              0123456789ABCDEF  // array indexing

		F . 0  -> TECS instruction type (C if 1, @ if 0)
		E . 1  -> op
		D . 2  -> op
		C . 3  -> op
		B . 4  -> op
		A . 5  -> op
		9 . 6  -> xSel
		8 . 7  -> xSel
		7 . 8  -> ySel
		6 . 9  -> ySel
		5 . A  -> dst
		4 . B  -> dst
		3 . C  -> dst
		2 . D  -> jmp
		1 . E  -> jmp
		0 . F  -> jmp

	x/y sel
		0     D
		1     A
		2     B
		3     M

	dst
		0     NULL
		1     D
		2     A
		3     B
		4     M
		5     unused
		6     unused
		7     unused

	jmp
		0     NULL
		1     JGT
		2     JEQ
		3     JGE
		4     JLT
		5     JNE
		6     JLE
		7     JMP

'''


# == Imports =================================================

# Built ins
import re
import os
import sys

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


# -- Constants -------------------------------------

# nBits = GC.N_BITS
nBits = 16

static_segment_start = GC.STATIC_START
static_segment_end   = GC.STATIC_END
static_segment_size  = static_segment_end - static_segment_start + 1

largest_immediate = 2 ** ( nBits - 1 ) - 1
negative_one = 2 ** nBits - 1
largest_address = 2 ** 26 - 1



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

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment

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
knownAddresses_DataMemory.update( LT.globalAddresses )  # fill with global addresses

# TODO: Come up with more elegant algorithm instead of tripling every '@label'

def tripleLabels_P1( cmdList ):

	''' Allow for labels greater than largest_immediate.

			For example,

				// A = 262143  (3, 65535)
				@0
				A = !A
				@@3

				// A = 65536  (1, 0)
				@0
				NOP      // redundancy for simplicity
				@@1
				
				// A = 61234   (0, 61234)
				@4301
				A = !A
				NOP      // redundancy for simplicity
				
				// A = 555     (0, 555)
				@555
				NOP      // redundancy for simplicity
				NOP      // redundancy for simplicity

		Bit flip idea by @cadet1620
		  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Is-it-possible-to-have-programs-longer-than-32K-with-the-Hack-instruction-set-td4031378.html
	'''

	''' Allocate space '''

	cmdList2 = []

	labels = []

	# Get labels
	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		if cmd[ 0 ] == '(':

			label = cmd[ 1 : - 1 ]  # get the label

			labels.append( label )

	# Triple references
	for i in range( len( cmdList ) ):

		cmd = cmdList[ i ]

		cmdList2.append( cmd )

		if cmd[ 0 ] == '@':

			if cmd[ 1 : ] in labels:

				cmdList2.append( 'placeholder' )
				cmdList2.append( 'placeholder' )

	# Check size
	if len( cmdList2 ) > largest_address:

		raise Exception( 'Program exceeds directly addressable memory by {} instructions'.format( len( cmdList2 ) - largest_address ) )

	return cmdList2


def tripleLabels_P2( cmdList ):

	''' Compute values '''

	i = 0

	n = len( cmdList )
	
	while i < n:

		cmd = cmdList[ i ]

		if ( cmd[ 0 ] == '@'                   and
			 i < ( n - 2 )                     and
			 cmdList[ i + 1 ] == 'placeholder' and
			 cmdList[ i + 2 ] == 'placeholder' ):

			cmdList[ i + 1 ] = 'NOP'
			cmdList[ i + 2 ] = 'NOP'

			addr = int( cmd[ 1 : ] )

			if addr > largest_immediate and addr <= negative_one:

				addr ^= negative_one  # flip bits

				cmdList[ i ] = '@{}'.format( addr )

				cmdList[ i + 1 ] = 'A=!A'

			elif addr > negative_one:

				lo = addr & negative_one
				hi = addr >> 16

				if lo > largest_immediate:

					lo ^= negative_one  # flip bits

					cmdList[ i ] = '@{}'.format( lo )

					cmdList[ i + 1 ] = 'A=!A'

				else:

					cmdList[ i ] = '@{}'.format( lo )

				cmdList[ i + 2 ] = '@@{}'.format( hi )

			i += 2  # skip subsequent associated @ instructions

		i += 1

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


		# NOP instruction
		if cmd_s.upper() == 'NOP':

			opcode = LT.fxType[ 'NOP' ]
			cmd_b = '1' + opcode + '0' * 10


		# RETI instruction
		elif cmd_s.upper() == 'RETI':

			opcode = LT.fxType[ 'RETI' ]
			cmd_b = '1' + opcode + '0' * 10


		# A and AA instruction
		elif cmd_s[ 0 ] == '@':

			# AA instruction
			if cmd_s[ 1 ] == '@':

				opcode = LT.fxType[ 'AA_IMMED' ]
				addr = int( cmd_s[ 2 : ] )
				addr = toBinary( addr, 10 )
				cmd_b = '1' + opcode + addr

			else:

				addr = int( cmd_s[ 1 : ] )
				addr = toBinary( addr, nBits - 1 )
				cmd_b = '0' + addr


		# C instruction
		else:

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

			# dst=IOBus instruction
			if comp == 'IOBUS':

				opcode = LT.fxType[ 'DST_EQ_IOBUS' ]

				xSel = '00'
				ySel = '00'

			# dst=cmp;jmp instruction
			else:

				z = None

				for k,v in LT.comp.items():

					z = re.fullmatch( k, comp )

					if z:

						z = z.groups()

						if len( z ) == 0:

							xSel = '00'
							ySel = '00'

						if len( z ) == 1:

							xSel = LT.xySel[ z[ 0 ].upper() ]
							ySel = '00'

						elif len( z ) == 2:

							xSel = LT.xySel[ z[ 0 ].upper() ]
							ySel = LT.xySel[ z[ 1 ].upper() ]

						opcode = v

						break

				if z == None:

					raise Exception ( 'Unrecognized computation - {}'.format( comp ) )

			cmd_b = '1' + opcode + xSel + ySel + dest + jump


		#
		binCmdList.append( cmd_b )

	return binCmdList


def translateCmds( cmdList, debug ):

	''' Translate assembly to binary '''

	# cmdList = handleLabels( cmdList )
	# cmdList = handleVariables( cmdList )
	# binCmdList = translateInstructions( cmdList )

	# Support for programs greater than largest_immediate lines long
	cmdList    = tripleLabels_P1( cmdList )
	cmdList    = handleLabels( cmdList )
	cmdList    = handleVariables( cmdList )
	cmdList    = tripleLabels_P2( cmdList )
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
