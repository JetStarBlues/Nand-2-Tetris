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

nStages = 4
dff = []
for i in range(nStages): dff.append( DFlipFlop() )
dataIn = [1,0,1,0,0,0,0,0,1,1,0,1]
dataIdx = len(dataIn) - 1  #load RtoL

# start with all gates reset
for i in range(nStages): dff[i].clear()

def SR(clk):

	global dataIn
	global dataIdx
	
	if dataIdx >= 0 :

		dff[0].doTheThing( clk, dataIn[dataIdx] )
		dff[1].doTheThing( clk, dff[0].q1 )
		dff[2].doTheThing( clk, dff[1].q1 )
		dff[3].doTheThing( clk, dff[2].q1 )

		dataIdx -= 1

	else: clock.stop() # stop the clock


def record():

	s = '' 
	if clock.currentCycle % nStages == nStages - 1: s = '>>' # parallel out (sort of, how do mod with logic gates?)

	print( toString( [dff[0].q1, dff[1].q1, dff[2].q1, dff[3].q1] ), s )


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