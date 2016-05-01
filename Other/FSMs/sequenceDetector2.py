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

clock = Clock()
delayRecording = clock.halfPeriod * 0.9

'''
When updating period values, consider:
	1) clock's half period
	2) FF propogation delay
		> faux/simulated
		> how long take for Q to update to new inputs
	3) record delay 
		> wait till Q/output values settled before recording/reading them.
		> Selection range -> immediately after FF Propogation delay .. before end of second halfTick
'''

''''''''''''''''''''''''' main '''''''''''''''''''''''''

nStages = 2
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with all gates reset
for i in range(nStages): dff[i].clear()

dataIn = [0,0,1,0,1,0,0,1,1,0]
dataIdx = len(dataIn) - 1  # load RtoL


def SD(clk):
	'''outputs a 1 when detect 010'''

	global dataIn
	global dataIdx

	data = dataIn[dataIdx]

	dff[0].doTheThing( 
		clk, 
		and_( data, dff[1].q1 )
	)
	dff[1].doTheThing( 
		clk, 
		not_( data )
	)
	out = and_( not_( data ), dff[0].q1 )

	#
	if dataIdx >= 0 : 

		dataIdx -= 1

		# Record output
		global delayRecording
		time.sleep(delayRecording)
		print( data, " ", out )

	else:
		print(".")


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	SD(clock.value)

def callOnFalling():
	pass


clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 1 # seconds
clock.run()