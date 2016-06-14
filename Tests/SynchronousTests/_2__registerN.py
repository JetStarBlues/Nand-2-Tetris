''' =========================================================
                   RegisterN_( N, clk, x, write )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName, clock, fails, k_idx, k, N, register = [ None ] * 7

def setup():

	global testName
	global clock
	global fails
	global k_idx
	global k
	global N
	global register

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()

	k_idx = -2

	k = KnownValues.k_register16
	N = 16
	register = RegisterN_( N )


# Update ---

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


# Start program
def start():
	setup()
	clock.run()
