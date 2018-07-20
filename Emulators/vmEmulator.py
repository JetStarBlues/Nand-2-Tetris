# ========================================================================================
#
#  Description:
#
#    Emulates execution of VM code.
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

		Faster than emulating binary code.
		Infact, does not emulate nor use the Hack Computer's architecture.
		Instead it executes the VM code using your machine's processor's architecture.

		While running binary code is cycle accurate,
		it is too slow in emulation (see cpuEmulator.py).

		I'm sure there are optimizations to be made that can improve the performance
		of the binary/CPU emulation. If you have any ideas, be sure to share
		them because the best case scenario is for the binary emulator to execute at a
		usable speed. Till then, this exists as an inbetween.
'''


# Imports --------------------------

# Built ins
import re
import time
import os
import threading
from multiprocessing import Array, Process
import yappi

# Hack computer
import Components
from commonHelpers import *
from .pythonNBitArithmetic import *


# Configure computer ---------------

# VMX file containing all necessary program code
programPath = ''

debugPath = 'VMEmulatorDebug/'  # Folder where logs go

debugMode = False

useMultiprocessing = False  # Gains realized only if screen fps > 3

runYappiProfile = False


# Setup computer -------------------

nBits = Components.N_BITS

ALU = NBitArithmetic( nBits )

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


static_segment_start = Components.STATIC_START
static_segment_end   = Components.STATIC_END
stack_segment_start  = Components.STACK_END
heap_segment_start   = Components.HEAP_START
heap_segment_end     = Components.HEAP_END


# Setup pointers -------------------

SP   = 0
LCL  = 1
ARG  = 2
THIS = 3
THAT = 4
TEMP = 5
# GP   = 13
STATIC = 16


# IO Helpers ------------------------

class RAMWrapper():

	def __init__( self, ram ):

		self.ram = ram

	def read( self, address ):

		return self.ram[ address ]

	def write( self, clk, x, write, address ):

		if clk == 1 and write == 1:

			self.ram[ address ] = x


# VM Helpers ------------------------

# unaryOps = [ 'not', 'neg' ]
# binaryOps = [ 'and', 'or', 'add', 'sub', 'xor', 'lsl', 'lsr' ]
# comparisonOps = [ 'eq', 'gt', 'lt', 'gte', 'lte', 'ne' ]
# operations = [ unaryOps + binaryOps + comparisonOps ]
unaryOps = set( [ 'not', 'neg' ] )
binaryOps = set( [ 'and', 'or', 'add', 'sub', 'xor', 'lsl', 'lsr', 'mul', 'div' ] )
comparisonOps = set( [ 'eq', 'gt', 'lt', 'gte', 'lte', 'ne' ] )
operations = unaryOps | binaryOps | comparisonOps  # Set marginally faster to lookup than list

addressLookup = {}
staticLookup = {}


# VM instructions -------------------

def executeInstruction( cmd ):

	cmdType = cmd[ 0 ]

	if cmdType == 'push':

		push( cmd[ 1 ], cmd[ 2 ], cmd )

	elif cmdType == 'pop':

		pop( cmd[ 1 ], cmd[ 2 ], cmd )

	elif cmdType in operations:

		operation( cmdType )

	elif cmdType == 'goto':

		goto( cmd[ 1 ] )

	elif cmdType == 'if-goto':

		ifgoto( cmd[ 1 ] )

	elif cmdType == 'call':

		call( cmd[ 1 ], cmd[ 2 ] )

	elif cmdType == 'return':

		ret()

	elif cmdType == 'label':

		label( cmd[ 1 ] )

	elif cmdType == 'function':

		function( cmd[ 1 ], cmd[ 2 ] )

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

		RAM[ addr ] = RAM[ staticLookup[ cmd[ 3 ] ] ]

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

	# if RAM[ SP ] >= heap_segment_start:

	# 	raiseException( 'Stack overflow' )


def pop( seg, index, cmd ):

	addr = RAM[ SP ] - 1
	value = RAM[ addr ]

	if seg == 'pointer':

		if index == 0: RAM[ THIS ] = value
		else:          RAM[ THAT ] = value

	elif seg == 'static':

		RAM[ staticLookup[ cmd[ 3 ] ] ] = value

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

			RAM[ addr ] = ALU._not( a )

		elif op == 'neg':

			RAM[ addr ] = ALU._neg( a )

	elif op in binaryOps:

		addr_a = RAM[ SP ] - 2
		addr_b = RAM[ SP ] - 1
		a = RAM[ addr_a ]
		b = RAM[ addr_b ]
		value = None

		if op == 'and':

			value = ALU._and( a, b )

		elif op == 'or':

			value = ALU._or( a, b )

		elif op == 'xor':

			value = ALU._xor( a, b )

		elif op == 'lsl':

			value = ALU._lsl( a, b )

		elif op == 'lsr':

			value = ALU._lsr( a, b )

		elif op == 'add':

			value = ALU._add( a, b )

		elif op == 'sub':

			value = ALU._sub( a, b )

		elif op == 'mul':

			value = ALU._mul( a, b )

		elif op == 'div':

			value = ALU._div( a, b )


		RAM[ addr_a ] = value

		# Update SP
		RAM[ SP ] -= 1

	elif op in comparisonOps:

		addr_a = RAM[ SP ] - 2
		addr_b = RAM[ SP ] - 1
		a = RAM[ addr_a ]
		b = RAM[ addr_b ]
		value = None

		if op == 'eq':

			value = ALU._eq( a, b )

		elif op == 'ne':

			value = ALU._ne( a, b )

		elif op == 'gt':

			value = ALU._gt( a, b )

		elif op == 'gte':

			value = ALU._gte( a, b )

		elif op == 'lt':

			value = ALU._lt( a, b )

		elif op == 'lte':

			value = ALU._lte( a, b )


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

	# Set ARG pointer
	RAM[ ARG ] = RAM[ SP ] - nArgs

	# Set LCL pointer
	RAM[ LCL ] = addr

	# Set SP
	RAM[ SP ] = addr

	# Goto function
	goto( fxName )


def ret():

	global PC
	global PC_jump

	global yieldToExternal

	# Save current LCL pointer
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

	# print( 'curFx - ', fxName )

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

# Sys ---
def Sys_wait():

	# Retrieve args ---
	argBase = RAM[ ARG ]
	duration = RAM[ argBase ]


	# Subroutine body ---

	'''
		if ( duration <= 0 ) {

			Sys.error( 1 );
			// Sys.raiseException( 'Sys.wait duration must be greater than zero' );
		}
	'''

	if duration <= 0:

		print( 'ERROR: Sys.wait duration must be greater than zero' )

		# Halt program
		haltOnError()

		return

	# print( 'About to sleep for {} ms'.format( duration ) )
	time.sleep( duration / 1000 )  # convert msec to sec


	# Return ---
	push( 'constant', 0, None )
	ret()


# ---
OSWrappers = {

	'Sys.wait'      : Sys_wait
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

				cmdType = cmd[ 0 ]

				if cmdType == 'function':

					curFx = cmd[ 1 ]
					curClass = curFx.split( '.' )[ 0 ]

					addressLookup[ cmd[ 1 ] ] = addr

					cmd[ 2 ] = int( cmd[ 2 ] )  # cast nLocals to int

					ROM.append( cmd )

				elif cmdType == 'label' or cmdType == 'goto' or cmdType == 'if-goto':

					# Make labels globally unique

					newLabel = '{}_{}'.format( curFx, cmd[ 1 ] )

					if cmdType == 'label':

						addressLookup[ newLabel ] = addr

					ROM.append( [ cmdType, newLabel ] )

				elif cmdType == 'push' or cmdType == 'pop':

					cmd[ 2 ] = int( cmd[ 2 ] )  # cast index to int

					if cmd[ 1 ] == 'static':

						# Make static references globally unique

						if len( cmd ) == 4:  # 'push/pop static index className' vs 'push/pop static index'

							className = cmd[ 3 ]

						else:

							className = curClass

						refName = '{}_{}'.format( className, cmd[ 2 ] )

						if refName not in staticLookup:

							if freeAddress <= static_segment_end:

								staticLookup[ refName ] = freeAddress

								freeAddress += 1

							else:

								raise Exception( 'Ran out of static space' )

						if len( cmd ) == 4:  # 'push/pop static index className' vs 'push/pop static index'

							cmd[ 3 ] = refName

						else:

							cmd += [ refName ]

					ROM.append( cmd )

				elif cmdType == 'call':

					cmd[ 2 ] = int( cmd[ 2 ] )  # cast nArgs to int

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

		# static
		file.write( 'Static' + '\n' )
		for i in range( static_segment_start, stack_segment_start ):
			file.write( '\t{:<3}  {}'.format( i, RAM[ i ] ) + '\n' )
		file.write( '' + '\n' )

		# stack
		sp = RAM[ 0 ]
		file.write( 'Stack' + '\n' )
		for i in range( stack_segment_start, sp ):
			file.write( '\t{:<4}  {}'.format( i, RAM[ i ] ) + '\n' )
		file.write( '\t{:<4}  .. ({})'.format( sp, RAM[ sp ] ) + '\n' )
		file.write( '' + '\n' )

		# heap
		file.write( 'Heap' + '\n' )
		for i in range( heap_segment_start, heap_segment_end + 1 ):
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
		for kv in sorted( addressLookup.items(), key = lambda x : x[ 1 ] ):
			file.write( '{:<5} - {}\n'.format( kv[ 1 ], kv[ 0 ] ) )
		file.write( '\n\n' )

		# Dump generated static addresses
		for kv in sorted( staticLookup.items(), key = lambda x : x[ 1 ] ):
			file.write( '{:<3} - {}\n'.format( kv[ 1 ], kv[ 0 ] ) )


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

	#
	if not Components.PERFORMANCE_MODE:

		raise Exception( 'The VM Emulator only works when GC.PERFORMANCE_MODE is True' )

	# Setup RAM
	RAM[ SP   ] = 256
	RAM[ LCL  ] = 256
	RAM[ ARG  ] = 256
	RAM[ THIS ] = 9999
	RAM[ THAT ] = 9999

	# Setup ROM
	startTime = time.time()
	extractProgram( programPath )
	print( 'Completed ROM flash. Took {0:.2f} seconds.'.format( time.time() - startTime ) )

	if debugMode:

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
	io = Components.IO( nBits, RAMWrapper( RAM ) )

	# Time it
	startTime = time.time()


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

	''' Kinda hacky, workaround for different clocks.
	    Make IO screen updates run on CPU clock.
	'''
	io.updateScreen()


def update():

	if not yieldToExternal:

		tick()

	# Handle exit via IO
	if io.hasExited or ( useMultiprocessing and not io_process.is_alive() ):

		if debugMode:

			debug2File()

		clock.stop()
		print( 'See you later!' )

		# Profile... temp
		if runYappiProfile:

			yappi.get_func_stats().print_all()

	# Stop running when reach Sys.halt
	if PC == sysHalt:

		# Stop clock
		clock.stop()

		# Stop (lower) screen update
		io.maxFps = 1  # lowest can go is 1 FPS

		print( 'Sys.halt reached. Took {0:.2f} seconds.'.format( time.time() - startTime ) )

		# Profile... temp
		if runYappiProfile:

			yappi.get_func_stats().print_all()



# Run -------------------------------

def run( programPath_ ):

	global programPath

	# Specify program
	if programPath_:
		
		programPath = programPath_ 

	# Setup
	setup()

	# Profile... temp
	if runYappiProfile:

		yappi.start()

	# Start IO
	io.runAsThread()

	# Start clock
	clock.run()

	print( 'Program has started' )

	startTime = time.time()


if __name__ == '__main__':

	''' For whatever reason, multiprocessing.Process needs to be
	    started from within this block.
	    See, https://stackoverflow.com/a/42617612/
	'''

	# Setup
	setup()

	# Profile... temp
	if runYappiProfile:

		yappi.start()

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
