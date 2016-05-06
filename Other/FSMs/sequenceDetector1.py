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

nStages = 2
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with all gates reset
for i in range(nStages): dff[i].clear()

dataIn = [0,1,1,1,1,0,1,1,1,0,0]
dataIdx = len(dataIn) - 1  # load RtoL
out = None


def SD(clk):
	'''outputs a 1 when detect three consecutive 1's'''

	global dataIn
	global dataIdx
	global out

	data = dataIn[dataIdx]

	dff[0].doTheThing( 
		clk, 
		and_( data, or_( dff[0].q1, dff[1].q1 ) )
	)
	dff[1].doTheThing( 
		clk, 
		and_( data, or_( dff[0].q1, dff[1]._q1 ) )
	)
	out = and_( data, dff[0].q1 )


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
