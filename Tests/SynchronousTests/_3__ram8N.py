''' =========================================================
                RAM8N_( N, clk, x, write, address )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )
clock = Clock()
fails = FailLogger()

k_idx = -2

k = k_ram8_16
N = 16
ram = RAM8N_( N )


def update(clk):

	global k_idx
	
	# increment
	k_idx += 2


	# execute
	if k_idx <= len(k) - 2: 
		
		x = toBinary( N, k[k_idx][1] )
		write = k[k_idx][2]
		address = k[k_idx][3]

		ram.write( clk, x, write, address )


	# exhausted test values
	else:
		clock.stop() # stop the clock
		fails.report( testName )   # show results


def record():

	address = k[k_idx + 1][3]

	result = toString( ram.read( address ) )

	expected = toBinary( N, k[k_idx + 1][4] )

	if expected != result:
		fails.record( expected, result, k_idx + 1 ) # log the fail



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

