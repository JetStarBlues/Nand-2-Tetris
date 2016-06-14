''' =========================================================
               ComputerN_( N, RAM_size, ROM_size )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Hack computer tests
from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

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

	computer.load( KnownValues.pathTo_kv_4 + 'test5a_array.bin' )


# Update ---

def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		pass

	elif count <= 170:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock


		print( '\n-- Finished test ' + testName )

		no_fails = True

		for i in range(10):

			result = computer.main_memory.read( 100 + i )

			if toDecimal_( result ) != 2**N - 1: # -1
				print( 'Fail! Something somewhere is not working' )
				print( 100 + i, result )
				no_fails = False

		if no_fails:
			print( 'Success! Program executes as expected' )
			

def record():
	pass



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
