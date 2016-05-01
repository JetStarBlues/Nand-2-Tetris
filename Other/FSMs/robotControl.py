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

dataIn = [0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,1,0,0,0,0,0,1,0,0,1,0]
dataIdx = len(dataIn) - 1  # load RtoL

def logState( bumped, state ):
	state = toString( state )
	if state == '000': print( "forward at 25% speed >" )
	if state == '001': print( "forward at 50% speed >>" )
	if state == '010': print( "forward at 75% speed >>>" )
	if state == '011': print( "forward at full speed >>>>" )
	if state == '100': print( "reverse at 25% speed <" )
	if state == '101': print( "reverse at 50% speed <<" )
	if state == '110': print( "reverse at 75% speed <<<" )
	if state == '111': print( "reverse at full speed <<<<" )
	if bumped: print( "- hit something" )
	# else: print( "- coast is clear" )

def RC(clk):
	'''changes direction when hits something'''

	global dataIn
	global dataIdx

	data = dataIn[dataIdx]

	dff[0].doTheThing( 
		clk,
		and_(
			not_( data ),
			or_( dff[0]._q1, dff[1].q1 )
		)
	)
	dff[1].doTheThing( 
		clk,
		and_(
			not_( data ),
			or_( dff[0].q1, dff[1].q1 )
		)		
	)
	dff[2].doTheThing( 
		clk,
		xor_( data, dff[2].q1 )
	)

	#
	if dataIdx >= 0 : 

		dataIdx -= 1

		# Record output
		global delayRecording
		time.sleep(delayRecording)
		logState( data, [ dff[2].q1, dff[1].q1, dff[0].q1 ] )

	else:
		print(".")


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	RC(clock.value)

def callOnFalling():
	pass


clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 1 # seconds
clock.run()