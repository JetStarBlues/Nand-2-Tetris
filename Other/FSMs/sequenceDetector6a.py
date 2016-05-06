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

clock = Clock()

nStages = 3
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with all gates reset
for i in range(nStages): dff[i].clear()

sequence = [1,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0]
sequence.reverse()
dataIn = sequence
# dataIn = [0,1,1,1,0,1,1,0,1,0,0,1,1,0]
dataIdx = len(dataIn) - 1  # load RtoL
out = None


def SD(clk):
	'''outputs a 1 when detect 101 or 110 or 011'''

	# using mux'es ( www.csee.umbc.edu/courses/undergraduate/313/Fall03/cpatel2/slides/slides20.pdf )

	global dataIn
	global dataIdx
	global out

	data = dataIn[dataIdx]

	n_data = not_( data )

	dff[0].doTheThing( 
		clk, 
		mux8to1_( 0, 1, data, 1, data, 1, data, 0, dff[0].q1, dff[1].q1, dff[2].q1 )
	)
	dff[1].doTheThing( 
		clk, 
		mux8to1_( 0, data, n_data, data, n_data, data, n_data, data, dff[0].q1, dff[1].q1, dff[2].q1 )
	)
	dff[2].doTheThing( 
		clk, 
		mux8to1_( 0, n_data, n_data, n_data, n_data, n_data, n_data, n_data, dff[0].q1, dff[1].q1, dff[2].q1 )
	)
	out = mux8to1_( 0, n_data, data, data, 0, 0, 0, 0, dff[0].q1, dff[1].q1, dff[2].q1 )


	#
	if dataIdx >= 0 : dataIdx -= 1		

	else: clock.stop() # stop the clock


def record():

	data = dataIn[dataIdx + 1]

	print( data, " ", out )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	SD( clock.value )

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


if __name__ == '__main__': 

	# Start program
	clock.run()