# ========================================================================================
# 
#  Description:
# 
#     Runs binary programs generated for the Hack computer.
#     Includes a debugger for troubleshooting.
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================


'''------------------------------ Imports ------------------------------'''

# Built ins
import os
import time

# Hack computer
from Components import *
from Assembler.disassembler import disassemble



'''------------------------------ Setup --------------------------------'''

programPath = 'Programs/Tests/Chapter_6_hardware/bin/test1_addTo.bin'
# programPath = 'Programs/Tests/Chapter_12/Main.bin'
# programPath = 'Programs/ByOthers/MarkArmbrust/Creature/modifiedCode/Main.bin'
# programPath = 'Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASchunky/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/hello/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/math/Main.bin'
# programPath = 'Programs/Demos/e06/bin/demo_eo6.bin'
# programPath = 'Programs/Demos/e06/bin/demo_eo6_color.bin'


debugPath = 'C:/Users/Janet/Desktop/Temp/DumpDebug/'

debugMode = False



'''----------------------------- Main -----------------------------------'''

computer = None
clock    = None
io       = None

startTime = 0


def setup():

	global computer
	global clock
	global io

	# Initialize computer
	computer = ComputerN_( N_BITS, DATA_MEMORY_SIZE, PROGRAM_MEMORY_SIZE )
	computer.program_memory.flash( programPath )

	# Initialize clock
	clock = Clock()

	# Setup callbacks
	if debugMode:

		clock.callbackRising = updateWithDebug

	else:

		clock.callbackRising = update

	# Initialize IO
	io = IO( N_BITS, computer.data_memory )
	io.runAsThread()


def update():

	computer.run( clock.value )  # tick

	if io.hasExited:

		clock.stop()
		print( 'See you later!' )


def start():

	global startTime

	setup()

	clock.run()
	print( 'Program has started' )

	startTime = time.time()



'''------------------------------ Debug ---------------------------------'''

instructionAddress = None


def negate( x ): return ( x ^ ( 2 ** 16 - 1 ) ) + 1


def updateWithDebug():

	global instructionAddress

	instructionAddress = computer.CPU.programCounter.read()

	update()

	# if clock.currentCycle > - 1:

	# 	debug2File()

	if breakpoint():

		clock.stop()
		# io.quitPygame()  # call crashes for some reason
		# print( 'Breakpoint reached' )
		print( 'Breakpoint reached after {} clock cycles'.format( clock.currentCycle ) )
		print( 'Took {} seconds to reach breakpoint'.format( time.time() - startTime ) )

		debug2File()


def breakpoint():

	# pass

	# Math_ex test...
	# return computer.data_memory.read( 8000 ) == 6
	# return computer.data_memory.read( 8001 ) == negate( 180 )
	# return computer.data_memory.read( 8002 ) == negate( 18000 )
	# return computer.data_memory.read( 8003 ) == negate( 18000 )
	# return computer.data_memory.read( 8004 ) == 0
	# return computer.data_memory.read( 8005 ) == 3
	# return computer.data_memory.read( 8006 ) == negate( 3000 )
	# return computer.data_memory.read( 8007 ) == 0
	# return computer.data_memory.read( 8008 ) == 3
	# return computer.data_memory.read( 8009 ) == 181
	# return computer.data_memory.read( 8010 ) == 123
	# return computer.data_memory.read( 8011 ) == 123
	# return computer.data_memory.read( 8012 ) == 27
	# return computer.data_memory.read( 8013 ) == 32767
	# return instructionAddress == 16551  # Sys.halt (position changes with recompile)

	return instructionAddress == 293  # Sys.halt (position changes with recompile)


def debug2File():

	filePath = debugPath + str( clock.currentCycle )

	sp = computer.data_memory.read( 0 )

	with open( filePath, 'w' ) as file:

		file.write( '{} ------------'.format( instructionAddress ) + '\n' )
		file.write( disassemble( computer.program_memory.read( instructionAddress ) ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'D     {}'.format( computer.CPU.D_register.read() ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'SP    {}'.format( computer.data_memory.read(  0 ) ) + '\n' )
		file.write( 'LCL   {}'.format( computer.data_memory.read(  1 ) ) + '\n' )
		file.write( 'ARG   {}'.format( computer.data_memory.read(  2 ) ) + '\n' )
		file.write( 'THIS  {}'.format( computer.data_memory.read(  3 ) ) + '\n' )
		file.write( 'THAT  {}'.format( computer.data_memory.read(  4 ) ) + '\n' )
		file.write( 'TMP0  {}'.format( computer.data_memory.read(  5 ) ) + '\n' )
		file.write( 'TMP1  {}'.format( computer.data_memory.read(  6 ) ) + '\n' )
		file.write( 'TMP2  {}'.format( computer.data_memory.read(  7 ) ) + '\n' )
		file.write( 'TMP3  {}'.format( computer.data_memory.read(  8 ) ) + '\n' )
		file.write( 'TMP4  {}'.format( computer.data_memory.read(  9 ) ) + '\n' )
		file.write( 'TMP5  {}'.format( computer.data_memory.read( 10 ) ) + '\n' )
		file.write( 'TMP6  {}'.format( computer.data_memory.read( 11 ) ) + '\n' )
		file.write( 'TMP7  {}'.format( computer.data_memory.read( 12 ) ) + '\n' )
		file.write( 'GP0   {}'.format( computer.data_memory.read( 13 ) ) + '\n' )
		file.write( 'GP1   {}'.format( computer.data_memory.read( 14 ) ) + '\n' )
		file.write( 'GP2   {}'.format( computer.data_memory.read( 15 ) ) + '\n' )
		file.write( '' + '\n' )

		# static
		file.write( 'Static' + '\n' )
		for i in range( STATIC_START, STACK_START ):
			file.write( '\t{:<3}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )

		# stack
		file.write( 'Stack' + '\n' )
		for i in range( STACK_START, sp ):
			file.write( '\t{:<4}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '\t{:<4}  .. ({})'.format( sp, computer.data_memory.read( sp ) ) + '\n' )
		file.write( '' + '\n' )

		# heap
		file.write( 'Heap' + '\n' )
		for i in range( HEAP_START, HEAP_END + 1 ):
			file.write( '\t{:<5}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )



'''----------------------------- Run -----------------------------------'''

if __name__ == '__main__':

	start()
