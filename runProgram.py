'''------------------------------ Imports ------------------------------'''

# Hack computer
from Components import *



'''------------------------------- Main -------------------------------'''

# Initialize
computer = ComputerN_( N_BITS, DATA_MEMORY_SIZE, PROGRAM_MEMORY_SIZE )
io = IO( N_BITS, computer.data_memory )


# Load program
# computer.program_memory.flash( 'Programs/Tests/Chapter_12/Main.bin' )
# computer.program_memory.flash( 'Programs/ByOthers/MarkArmbrust/Creature/Main.bin' )
# computer.program_memory.flash( 'Programs/ByOthers/GavinStewart/GASchunky/Main.bin' )
computer.program_memory.flash( '../tempNotes/MyCompilerOut/OS_standalone/hello/Main.bin' )
# computer.program_memory.flash( 'Programs/Demos/bin/demo_eo6.bin' )
# computer.program_memory.flash( 'Programs/Demos/bin/demo_eo6_color.bin' )


# Set data bits required by program accordingly
# computer.main_memory.write( 1, toBinary( N_BITS, x ), 1, 0 )  # clk, x, write, address



'''-------------------------------- Run --------------------------------'''

def update():

	computer.run( clock.value )

	if io.hasExited: 
		clock.stop()
		print( 'See you later!' )


# Setup and start clock
clock = Clock()
clock.callbackRising = update
clock.run()

print( 'Program has started' )