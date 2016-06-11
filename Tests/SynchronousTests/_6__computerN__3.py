''' =========================================================
               ComputerN_( N, RAM_size, ROM_size )
    ========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Hack computer tests
from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )
clock = Clock()
fails = FailLogger()
count = 0

N = 16
computer = ComputerN_( N, 2**16, 2**15 )

computer.load( KnownValues.pathTo_kv_4 + 'test3_add.bin' )

a = 2**14
b = 356
expected = a + b


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
		result_dec = toDecimal( toString( result ) )


		print( '\n-- Finished test ' + testName )

		if result_dec == expected:
			print( 'Success! Program executes as expected' )
		else:
			print( 'Fail! Something somewhere is not working' )
			print( result_dec, result )


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
