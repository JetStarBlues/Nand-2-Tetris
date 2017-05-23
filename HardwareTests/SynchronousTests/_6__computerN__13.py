'''=== ComputerN ==================================================== '''


'''----------------------------- Imports -----------------------------'''

# Hack computer tests
from HardwareTests import *


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

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()
	count = 0

	N = 16
	computer = ComputerN_( N, 2**16, 2**15 )

	computer.load( KnownValues.pathTo_kv_4 + 'test13_shiftRight.bin' )

	a = 40337
	b = 5
	expected = a >> b


# Update ---

def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		computer.main_memory.write( clk, toBinary( N, a ), 1, 0 ) # clk, x, write, address
		computer.main_memory.write( clk, toBinary( N, b ), 1, 1 )

	elif count <= 20:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock
		

		result = computer.main_memory.read( 2 )
		result_dec = toDecimal_( result )


		print( '\n-- Finished test ' + testName )

		if result_dec == expected:
			print( 'Success! Program executes as expected' )
		else:
			print( 'Fail! Something somewhere is not working' )
			print( result_dec, result )


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
