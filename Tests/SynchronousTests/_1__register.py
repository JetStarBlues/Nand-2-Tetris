'''=== Register ======================================================'''


'''----------------------------- Imports -----------------------------'''

from Tests import *


'''------------------------------- Main -------------------------------'''

# Setup ---

testName, clock, fails, k_idx, k, register = [ None ] * 6

def setup():

	global testName
	global clock
	global fails
	global k_idx
	global k
	global register

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()

	k_idx = -2

	k = KnownValues.k_register
	register = Register_()


# Update ---

def update(clk):

	global k_idx
	
	# increment
	k_idx += 2


	# execute
	if k_idx <= len(k) - 2: 
		
		x = k[k_idx][1]
		write = k[k_idx][2]

		register.write( clk, x, write )


	# exhausted test values
	else:
		clock.stop() # stop the clock
		fails.report( testName )   # show results


def record():

	result = register.read()

	expected = k[k_idx + 1][3]

	if expected != result:
		fails.record( expected, result, k_idx + 1 ) # log the fail



'''----------------------------- Run -----------------------------'''

# Things to execute on clock edges
def callOnRising():
	update( clock.value )

def callOnFalling():
	record()


# Start program
def start():
	setup()
	clock.run()