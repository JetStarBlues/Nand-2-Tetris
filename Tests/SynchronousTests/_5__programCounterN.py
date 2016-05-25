''' =========================================================
           ProgramCounterN_( N, clk, x, write, inc, rst )
	========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )

clock = Clock()
fails = FailLogger()

k_idx = -2

k = k_programCounter_16
N = 16
pc = ProgramCounterN_( N )


def update(clk):

	global k_idx
	
	# increment
	k_idx += 2


	# execute
	if k_idx <= len(k) - 2: 
		
		x = toBinary( N, k[k_idx][1] )
		rst = k[k_idx][2]
		write = k[k_idx][3]
		inc = k[k_idx][4]

		pc.doTheThing( clk, x, rst, write, inc )


	# exhausted test values
	else:
		clock.stop() # stop the clock
		fails.report( testName )   # show results


def record():

	result = toString( pc.out() )

	# print( toDecimal( result ) )

	expected = toBinary( N, k[k_idx + 1][5] )

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

