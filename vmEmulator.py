# ========================================================================================
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
	Purpose:

		Emulation at a usable execution speed.

	Description:

		Faster than emulating assembly code.
		Infact, does not emulate nor use the Hack computer architecture.
		Instead it executes the VM code using your machine's processor architecture.

		While running assembly (and in turn binary) code is cycle accurate,
		it is too slow in emulation (see runProgram.py).
		The best I could squeeze out was around 7K instructions per second. Compare
		this to the speed of execution in dedicated hardware. Even a 'slow' 25Mhz clock
		would put this performance to shame.

		I'm sure there are optimizations to be made that can improve the performance
		of the assembly/binary emulation. If you have any ideas, be sure to share
		them because the best case scenario is for the binary emulator to execute at a
		usable speed. Till then, this exists as an inbetween.
'''

'''
	TODO - Make if faster!

	Official emulator attains speed by using OS libraries written in Java instead of Jack.
	Is this a possible course of action?
	E.g.
	  - Sys.wait
	  - GFX.drawPixel
'''


# Imports --------------------------

# Built ins
import re
import time
import os
from multiprocessing import Array, Process
import threading

# Hack computer (will use only the Clock and IO modules)
import Components


# Configure computer ---------------

# VMX file containing all necessary program code
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/pong/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/cadet/Creature/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/gav/GASchunky/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/gav/GASscroller/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/gav/GASboing/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/temp_delete/Main.vmx'
programPath = '../colorImages/lp/Main.vmx'
# programPath = '../colorImages/sunset/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/hello/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/sys/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/string/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/memory/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/math/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/keyboard/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/gfx/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/array/Main.vmx'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/includesOfIncludes/Main.vmx'
# programPath = 'Programs/ByOthers/MarkArmbrust/Creature/modifiedCode/Main.vmx'
# programPath = 'Programs/ByOthers/GavinStewart/Games&Demos/GASscroller/modifiedCode/Main.vmx'


debugPath = 'C:/Users/Janet/Desktop/Temp/DumpDebug2/'  # Folder where logs go

debugMode = False

useMultiprocessing = False  # Gains realized only if screen fps > 3



# Setup computer -------------------

N_BITS = 16

PC = 0
PC_prev = 0
PC_jump = False

RAM = None
if useMultiprocessing:

	RAM = Array( 'i', 2 ** 16 )  # Slower than 'list', but allows IO to be run in separate process

else:

	RAM = [ 0 ] * ( 2 ** 16 )

ROM = []  # Psuedo ROM, loaded with VM code

clock = None
io    = None

startTime = None
sysHalt = None

io_process = None

yieldToExternal = False  # Suspend tick


# Setup stack ----------------------

SP   = 0
LCL  = 1
ARG  = 2
THIS = 3
THAT = 4
TEMP = 5
# GP   = 13
STATIC = 16

static_segment_start = 16
static_segment_end   = 255


# IO Helpers ------------------------

class RAMWrapper():

	def __init__( self, ram ):

		self.ram = ram

	def read( self, address ):

		return self.ram[ address ]

	def write( self, clk, x, write, address ):

		if clk == 1 and write == 1:

			self.ram[ address ] = x


# ALU Helpers -----------------------

negativeOne = 2 ** N_BITS - 1

largestInt = 2 ** ( N_BITS - 1 ) - 1

def trim( x ):

	return x & negativeOne  # discard overflow bits

def negate( x ):

	return trim( ( x ^ negativeOne ) + 1 )  # twos complement

def isNegative( x ):

	return x > largestInt


# VM Helpers ------------------------

# unaryOps = [ 'not', 'neg' ]
# binaryOps = [ 'and', 'or', 'add', 'sub', 'xor', 'shiftL', 'shiftR' ]
# comparisonOps = [ 'eq', 'gt', 'lt', 'gte', 'lte', 'ne' ]
# operations = [ unaryOps + binaryOps + comparisonOps ]
unaryOps = set( [ 'not', 'neg' ] )
# binaryOps = set( [ 'and', 'or', 'add', 'sub', 'xor', 'shiftL', 'shiftR' ] )
binaryOps = set( [ 'and', 'or', 'add', 'sub', 'xor', 'shiftL', 'shiftR', 'mult', 'div' ] )
comparisonOps = set( [ 'eq', 'gt', 'lt', 'gte', 'lte', 'ne' ] )
operations = unaryOps | binaryOps | comparisonOps  # Set marginally faster to lookup than list

addressLookup = {}
staticLookup = {}


# VM instructions -------------------

def executeInstruction( cmd ):

	cmdType = cmd[ 0 ]

	if cmdType == 'push':

		push( cmd[1], cmd[2], cmd )

	elif cmdType == 'pop':

		pop( cmd[1], cmd[2], cmd )

	elif cmdType in operations:

		operation( cmdType )

	elif cmdType == 'goto':

		goto( cmd[1] )

	elif cmdType == 'if-goto':

		ifgoto( cmd[1] )

	elif cmdType == 'call':

		call( cmd[1], cmd[2] )

	elif cmdType == 'return':

		ret()

	elif cmdType == 'label':

		label( cmd[1] )

	elif cmdType == 'function':

		function( cmd[1], cmd[2] )

	else:

		raise Exception( "Don't know how to execute the command - {}".format( cmd ) )


def push( seg, index, cmd ):

	addr = RAM[ SP ]

	if seg == 'constant':

		RAM[ addr ] = index

	elif seg == 'pointer':

		if index == 0: RAM[ addr ] = RAM[ THIS ]

		else:          RAM[ addr ] = RAM[ THAT ]

	elif seg == 'static':

		RAM[ addr ] = RAM[ staticLookup[ cmd[3] ] ]

	elif seg == 'temp':

		RAM[ addr ] = RAM[ TEMP + index ]

	elif seg == 'argument':

		RAM[ addr ] = RAM[ RAM[ ARG ] + index ]

	elif seg == 'local':

		RAM[ addr ] = RAM[ RAM[ LCL ] + index ]

	elif seg == 'this':

		RAM[ addr ] = RAM[ RAM[ THIS ] + index ]

	elif seg == 'that':

		RAM[ addr ] = RAM[ RAM[ THAT ] + index ]

	else:

		raise Exception( 'Unknown segment - {}'.format( seg ) )

	# Update SP
	RAM[ SP ] += 1


def pop( seg, index, cmd ):

	addr = RAM[ SP ] - 1
	value = RAM[ addr ]

	if seg == 'pointer':

		if index == 0: RAM[ THIS ] = value
		else:          RAM[ THAT ] = value

	elif seg == 'static':

		RAM[ staticLookup[ cmd[3] ] ] = value

	elif seg == 'temp':

		RAM[ TEMP + index ] = value

	elif seg == 'argument':

		RAM[ RAM[ ARG ] + index ] = value

	elif seg == 'local':

		RAM[ RAM[ LCL ] + index ] = value

	elif seg == 'this':

		RAM[ RAM[ THIS ] + index ] = value

	elif seg == 'that':

		RAM[ RAM[ THAT ] + index ] = value

	else:

		raise Exception( 'Unknown segment - {}'.format( seg ) )

	# Update SP
	RAM[ SP ] -= 1


def operation( op ):

	if op in unaryOps:

		addr = RAM[ SP ] - 1
		a = RAM[ addr ]

		if op == 'not':

			RAM[ addr ] = a ^ negativeOne  # flip bits

		elif op == 'neg':

			RAM[ addr ] = negate( a )

	elif op in binaryOps:

		addr_a = RAM[ SP ] - 2
		addr_b = RAM[ SP ] - 1
		a = RAM[ addr_a ]
		b = RAM[ addr_b ]
		value = None

		if op == 'and':

			value = a & b

		elif op == 'or':

			value = a | b

		elif op == 'xor':

			value = a ^ b

		elif op == 'shiftL':

			value = trim( a << b )

		elif op == 'shiftR':

			value = a >> b  # logical shift

		elif op == 'add':

			value = trim( a + b )

		elif op == 'sub':

			value = trim( a + negate( b ) )

		elif op == 'mult':

			value = trim( a * b )

		elif op == 'div':

			# value = a // b  # floor

			# Divide using absolutes and add signs after
			if a > largestInt:

				a = negate( a )

				if b > largestInt:

					b = negate( b )

					value = a // b

				else:

					value = negate( a // b )

			else:

				if b > largestInt:

					b = negate( b )

					value = negate( a // b )

				else:

					value = a // b


		RAM[ addr_a ] = value

		# Update SP
		RAM[ SP ] -= 1

	elif op in comparisonOps:

		addr_a = RAM[ SP ] - 2
		addr_b = RAM[ SP ] - 1
		a = RAM[ addr_a ]
		b = RAM[ addr_b ]
		value = None

		diff = trim( a + negate( b ) )
		zr = diff == 0
		ng = diff > largestInt

		if op == 'eq':

			value = zr

		elif op == 'ne':

			value = not( zr )

		else:

			# For gt, gte, lt, lte see discussion here,
			#  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Greater-or-less-than-when-comparing-numbers-with-different-signs-td4031520.html

			oppositeSigns = ( a > largestInt ) ^ ( b > largestInt )
			aIsNeg = a > largestInt

			if op == 'gt':

				# value = not( zr or ng )

				if oppositeSigns:  # opposite signs and,

					if aIsNeg:     # a is negative

						value = False

					else:          # a is zero or positive

						value = True

				else:  # same signs

					value = not( zr or ng )

			elif op == 'gte':

				# value = not( ng )

				if oppositeSigns:  # opposite signs and,

					if aIsNeg:     # a is negative

						value = False

					else:          # a is zero or positive

						value = True

				else:  # same signs

					value = not( ng )

			elif op == 'lt':

				# value = ng

				if oppositeSigns:  # opposite signs and,

					if aIsNeg:     # a is negative

						value = True

					else:          # a is zero or positive

						value = False

				else:  # same signs

					value = ng

			elif op == 'lte':

				# value = zr or ng

				if oppositeSigns:  # opposite signs and,

					if aIsNeg:     # a is negative

						value = True

					else:          # a is zero or positive

						value = False

				else:  # same signs

					value = zr or ng

		if value:

			RAM[ addr_a ] = negativeOne  # 111111 so that !True = 00000

		else:

			RAM[ addr_a ] = 0

		# Update SP
		RAM[ SP ] -= 1


def goto( loc ):

	global PC
	global PC_jump

	PC = addressLookup[ loc ]

	PC_jump = True


def ifgoto( loc ):

	global PC
	global PC_jump

	addr = RAM[ SP ] - 1
	value = RAM[ addr ]

	if value != 0:
	# if value:

		PC = addressLookup[ loc ]

		PC_jump = True

	# Update SP
	RAM[ SP ] -= 1


def call( fxName, nArgs ):

	addr = RAM[ SP ]

	# Save return position
	RAM[ addr ] = PC + 1
	addr += 1

	# Save segment pointers
	RAM[ addr ] = RAM[ LCL ]
	addr += 1
	RAM[ addr ] = RAM[ ARG ]
	addr += 1
	RAM[ addr ] = RAM[ THIS ]
	addr += 1
	RAM[ addr ] = RAM[ THAT ]
	addr += 1

	# Set ARG
	RAM[ ARG ] = RAM[ SP ] - nArgs

	# Set LCL
	RAM[ LCL ] = addr

	# Set SP
	RAM[ SP ] = addr

	# Goto function
	goto( fxName )


def ret():

	global PC
	global PC_jump

	global yieldToExternal

	# Save current LCL
	curLCL = RAM[ LCL ]

	# Save return address
	retAddr = RAM[ curLCL - 5 ]

	# Copy return value into arg0
	addr_a = RAM[ ARG ]
	addr_r = RAM[ SP ] - 1

	RAM[ addr_a ] = RAM[ addr_r ]

	# Reposition SP for caller (to just after return value)
	RAM[ SP ] = addr_a + 1

	# Restore segment pointers of caller
	curLCL -= 1
	RAM[ THAT ] = RAM[ curLCL ]
	curLCL -= 1
	RAM[ THIS ] = RAM[ curLCL ]
	curLCL -= 1
	RAM[ ARG ] = RAM[ curLCL ]
	curLCL -= 1
	RAM[ LCL ] = RAM[ curLCL ]

	# Jump to return position
	PC = retAddr

	PC_jump = True

	yieldToExternal = False  # temp...


def label( loc ): pass


def function( fxName, nLocals ):

	global yieldToExternal

	# Init locals to zeros
	for i in range( nLocals ):

		addr = RAM[ LCL ] + i
		RAM[ addr ] = 0

	RAM[ SP ] += nLocals

	# If exists, execute python equivalent
	if fxName in OSWrappers:

		yieldToExternal = True
		OSWrappers[ fxName ]()


# OS Wrappers -----------------------

def Sys_wait():

	# Retrieve args ---
	argBase = RAM[ ARG ]
	duration = RAM[ argBase ]


	# Subroutine body ---

	'''
		if ( duration <= 0 ) {

			Sys.error( 1 );
			// Sys.raiseException( "Sys.wait duration must be greater than zero" );
		}
	'''

	if duration <= 0:

		print( "ERROR: Sys.wait duration must be greater than zero" )

		# Halt program
		haltOnError()

		return

	# print( "About to sleep for {} ms".format( duration ) )
	time.sleep( duration / 1000 )  # convert msec to sec


	# Return ---
	push( 'constant', 0, None )
	ret()


def GFX_drawPixel():

	# Retrieve args ---
	argBase = RAM[ ARG ]
	x = RAM[ argBase ]
	y = RAM[ argBase + 1 ]


	# Subroutine body ---

	'''
		var int screenIdx, wordIdx;
		var int curWord;

		// A bit slow to do this check for every pixel drawn!
		if ( ( y < 0 ) | ( y >= height ) | ( x < 0 ) | ( x >= width ) ) {

			Sys.error( 7 );
			// Sys.raiseException( "Pixel coordinates are out of bounds" );
		}

		screenIdx = ( y * wordsPerRow ) + ( x >> pixelsPerWordL2 );
		screenIdx += screenBaseAddr;

		curWord = DataMemory.peek( screenIdx );

		wordIdx = x % pixelsPerWord;

		/**/
		// 1bit color mode ----------------------------

		if ( fgColor ) {

			DataMemory.poke( screenIdx, curWord | pixelMask[ wordIdx ] );  // set bit to 1
		}
		else {

			DataMemory.poke( screenIdx, curWord & ( ~ pixelMask[ wordIdx ] ) );  // set bit to 0
		}/**/


		/*
		// 4bit color mode ----------------------------
		
		DataMemory.poke(

			screenIdx,
			colorMask[ fgColor ][ wordIdx ] | ( curWord & ( ~ pixelMask4[ wordIdx ] ) )
		);*/
	'''

	# Static indices depend on the order they are listed in 'GFX.jack'
	colorBitMode    = RAM[ staticLookup[ 'GFX_0' ] ]
	screenBaseAddr  = RAM[ staticLookup[ 'GFX_1' ] ]
	wordsPerRow     = RAM[ staticLookup[ 'GFX_2' ] ]
	pixelsPerWord   = RAM[ staticLookup[ 'GFX_3' ] ]
	pixelsPerWordL2 = RAM[ staticLookup[ 'GFX_4' ] ]
	fgColor         = RAM[ staticLookup[ 'GFX_5' ] ]

	# print( "Got {} of value {}".format( 'colorBitMode   ', colorBitMode    ) )
	# print( "Got {} of value {}".format( 'screenBaseAddr ', screenBaseAddr  ) )
	# print( "Got {} of value {}".format( 'wordsPerRow    ', wordsPerRow     ) )
	# print( "Got {} of value {}".format( 'pixelsPerWord  ', pixelsPerWord   ) )
	# print( "Got {} of value {}".format( 'pixelsPerWordL2', pixelsPerWordL2 ) )
	# print( "Got {} of value {}".format( 'fgColor        ', fgColor         ) )

	width = 512
	height = 256

	pixelMask = (

		0b1000000000000000,
		0b0100000000000000,
		0b0010000000000000,
		0b0001000000000000,
		0b0000100000000000,
		0b0000010000000000,
		0b0000001000000000,
		0b0000000100000000,
		0b0000000010000000,
		0b0000000001000000,
		0b0000000000100000,
		0b0000000000010000,
		0b0000000000001000,
		0b0000000000000100,
		0b0000000000000010,
		0b0000000000000001
	)
	pixelMask4 = (

		0b1111000000000000,
		0b0000111100000000,
		0b0000000011110000,
		0b0000000000001111
	)
	colorMask = (

		(
			0b0000000000000000,
			0b0000000000000000,
			0b0000000000000000,
			0b0000000000000000
		),
		(
			0b0001000000000000,
			0b0000000100000000,
			0b0000000000010000,
			0b0000000000000001
		),
		(
			0b0010000000000000,
			0b0000001000000000,
			0b0000000000100000,
			0b0000000000000010
		),
		(
			0b0011000000000000,
			0b0000001100000000,
			0b0000000000110000,
			0b0000000000000011
		),
		(
			0b0100000000000000,
			0b0000010000000000,
			0b0000000001000000,
			0b0000000000000100
		),
		(
			0b0101000000000000,
			0b0000010100000000,
			0b0000000001010000,
			0b0000000000000101
		),
		(
			0b0110000000000000,
			0b0000011000000000,
			0b0000000001100000,
			0b0000000000000110
		),
		(
			0b0111000000000000,
			0b0000011100000000,
			0b0000000001110000,
			0b0000000000000111
		),
		(
			0b1000000000000000,
			0b0000100000000000,
			0b0000000010000000,
			0b0000000000001000
		),
		(
			0b1001000000000000,
			0b0000100100000000,
			0b0000000010010000,
			0b0000000000001001
		),
		(
			0b1010000000000000,
			0b0000101000000000,
			0b0000000010100000,
			0b0000000000001010
		),
		(
			0b1011000000000000,
			0b0000101100000000,
			0b0000000010110000,
			0b0000000000001011
		),
		(
			0b1100000000000000,
			0b0000110000000000,
			0b0000000011000000,
			0b0000000000001100
		),
		(
			0b1101000000000000,
			0b0000110100000000,
			0b0000000011010000,
			0b0000000000001101
		),
		(
			0b1110000000000000,
			0b0000111000000000,
			0b0000000011100000,
			0b0000000000001110
		),
		(
			0b1111000000000000,
			0b0000111100000000,
			0b0000000011110000,
			0b0000000000001111
		)
	)


	screenIdx = None
	wordIdx   = None
	curWord   = None

	# A bit slow to do this check for every pixel drawn!
	if ( ( y < 0 ) | ( y >= height ) | ( x < 0 ) | ( x >= width ) ):

		print( "ERROR: Pixel coordinates are out of bounds ( {}, {} )".format( x, y ) )

		# Halt program
		haltOnError()

		return

	screenIdx = trim( trim( y * wordsPerRow ) + ( x >> pixelsPerWordL2 ) )
	screenIdx = trim( screenIdx + screenBaseAddr )

	curWord = RAM[ screenIdx ]

	# Equivalent of 'x % pixelsPerWord'
	# Assumes, 'x' is zero or positive, 'pixelsPerWord' is positive
	wordIdx = trim( x + negate( trim( pixelsPerWord * ( x // pixelsPerWord ) ) ) )  #  x % pixelsPerWord


	# If fast enough, do colorBitMode check here so that less manual work when switching modes

	'''
	# 1bit color mode ----------------------------

	if ( fgColor ):

		RAM[ screenIdx ] = curWord | pixelMask[ wordIdx ]  # set bit to 1

	else:

		RAM[ screenIdx ] = curWord & ( pixelMask[ wordIdx ] ^ negativeOne )  # set bit to 0

	'''

	''''''
	# 4bit color mode ----------------------------
	
	RAM[ screenIdx ] = colorMask[ fgColor ][ wordIdx ] | ( curWord & ( pixelMask4[ wordIdx ] ^ negativeOne ) )
	''''''


	# Return ---
	push( 'constant', 0, None )
	ret()

OSWrappers = {
	
	'Sys.wait'      : Sys_wait,
	'GFX.drawPixel' : GFX_drawPixel  # Atm about 1 second faster
}


# Load program ----------------------

cmdPattern = '''
	^                # from beginning of string
	.*?              # select all characters until
	(?=\/\/|[\r\n])  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )

def extractCmd( line ):

	found = re.search( cmdPattern, line )  # select everything that is not a comment

	if found:

		cmd = found.group( 0 )
		cmd = cmd.strip()  # remove leading and trailing whitespace
		return cmd.split( ' ' )  # split on spaces

	else:

		return None

def extractProgram( inputFilePath ):

	addr = 0

	curFx = ''
	curClass = ''

	freeAddress = static_segment_start

	with open( inputFilePath, 'r' ) as file:

		for line in file:

			cmd = extractCmd( line )

			if cmd:

				cmdType = cmd[0]

				if cmdType == 'function':

					curFx = cmd[1]
					curClass = curFx.split( '.' )[0]

					addressLookup[ cmd[1] ] = addr

					cmd[2] = int( cmd[2] )  # cast nLocals to int

					ROM.append( cmd )

				elif cmdType == 'label' or cmdType == 'goto' or cmdType == 'if-goto':

					# Make labels globally unique

					newLabel = '{}_{}'.format( curFx, cmd[1] )

					if cmdType == 'label':

						addressLookup[ newLabel ] = addr

					ROM.append( [ cmdType, newLabel ] )

				elif cmdType == 'push' or cmdType == 'pop':

					cmd[2] = int( cmd[2] )  # cast index to int

					if cmd[1] == 'static':

						# Make static references globally unique

						refName =  '{}_{}'.format( curClass, cmd[2] )

						if refName not in staticLookup:

							if freeAddress <= static_segment_end:

								staticLookup[ refName ] = freeAddress

								freeAddress += 1

							else:

								raise Exception( "Ran out of static space" )

						cmd += [ refName ]

					ROM.append( cmd )

				elif cmdType == 'call':

					cmd[2] = int( cmd[2] )  # cast nArgs to int

					ROM.append( cmd )

				else:

					ROM.append( cmd )

			addr += 1


# Debug -----------------------------

def updateWithDebug():

	update()

	if breakpoint():

		clock.stop()
		# io_process.terminate()
		# print( 'Breakpoint reached' )
		print( 'Breakpoint reached after {} clock cycles'.format( clock.currentCycle ) )
		print( 'Took {} seconds to reach breakpoint'.format( time.time() - startTime ) )

		debug2File()


def breakpoint():

	# pass
	# return PC == addressLookup[ 'GFX.fillRect' ]
	return PC == sysHalt
	# return clock.currentCycle == 384381


def debug2File():

	filePath = debugPath + str( clock.currentCycle )

	with open( filePath, 'w' ) as file:

		file.write( '{} ------------'.format( PC_prev ) + '\n' )
		file.write( ' '.join( map( str, ROM[ PC_prev ] ) ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'SP    {}'.format( RAM[  0 ] ) + '\n' )
		file.write( 'LCL   {}'.format( RAM[  1 ] ) + '\n' )
		file.write( 'ARG   {}'.format( RAM[  2 ] ) + '\n' )
		file.write( 'THIS  {}'.format( RAM[  3 ] ) + '\n' )
		file.write( 'THAT  {}'.format( RAM[  4 ] ) + '\n' )
		file.write( 'TMP0  {}'.format( RAM[  5 ] ) + '\n' )
		file.write( 'TMP1  {}'.format( RAM[  6 ] ) + '\n' )
		file.write( 'TMP2  {}'.format( RAM[  7 ] ) + '\n' )
		file.write( 'TMP3  {}'.format( RAM[  8 ] ) + '\n' )
		file.write( 'TMP4  {}'.format( RAM[  9 ] ) + '\n' )
		file.write( 'TMP5  {}'.format( RAM[ 10 ] ) + '\n' )
		file.write( 'TMP6  {}'.format( RAM[ 11 ] ) + '\n' )
		file.write( 'TMP7  {}'.format( RAM[ 12 ] ) + '\n' )
		file.write( 'GP0   {}'.format( RAM[ 13 ] ) + '\n' )
		file.write( 'GP1   {}'.format( RAM[ 14 ] ) + '\n' )
		file.write( 'GP2   {}'.format( RAM[ 15 ] ) + '\n' )
		file.write( '' + '\n' )

		# static 16..255
		file.write( 'Static' + '\n' )
		for i in range( 16, 256 ):
			file.write( '\t{:<3}  {}'.format( i, RAM[ i ] ) + '\n' )
		file.write( '' + '\n' )

		# stack 256..2047
		sp = RAM[ 0 ]
		file.write( 'Stack' + '\n' )
		for i in range( 256, sp ):
		# for i in range( 256, 2048 ):
			file.write( '\t{:<4}  {}'.format( i, RAM[ i ] ) + '\n' )
		file.write( '\t{:<4}  .. ({})'.format( sp, RAM[ sp ] ) + '\n' )
		file.write( '' + '\n' )

		# heap 2048..16383
		# heapEnd = 16384
		heapEnd = 32762  # 4bit color mode
		file.write( 'Heap' + '\n' )
		for i in range( 2048, heapEnd ):
			file.write( '\t{:<5}  {}'.format( i, RAM[ i ] ) + '\n' )
		file.write( '' + '\n' )


def dumpROMnAddresses():

	# Dump ROM
	with open( debugPath + 'romDump', 'w' ) as file:
		for e in ROM:
			file.write( ' '.join( map( str, e ) ) + '\n' )

	# Dump addresses
	with open( debugPath + 'addressDump', 'w' ) as file:

		# Dump generated label addresses
		for kv in sorted( addressLookup.items(), key = lambda x : x[1] ):
			file.write( '{:<5} - {}\n'.format( kv[1], kv[0] ) )
		file.write( '\n\n' )

		# Dump generated static addresses
		for kv in sorted( staticLookup.items(), key = lambda x : x[1] ):
			file.write( '{:<3} - {}\n'.format( kv[1], kv[0] ) )


# Computer --------------------------

def haltOnError():

	global PC
	global yieldToExternal

	PC = sysHalt  # end program

	yieldToExternal = True  # prevent tick

	if debugMode:

		debug2File()

	update()


def setup():

	global clock
	global io
	global startTime
	global sysHalt

	# Setup RAM
	RAM[ SP   ] = 256
	RAM[ LCL  ] = 256
	RAM[ ARG  ] = 256
	RAM[ THIS ] = 9999
	RAM[ THAT ] = 9999

	# Setup ROM
	startTime = time.time()
	extractProgram( programPath )
	print( 'Completed ROM flash. Took {} seconds.'.format( time.time() - startTime ) )

	if debugMode:

		# Remove existing logs
		for f in os.listdir( debugPath ): os.remove( debugPath + f )

		# Dump ROM and addresses
		dumpROMnAddresses()

	# Retrive location
	sysHalt = addressLookup[ 'Sys.halt' ]

	# Initialize clock
	clock = Components.Clock()

	# Setup callbacks
	if debugMode:
		clock.callbackRising = updateWithDebug
	else:
		clock.callbackRising = update

	# Initialize IO
	io = Components.IO( N_BITS, RAMWrapper( RAM ) )


def tick():

	global PC
	global PC_prev
	global PC_jump

	PC_prev = PC  # helps with debugging

	# Fetch instruction
	instruction = ROM[ PC ]
	# print( '{} - {}'.format( PC, instruction ) )

	# Execute instruction
	executeInstruction( instruction )

	# Increment PC
	if PC_jump == False:

		PC += 1

	else:

		PC_jump = False


def update():

	if not yieldToExternal:

		tick()

	# Handle exit via IO
	if ( useMultiprocessing and not io_process.is_alive() ) or io.hasExited :

		if debugMode:

			debug2File()

		clock.stop()
		print( 'See you later!' )

	# Stop running when reach Sys.halt
	if PC == sysHalt:

		# TODO, none of these actions seem to lower processor use...

		clock.stop()
		io.maxFps = 0  # stop screen refresh

		print( 'Sys.halt reached' )

		# Am I really killing the clock and IO threads with the above??
		main_thread = threading.main_thread()

		for t in threading.enumerate():

			print( t.getName(), t.isAlive() )  # Nope, they are still alive! TODO, how to properly stop them


	#Hmmm
	# if PC == addressLookup[ 'Main.main' ]:

	# 	print( 'Main thread is alive', threading.main_thread().isAlive() )  # main dead...



# Run -------------------------------

if __name__ == '__main__':

	''' For whatever reason, multiprocessing.Process needs to be
	    started from within this block.
	    See, https://stackoverflow.com/a/42617612/
	'''

	# Setup
	setup()

	# Start IO
	if useMultiprocessing:

		io_process = Process(
			target = io.initPygame,
			name   = 'io_process'
		)
		io_process.start()

	else:

		io.runAsThread()

	# Start clock
	clock.run()

	print( 'Program has started' )

	startTime = time.time()
