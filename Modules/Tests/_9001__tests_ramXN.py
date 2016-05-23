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
			print( 'exp {}  got {}  at {}  for RAM{}'.format( fail[0], fail[1], fail[2], X[fail[3]] ) )

	else:
		print( 'Success! All values match.')	



''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

''' =========================================================
              RAMXN_( X, N, clk, x, write, address )
	========================================================= '''

# Setup ---

clock = Clock()

k = [ k_ram8_16, k_ram64_16, k_ram512_16, k_ram4k_16, k_ram16k_16 ]
X = [ 8, 64, 512, 2**12, 2**14 ]
N = 16

k_idx = -2
r_idx = 0
ram = RAMXN_( X[r_idx], N )


def update(clk):

	global r_idx
	global k_idx
	global ram


	# increment
	k_idx += 2

	
	if k_idx <= len( k[r_idx] ) - 2:
	
		# execute		
		x = toBinary( N, k[r_idx][k_idx][1] )
		write = k[r_idx][k_idx][2]
		address = k[r_idx][k_idx][3]

		ram.write( clk, x, write, address )

	else:

		# exhausted test values
		if r_idx == len(X) - 1:
			clock.stop() # stop the clock
			logFails()   # show results

		# test next ram chip
		else:
			r_idx += 1
			ram = RAMXN_( X[r_idx], N )
			k_idx = -2
			update(clk)  # oO! Hacky oh well. Avoids having clock cycle where nothing thing executes


def record():

	global fails

	address = k[r_idx][k_idx + 1][3]

	result = toString( ram.read( address ) )

	expected = toBinary( N, k[r_idx][k_idx + 1][4] )

	if expected != result:
		fails.append( [ expected, result, k_idx + 1, r_idx ] ) # log the fail



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

