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

N = 16
computer = ComputerN_( N, 2**16, 2**15 )

computer.load( './PlayArea/assembler/bin/test3_add.bin' )


count = 0

def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		computer.main_memory.write( clk, toBinary( N, 2**14 ), 1, 0 ) # clk, x, write, address
		computer.main_memory.write( clk, toBinary( N, 356 ), 1, 1 )

	elif count <= 20:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock
		
		result = computer.main_memory.read( 2 )


		print( '\n-- Finished test ' + testName )

		if toDecimal( toString( result ) ) == 2**14 + 356:
			print( 'Success! Program executes as expected' )
		else:
			print( 'Fail! Something somewhere is not working' )


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
