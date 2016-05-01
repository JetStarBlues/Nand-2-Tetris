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

nStages = 3
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with all gates reset
for i in range(nStages): dff[i].clear()

#
def logState(data):
	state = toString(data)
	if state == '000': print('A')
	elif state == '001' or state == '101': print('B')
	elif state == '010' or state == '100': print('C')
	elif state == '011': print('D')
	else: print(state)


def FSM(clk):
	'''light up four LEDs in 1234321.. pattern 
		 https://www.youtube.com/watch?v=OXscvtUomOA
	'''
	# round robin / Moore, 6 states

	dff[0].doTheThing( 
		clk,
		or_(
			and_( dff[0].q1, dff[2]._q1 ),
			and_( dff[1].q1, dff[2].q1 )
		)
	)
	dff[1].doTheThing( 
		clk,
		or_(
			and_( dff[1].q1, dff[2]._q1 ),
			and3_( dff[0]._q1, dff[1]._q1, dff[2].q1 )
		)
	)
	dff[2].doTheThing( clk, dff[2]._q1 )


	# Record output
	global delayRecording
	time.sleep(delayRecording)	
	logState([ dff[0].q1, dff[1].q1, dff[2].q1 ])



''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	FSM(clock.value)

def callOnFalling():
	pass


clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 1 # seconds
clock.run()