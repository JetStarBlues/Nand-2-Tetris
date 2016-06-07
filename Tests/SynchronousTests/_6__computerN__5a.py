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

computer.load( './PlayArea/assembler/bin/test5a_array.bin' )


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

			if toDecimal( toString( result ) ) != 2**N - 1: # -1
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
