'''=== ProgramCounterN ==============================================='''


'''----------------------------- Imports -----------------------------'''

from HardwareTests import *


'''------------------------------- Main -------------------------------'''

# Setup ---

testName, clock, fails, k_idx, k, N, pc = [ None ] * 7

def setup():

	global testName
	global clock
	global fails
	global k_idx
	global k
	global N
	global pc

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()

	k_idx = -2

	k = KnownValues.k_programCounter_16
	N = 16
	pc = ProgramCounterN_( N )

	if PERFORMANCE_MODE:
		pc = ProgramCounterN_( N )


# Update ---

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

	result = pc.read()

	expected = k[k_idx + 1][5]
	if expected < 0: expected = 2 ** N + expected  # change to 2s complement notation

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

