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
import threading


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

# Setup ---
clock = Clock()
delayRecording = clock.halfPeriod * 0.9
k_idx = 0


''' =========================================================
                   RegisterN_( N, clk, x, write )
	========================================================= '''

k = k_register16
N = 16
register = RegisterN_( N )

def test(clk):

	global fails
	global k_idx
	

	if k_idx <= len(k) - 1: 

		# execute ---
		x = toBinary( N, k[k_idx][1] )
		write = k[k_idx][2]
		expected = toBinary( N, k[k_idx][3] )

		register.doTheThing( clk, x, write )


		# record result ---
		time.sleep(delayRecording * 2 * N)
		
		result = toString( register.out() )

		if expected != result:
			fails.append( [ expected, result, k_idx ] ) # log the fail


		# increment ---
		k_idx += 1


	else:
		# exhausted test values, show results ---
		clock.duration = clock.duration - 1e5 # stop the clock
		logFails()


''''''''''''''''''''''''''' run '''''''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	test( clock.value )

def callOnFalling():
	pass

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 60 # seconds
clock.run()
