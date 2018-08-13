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

# Hack computer
import Components
from commonHelpers import *
import Assembler.disassembler as dis


# Configure computer ---------------

# binary file
programPath = ''

debugPath = 'Debug/CPUEmulator/'  # Folder where logs go

debugMode = True

# printCurrentInstruction = False

runYappiProfile = False


# Setup computer -------------------

nBits = Components.N_BITS

computer = None
clock    = None
io       = None

startTime = None

instructionAddress = None


# Debug -----------------------------

def updateWithDebug():

	global instructionAddress

	instructionAddress = computer.CPU.programCounter.readDecimal()

	update()

	if breakpoint():

		clock.stop()

		# print( 'Breakpoint reached' )
		print( 'Breakpoint reached after {} clock cycles'.format( clock.currentCycle ) )
		print( 'Took {} seconds to reach breakpoint'.format( time.time() - startTime ) )

		debug2File()


def negate( x ):

	return ( x ^ ( 2 ** 16 - 1 ) ) + 1


def breakpoint( fx = None ):

	return computer.halted  # assembly HALT instruction
	# return instructionAddress == 16551  # Sys.halt (position changes with recompile)

	# return False


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


def update():

	# global instructionAddress

	# if printCurrentInstruction:

	# 	instructionAddress = computer.CPU.programCounter.readDecimal()

	# 	print( 'PC', instructionAddress )

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

def run( programPath_ ):

	global programPath
	global startTime

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
