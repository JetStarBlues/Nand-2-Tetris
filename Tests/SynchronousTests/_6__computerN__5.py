''' =========================================================
               ComputerN_( N, RAM_size, ROM_size )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )
clock = Clock()
fails = FailLogger()
count = 0

N = 16
computer = ComputerN_( N, 2**16, 2**15 )

computer.load( './PlayArea/assembler/bin/test5_array.bin' )

a = 9000


def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		computer.main_memory.write( clk, toBinary( N, a ), 1, 0 ) # clk, x, write, address

	elif count <= 230:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock


		print( '\n-- Finished test ' + testName )

		no_fails = True

		for i in range(10):

			result = computer.main_memory.read( 100 + i )

			if toDecimal( toString( result ) ) != a:
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

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
def start():
	clock.run()
