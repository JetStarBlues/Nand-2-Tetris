'''------------------------------ Imports ------------------------------'''

# Built ins
import os

# Hack computer
from Components import *



'''------------------------------ Setup --------------------------------'''

# programPath = 'Programs/Tests/Chapter_12/Main.bin'
# programPath = 'Programs/ByOthers/MarkArmbrust/Creature/Main.bin'
# programPath = 'Programs/ByOthers/GavinStewart/GASchunky/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/hello_ex/Main.bin'
programPath = '../tempNotes/MyCompilerOut/OS_standalone/math_ex/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/math/Main.bin'
# programPath = 'Programs/Demos/bin/demo_eo6.bin'
# programPath = 'Programs/Demos/bin/demo_eo6_color.bin'

debugMode = True



'''----------------------------- Main -----------------------------------'''

# Initialize computer
computer = ComputerN_( N_BITS, DATA_MEMORY_SIZE, PROGRAM_MEMORY_SIZE )
computer.program_memory.flash( programPath )

# Initialize IO
io = IO( N_BITS, computer.data_memory )

# Initialize clock
clock = Clock()


def update():

	computer.run( clock.value )

	if io.hasExited:

		clock.stop()
		print( 'See you later!' )


	if debugMode:

		# debug()
		debug2File()
		

		if breakpoint():

			clock.stop()
			# io.quitPygame()  # call crashes for some reason
			print( 'Breakpoint reached' )



'''------------------------------ Debug ---------------------------------'''

def breakpoint():

	# return computer.data_memory.RAM.registers[ 8000 ] == 6
	# return computer.data_memory.RAM.registers[ 4 ] == 9999

	pass


def debug():

	# print( clock.currentCycle )

	print( '{} ------------'.format( computer.CPU.programCounter.register.register ) )
	print( '' )

	print( 'SP    {}'.format( computer.data_memory.RAM.registers[ 0 ] ) )
	print( 'LCL   {}'.format( computer.data_memory.RAM.registers[ 1 ] ) )
	print( 'ARG   {}'.format( computer.data_memory.RAM.registers[ 2 ] ) )
	print( 'THIS  {}'.format( computer.data_memory.RAM.registers[ 3 ] ) )
	print( 'THAT  {}'.format( computer.data_memory.RAM.registers[ 4 ] ) )
	print( 'GP0   {}'.format( computer.data_memory.RAM.registers[ 13 ] ) )
	print( 'GP1   {}'.format( computer.data_memory.RAM.registers[ 14 ] ) )
	print( 'GP2   {}'.format( computer.data_memory.RAM.registers[ 15 ] ) )
	print( '' )

	# static 16..255
	print( 'Static' )
	for i in range( 16, 256 ):
		print( '{:<3}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) )
	print( '' )

	# stack 256..2047
	print( 'Stack' )
	for i in range( 256, computer.data_memory.RAM.registers[ 0 ] + 1 ):
		print( '{:<4}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) )
	print( '' )

	# heap 2048..16383
	print( 'Heap' )
	for i in range( 2048, 16384 ):
		print( '{:<5}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) )
	print( '' )


debugPath = 'C:/Users/Janet/Desktop/Temp/DumpDebug/'

def debug2File():

	filePath = debugPath + str( clock.currentCycle )

	with open( filePath, 'w' ) as file:

		file.write( '{} ------------'.format( computer.CPU.programCounter.register.register ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'SP    {}'.format( computer.data_memory.RAM.registers[ 0 ] ) + '\n' )
		file.write( 'LCL   {}'.format( computer.data_memory.RAM.registers[ 1 ] ) + '\n' )
		file.write( 'ARG   {}'.format( computer.data_memory.RAM.registers[ 2 ] ) + '\n' )
		file.write( 'THIS  {}'.format( computer.data_memory.RAM.registers[ 3 ] ) + '\n' )
		file.write( 'THAT  {}'.format( computer.data_memory.RAM.registers[ 4 ] ) + '\n' )
		file.write( 'GP0   {}'.format( computer.data_memory.RAM.registers[ 13 ] ) + '\n' )
		file.write( 'GP1   {}'.format( computer.data_memory.RAM.registers[ 14 ] ) + '\n' )
		file.write( 'GP2   {}'.format( computer.data_memory.RAM.registers[ 15 ] ) + '\n' )
		file.write( '' + '\n' )

		# static 16..255
		file.write( 'Static' + '\n' )
		for i in range( 16, 256 ):
			file.write( '{:<3}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) + '\n' )
		file.write( '' + '\n' )

		# stack 256..2047
		file.write( 'Stack' + '\n' )
		for i in range( 256, computer.data_memory.RAM.registers[ 0 ] + 1 ):
			file.write( '{:<4}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) + '\n' )
		file.write( '' + '\n' )

		# heap 2048..16383
		file.write( 'Heap' + '\n' )
		for i in range( 2048, 16384 ):
			file.write( '{:<5}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) + '\n' )
		file.write( '' + '\n' )



'''----------------------------- Run -----------------------------------'''

# Remove existing logs
if debugMode:
	for f in os.listdir( debugPath ): os.remove( debugPath + f )

# Setup callbacks
clock.callbackRising = update

# Start
clock.run()
print( 'Program has started' )
