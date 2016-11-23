'''=== RAM8N ========================================================='''


'''----------------------------- Imports -----------------------------'''

from Tests import *


'''------------------------------- Main -------------------------------'''

# Setup ---

testName, clock, fails, k_idx, k, N, ram = [ None ] * 7

def setup():

	global testName
	global clock
	global fails
	global k_idx
	global k
	global N
	global ram

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()

	k_idx = -2

	k = KnownValues.k_ram8_16
	N = 16
	ram = RAM8N_( N )


# Update ---

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



'''------------------------------- Run -------------------------------'''

# Things to execute on clock edges
def callOnRising():
	update( clock.value )

def callOnFalling():
	record()


# Start program
def start():
	setup()
	clock.run()

