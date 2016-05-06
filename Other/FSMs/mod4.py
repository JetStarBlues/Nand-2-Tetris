''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys

# Computer files
sys.path.append('../../Modules')
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _3__clock import *
from _4__flipFlops import *


''''''''''''''''''''''''' helpers '''''''''''''''''''''''''

def toString(array):
	return ''.join( map(str, array) )

def toDecimal(bitSeq):
	return int(bitSeq, 2)


''''''''''''''''''''''''' main '''''''''''''''''''''''''

# Mod4 FSM diagram -> www.csee.umbc.edu/courses/undergraduate/313/Fall03/cpatel2/slides/slides20.pdf

clock = Clock()

dA = DFlipFlop()
dB = DFlipFlop()

# start with all gates reset
dA.clear()
dB.clear()

def logState(a, b):
	state = str(a) + str(b)
	# return( toDecimal(state) )
	return( state + "   " + str( toDecimal(state) ) )

reset = [0,0,0,0,0,0,1,1,1,0,0,0,0,0,0] # active high
idx = len(reset) - 1  # load RtoL


def FSM(clk):

	global reset
	global idx

	#
	dA.doTheThing( 
		clk, 
		and_( 
			not_(reset[idx]),
			xor_(dA.q1, dB.q1 )
		)
	)

	dB.doTheThing(
		clk,
		and_( not_(reset[idx]), dB._q1 )
	)

	#
	if idx >= 0 : idx -= 1

	else: clock.stop() # stop the clock


def record():

	# Record output
	print( logState( dA.q1, dB.q1 ) )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	FSM(clock.value)

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


if __name__ == '__main__': 

	# Start program
	clock.run()