'''
	In the spirit of
	  http://www.diveintopython3.net/unit-testing.html
	  http://www.diveintopython3.net/refactoring.html
	The tutorials show how maintainable and refactorable code becomes when use tests
'''

''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys
# import unittest  ... Not sure how to use for clocked circuits. Revisit!!


# Computer files
sys.path.append('../')
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _3__clock import *
from _4__flipFlops import *
from _5__memory import *


# Testing files
sys.path.append('KnownValues')
from kv_1__elementaryGates import *
from kv_2__arithmeticGates import *
from kv_3__memory import *


''''''''''''''''''''''''' testing helpers '''''''''''''''''''''''''

# Formatting ---

def toString(array):
	return ''.join( map(str, array) )

def toDecimal(bitSeq):
	return int(bitSeq, 2)

def toBinary(N, x):
	if x < 0: x = 2**N + x  # 2s complement
	return bin(x)[2:].zfill(N)


# Logging ---

fails = []
def logFails():

	global fails

	if fails:
		print( '\n--- {} values failed --- \n'.format( len(fails) ) )
		for fail in fails:
			print( 'exp {}  got {}  at {}'.format( fail[0], fail[1], fail[2] ) )

	else:
		print( 'Success! All values match.')	



''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

''' =========================================================
           ProgramCounterN_( N, clk, x, write, inc, rst )
	========================================================= '''

# Setup ---

clock = Clock()
k_idx = -2

k = k_programCounter_16
N = 16
pc = ProgramCounterN_( N )


def update(clk):

	global k_idx
	
	# increment
	k_idx += 2


	# execute
	if k_idx <= len(k) - 2: 
		
		x = toBinary( N, k[k_idx][1] )
		rst = k[k_idx][2]
		write = k[k_idx][3]
		inc = k[k_idx][4]

		pc.doTheThing( clk, x, rst, write, inc )


	# exhausted test values
	else:
		clock.stop() # stop the clock
		logFails()   # show results


def record():

	global fails

	result = toString( pc.out() )

	# print( toDecimal( result ) )

	expected = toBinary( N, k[k_idx + 1][5] )

	if expected != result:
		fails.append( [ expected, result, k_idx + 1 ] ) # log the fail



''''''''''''''''''''''''''' run '''''''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	update( clock.value )

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


if __name__ == '__main__': 

	# Start program
	clock.run()

