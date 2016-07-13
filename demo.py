''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Hack computer
from Components import *



''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Initialize
computer = ComputerN_( N_BITS, RAM_SIZE, ROM_SIZE )
io = IO( N_BITS, computer.main_memory )


# Load program
computer.program_memory.flash( 'Programs/Demos/bin/demo_eo6.bin' )


# Set data bits required by program accordingly
# computer.main_memory.write( 1, toBinary( N_BITS, x ), 1, 0 )  # clk, x, write, address



''''''''''''''''''''''''''' run '''''''''''''''''''''''''''''

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