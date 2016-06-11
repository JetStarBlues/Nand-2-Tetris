''' =========================================================
               ComputerN_( N, RAM_size, ROM_size )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Hack computer tests
from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )
clock = Clock()
fails = FailLogger()
count = 0

N = 16
computer = ComputerN_( N, 2**16, 2**15 )
screen = Screen( computer.main_memory )

computer.load( KnownValues.pathTo_kv_4 + 'test8_fill.bin' )


def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		pass

	elif count <= 100:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock			


def record():
	pass



''''''''''''''''''''''''''' run '''''''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	update( clock.value )

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
def start():
	clock.run()
