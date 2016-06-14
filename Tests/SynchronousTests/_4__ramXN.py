''' =========================================================
              RAMXN_( X, N, clk, x, write, address )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName, clock, fails, k_idx, r_idx, k, X, N, ram = [ None ] * 9

def setup():

	global testName
	global clock
	global fails
	global k_idx
	global r_idx
	global k
	global X
	global N
	global ram

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()

	k = [ 
		KnownValues.k_ram8_16, 
		KnownValues.k_ram64_16, 
		KnownValues.k_ram512_16, 
		KnownValues.k_ram4k_16, 
		KnownValues.k_ram16k_16 
	]
	X = [ 8, 64, 512, 2**12, 2**14 ]
	N = 16

	k_idx = -2
	r_idx = 0
	ram = RAMXN_( X[r_idx], N )


# Update ---

def update(clk):

	global r_idx
	global k_idx
	global ram


	# increment
	k_idx += 2

	
	if k_idx <= len( k[r_idx] ) - 2:
	
		# execute		
		x = toBinary( N, k[r_idx][k_idx][1] )
		write = k[r_idx][k_idx][2]
		address = k[r_idx][k_idx][3]

		ram.write( clk, x, write, address )

	else:

		# exhausted test values
		if r_idx == len(k) - 1:
			clock.stop() # stop the clock
			fails.report( testName )   # show results

		# test next ram chip
		else:
			r_idx += 1
			ram = RAMXN_( X[r_idx], N )
			k_idx = -2
			update(clk)  # oO! Hacky oh well. Avoids having clock cycle where nothing thing executes


def record():

	address = k[r_idx][k_idx + 1][3]

	result = toString( ram.read( address ) )

	expected = toBinary( N, k[r_idx][k_idx + 1][4] )

	if expected != result:
		fails.record( expected, result, toString( [k_idx + 1, '  for RAM', r_idx] ) ) # log the fail



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

