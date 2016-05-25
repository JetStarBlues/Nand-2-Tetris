''' =========================================================
                   CPU_( N, clk, x, write ) ???
	========================================================= '''


''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

from Tests import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# Setup ---

testName = fileName( __name__ )

clock = Clock()
fails = FailLogger()

k_idx = -2

k = k_register16
N = 16
register = RegisterN_( N )



# potato = MemoryROM_( 2**16, 16 )
# potato.flash( '../PlayArea/assembler/bin/mult.bin' )
# print( 'the value stored at register {} is {}'.format( 17, ''.join( map(str, potato.read( 17 ) ) ) ) )

potato = ComputerN_( 16, 2**16, 2**15 )
potato.main_memory.write( )



def update(clk):

	global k_idx
	
	# increment
	k_idx += 2

	'''
	# execute 
	if k_idx <= len(k) - 2: 
		
		x = toBinary( N, k[k_idx][1] )
		write = k[k_idx][2]

		register.write( clk, x, write )
	'''

	if k_idx <= 200:
		??

	# exhausted test values
	else:
		clock.stop() # stop the clock
		fails.report( testName )   # show results


def record():

	result = toString( register.read() )

	expected = toBinary( N, k[k_idx + 1][3] )

	if expected != result:
		fails.record( expected, result, k_idx + 1 ) # log the fail



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
