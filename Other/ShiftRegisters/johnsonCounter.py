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

nStages = 5
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with '1000'
for i in range(nStages): dff[i].clear()
dff[0].preset()


def SR(clk):

	# Shift
	dff[0].doTheThing( clk, not_( dff[nStages - 1].q1 ) )  # invert

	for i in range( 1, nStages ):
		dff[i].doTheThing( clk, dff[i - 1].q1 )


	# Read outputs
	global delayRecording
	time.sleep(delayRecording)
	print( toString( [dff[0].q1, dff[1].q1, dff[2].q1, dff[3].q1] ) )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	SR(clock.value)

def callOnFalling():
	pass


clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 1 # seconds
clock.run()