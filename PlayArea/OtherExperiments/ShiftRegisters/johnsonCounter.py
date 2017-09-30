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

nStages = 5
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with '1000'
for i in range(nStages): dff[i].clear()
dff[0].preset()

n_iterations = 0


def SR(clk):

	# Shift
	dff[0].doTheThing( clk, not_( dff[nStages - 1].q1 ) )  # invert

	for i in range( 1, nStages ):
		dff[i].doTheThing( clk, dff[i - 1].q1 )


	global n_iterations
	n_iterations += 1
	if n_iterations >= 100: clock.stop() # stop the clock


def record():
	print( toString( [dff[0].q1, dff[1].q1, dff[2].q1, dff[3].q1] ) )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	SR( clock.value )

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


if __name__ == '__main__': 

	# Start program
	clock.run()