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

computer.load( './PlayArea/assembler/bin/test1_addTo.bin' )
x = 6
expected = sum(range(x+1))  # 1 + 2 + ... x


count = 0

def update(clk):

	global count
	
	# increment
	count += 1


	#
	if count == 1:
		# setup
		computer.main_memory.write( clk, toBinary( N, 6 ), 1, 0 ) # clk, x, write, address

	elif count <= 110:
		# main
		computer.run( clk )


	# done test
	else:
		clock.stop() # stop the clock
		
		result = computer.main_memory.read( 1 )
		result_d = toDecimal( toString( result ) )
		# print( result_d, result )


		print( '\n-- Finished test ' + testName )
		
		if result_d == expected :
			print( 'Success! Program executes as expected' )
		else:
			print( 'Fail! Something somewhere is not working' )


def record():
	pass

	# print(   'i', toDecimal( toString( computer.main_memory.read( 16 ) ) ) )
	# print( 'sum', toDecimal( toString( computer.main_memory.read( 17 ) ) ) )



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
