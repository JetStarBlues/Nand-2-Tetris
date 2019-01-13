# ========================================================================================
#
#  Description:
#
#    Emulates execution of binary/machine code.
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

		Emulate the Hack Computer's architecture.
		Includes a debugger for troubleshooting.

	Description:

		Cycle accurate but slow as molasses.
'''

# Imports --------------------------

# Built ins
import time
import yappi
import re

# Hack computer
import Components
from commonHelpers import *
import Assembler.disassembler as dis


# Configure computer ---------------

# binary file
programPath = ''

debugPath = 'Debug/CPUEmulator/'  # Folder where logs go

debugMode = True

runYappiProfile = False


# Setup computer -------------------

nBits = Components.N_BITS

computer = None
clock    = None
io       = None

startTime = None

instructionAddress = None
sysHaltAddress     = None


# Debug -----------------------------

def updateWithDebug():

	global instructionAddress

	instructionAddress = computer.CPU.programCounter.readDecimal()

	update()

	if breakpoint():

		clock.stop()

		# print( 'Breakpoint reached' )
		print( '\nBreakpoint reached after {} clock cycles'.format( clock.currentCycle ) )
		print( 'Took {} seconds to reach breakpoint'.format( time.time() - startTime ) )

		debug2File()

		stepMode()


def negate( x ):

	return ( x ^ ( 2 ** 16 - 1 ) ) + 1


def breakpoint():

	# return computer.halted  # assembly HALT instruction
	# return instructionAddress == sysHaltAddress
	return computer.data_memory.readDecimal( 9000 ) == 12345

	# return instructionAddress ==  #  Sys.init
	# return instructionAddress ==  #  GlobalConstants.init
	# return instructionAddress ==   #  DataMemory.init
	# return instructionAddress == 6558   #  Math.init
	# return instructionAddress == 27656  #  Font.init  # 40 sec
	# return instructionAddress ==   #  Colors.init
	# return instructionAddress ==   #  GFX.init
	# return instructionAddress ==   #  Keyboard.init
	# return instructionAddress ==   #  Mouse.init
	# return instructionAddress ==   #  Sys.runProgram

	# return instructionAddress == 1938   #  DataMemory.alloc

	return False


def debug2File():

	filePath = debugPath + str( clock.currentCycle )

	sp          = computer.data_memory.readDecimal( 0 )
	instruction = computer.program_memory.read( instructionAddress )

	with open( filePath, 'w' ) as file:

		file.write( 'Instruction' + '\n' )
		file.write( '\taddress      {}'.format( instructionAddress ) + '\n' )
		file.write( '\tinstruction  {}'.format( instruction ) + '\n' )
		file.write( '\t             {}'.format( dis.disassemble( instruction ) ) + '\n' )
		file.write( '\n' )

		file.write( 'Registers' + '\n' )
		file.write( '\tD     {}'.format( computer.CPU.D_register.readDecimal() ) + '\n' )
		file.write( '\n' )

		file.write( 'Memory' + '\n' )
		file.write( '\tSP    {}'.format( computer.data_memory.readDecimal(  0 ) ) + '\n' )
		file.write( '\tLCL   {}'.format( computer.data_memory.readDecimal(  1 ) ) + '\n' )
		file.write( '\tARG   {}'.format( computer.data_memory.readDecimal(  2 ) ) + '\n' )
		file.write( '\tTHIS  {}'.format( computer.data_memory.readDecimal(  3 ) ) + '\n' )
		file.write( '\tTHAT  {}'.format( computer.data_memory.readDecimal(  4 ) ) + '\n' )
		file.write( '\tTMP0  {}'.format( computer.data_memory.readDecimal(  5 ) ) + '\n' )
		file.write( '\tTMP1  {}'.format( computer.data_memory.readDecimal(  6 ) ) + '\n' )
		file.write( '\tTMP2  {}'.format( computer.data_memory.readDecimal(  7 ) ) + '\n' )
		file.write( '\tTMP3  {}'.format( computer.data_memory.readDecimal(  8 ) ) + '\n' )
		file.write( '\tTMP4  {}'.format( computer.data_memory.readDecimal(  9 ) ) + '\n' )
		file.write( '\tTMP5  {}'.format( computer.data_memory.readDecimal( 10 ) ) + '\n' )
		file.write( '\tTMP6  {}'.format( computer.data_memory.readDecimal( 11 ) ) + '\n' )
		file.write( '\tTMP7  {}'.format( computer.data_memory.readDecimal( 12 ) ) + '\n' )
		file.write( '\tGP0   {}'.format( computer.data_memory.readDecimal( 13 ) ) + '\n' )
		file.write( '\tGP1   {}'.format( computer.data_memory.readDecimal( 14 ) ) + '\n' )
		file.write( '\tGP2   {}'.format( computer.data_memory.readDecimal( 15 ) ) + '\n' )
		file.write( '\n' )

		# static
		file.write( 'Static' + '\n' )
		for i in range( Components.STATIC_START, Components.STACK_START ):
			file.write( '\t{:<3}  {}'.format( i, computer.data_memory.readDecimal( i ) ) + '\n' )
		file.write( '\n' )

		# stack
		file.write( 'Stack' + '\n' )
		for i in range( Components.STACK_START, sp ):
			file.write( '\t{:<4}  {}'.format( i, computer.data_memory.readDecimal( i ) ) + '\n' )
		file.write( '\t{:<4}  .. ({})'.format( sp, computer.data_memory.readDecimal( sp ) ) + '\n' )
		file.write( '\n' )

		# heap
		file.write( 'Heap' + '\n' )
		for i in range( Components.HEAP_START, Components.HEAP_END + 1 ):
			file.write( '\t{:<5}  {}'.format( i, computer.data_memory.readDecimal( i ) ) + '\n' )
		file.write( '\n' )

		# io
		file.write( 'IO' + '\n' )
		file.write( '\tscreen' + '\n' )
		for i in range( Components.IO_START, Components.KEYBOARD_MEMORY_MAP ):
			file.write( '\t\t{:<5}  {}'.format( i, computer.data_memory.readDecimal( i ) ) + '\n' )
		file.write( '\tkeyboard' + '\n' )
		for i in range( Components.KEYBOARD_MEMORY_MAP, Components.MOUSE_MEMORY_MAP ):
			file.write( '\t\t{:<5}  {}'.format( i, computer.data_memory.readDecimal( i ) ) + '\n' )
		file.write( '\tmouse' + '\n' )
		for i in range( Components.MOUSE_MEMORY_MAP, Components.IO_END + 1 ):
			file.write( '\t\t{:<5}  {}'.format( i, computer.data_memory.readDecimal( i ) ) + '\n' )
		file.write( '\n' )


def stepMode():

	print( "\nEntered manual step mode..." )
	print( "Type 'n' to step, and 'q' to quit" )
	print( "To step multiple, type 'nX' where X is nSteps wish to advance" )

	skipAhead = 0

	def _smUpdate():

		global instructionAddress

		instructionAddress = computer.CPU.programCounter.readDecimal()

		step()

		clock.currentCycle += 1  # ...

		debug2File()

	while True:

		if skipAhead > 0:

			_smUpdate()

			skipAhead -= 1

			continue


		uInput = input()

		if uInput == 'q':

			print( 'Exited manual step mode\n' )

			break

		else:

			nxt = re.match( r'n(\d*)', uInput )  # uInput is n or nX

			if nxt:

				_smUpdate()

				if nxt.group( 1 ):

					skipAhead = int( nxt.group( 1 ) ) - 1


# Computer --------------------------

def setup():

	global computer
	global clock
	global io

	# Initialize computer
	computer = Components.ComputerN_(

		nBits,
		Components.DATA_MEMORY_SIZE,
		Components.PROGRAM_MEMORY_SIZE
	)

	# Setup ROM
	computer.load( programPath )

	# Initialize clock
	clock = Components.Clock()

	# Setup callbacks
	if debugMode:

		clock.callbackRising = updateWithDebug

	else:

		clock.callbackRising = update

	# Initialize IO
	io = Components.IO( nBits, computer.data_memory )


def tick():

	computer.run( clock.value )

	io.updateScreen()


def step():  # manual tick

	computer.run( 1 )

	io.updateScreen()


def update():

	# print( 'PC', instructionAddress )

	tick()

	# Handle exit via IO
	if io.hasExited:

		if debugMode:

			debug2File()

		clock.stop()
		print( 'See you later!' )

		# Profile... temp
		if runYappiProfile:

			yappi.get_func_stats().print_all()


	# Stop running when reach Sys.halt (TODO)



# Run -------------------------------

def run( programPath_, sysHaltAddress_ = None ):

	global programPath
	global startTime
	global sysHaltAddress

	# Specify program
	if programPath_:
		
		programPath = programPath_

	# Spceify location of Sys.halt
	if sysHaltAddress_:

		sysHaltAddress = sysHaltAddress_

		if debugMode:

			print( 'Sys.halt at {}'.format( sysHaltAddress_ ) )

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
