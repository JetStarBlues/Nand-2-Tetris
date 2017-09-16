'''------------------------------ Imports ------------------------------'''

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

	debug()
	
	# if breakpoint():

	# 	clock.stop()
	# 	print( 'Breakpoint reached' )



'''------------------------------ Debug ---------------------------------'''

def breakpoint():

	# return computer.data_memory.RAM.registers[ 8000 ] == 6

	pass


def debug():

	# print( clock.currentCycle )

	print( '{} ------------'.format( computer.CPU.programCounter.register.register ) )
	print( 'SP    {}'.format( computer.data_memory.RAM.registers[ 0 ] ) )
	print( 'LCL   {}'.format( computer.data_memory.RAM.registers[ 1 ] ) )
	print( 'ARG   {}'.format( computer.data_memory.RAM.registers[ 2 ] ) )
	print( 'THIS  {}'.format( computer.data_memory.RAM.registers[ 3 ] ) )
	print( 'THAT  {}'.format( computer.data_memory.RAM.registers[ 4 ] ) )
	# print( 'GP0   {}'.format( computer.data_memory.RAM.registers[ 13 ] ) )
	# print( 'GP1   {}'.format( computer.data_memory.RAM.registers[ 14 ] ) )
	# print( 'GP2   {}'.format( computer.data_memory.RAM.registers[ 15 ] ) )
	print()

	# static 16..255
	print( 'Static' )
	for i in range( 16, 256 ):
		print( '{:<3}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) )
	print()

	# stack 256..2047
	print( 'Stack' )
	for i in range( 256, computer.data_memory.RAM.registers[ 0 ] + 1 ):
		print( '{:<4}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) )
	print()

	# heap 2048..16383
	print( 'Heap' )
	for i in range( 2048, 16384 ):
		print( '{:<5}  {}'.format( i, computer.data_memory.RAM.registers[ i ] ) )
	print()


'''----------------------------- Run -----------------------------------'''

clock.callbackRising = update
clock.run()
print( 'Program has started' )
