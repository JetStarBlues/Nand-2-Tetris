''' =========================================================
                   RegisterN_( N, clk, x, write )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )
clock = Clock()
fails = FailLogger()

k_idx = -2

k = k_register16
N = 16
register = RegisterN_( N )


def update(clk):

	global k_idx
	
	# increment
	k_idx += 2


	# execute
	if k_idx <= len(k) - 2: 
		
		x = toBinary( N, k[k_idx][1] )
		write = k[k_idx][2]

		register.write( clk, x, write )


	# exhausted test values
	else:
		clock.stop() # stop the clock
		fails.report( testName )   # show results


def record():

	result = toString( register.read() )

	expected = toBinary( N, k[k_idx + 1][3] )

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
