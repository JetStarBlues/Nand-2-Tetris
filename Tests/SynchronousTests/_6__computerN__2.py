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

	testName = fileName( __name__ )

	clock = Clock()
	clock.callbackRising = callOnRising
	clock.callbackFalling = callOnFalling

	fails = FailLogger()
	count = 0

	N = 16
	computer = ComputerN_( N, 2**16, 2**15 )

	computer.load( KnownValues.pathTo_kv_4 + 'test2_flip.bin' )

	a = 50
	b = 33


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
		
		result0 = computer.main_memory.read( 0 )
		result1 = computer.main_memory.read( 1 )


		print( '\n-- Finished test ' + testName )

		if toString( result0 ) == toBinary( N, b ) and \
		   toString( result1 ) == toBinary( N, a ):
			print( 'Success! Program executes as expected' )
		else:
			print( 'Fail! Something somewhere is not working' )


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
