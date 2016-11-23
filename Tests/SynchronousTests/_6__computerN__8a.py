'''=== ComputerN ==================================================== '''


'''----------------------------- Imports -----------------------------'''

# Hack computer tests
from Tests import *


'''------------------------------- Main -------------------------------'''

# Setup ---

testName, clock, fails, count, N, computer, a, b, expected = [ None ] * 9

def setup():

	global testName
	global clock
	global fails
	global count
	global N
	global computer
	global a
	global b
	global expected
	global io

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()
	count = 0

	N = 16
	computer = ComputerN_( N, 2**16, 2**15 )
	io = IO( N, computer.main_memory )

	computer.load( KnownValues.pathTo_kv_4 + 'test8a_fill.bin' )
	a = 32 * 100


# Update ---

def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		computer.main_memory.write( clk, toBinary( N, a ), 1, 0 ) # clk, x, write, address

	elif count <= 1+16+17*32+6+ 8:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock			

	if io.hasExited:
		clock.stop() # stop the clock


def record():
	pass



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
