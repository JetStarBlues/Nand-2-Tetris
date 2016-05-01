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

nStages = 4
dff = []
for i in range(nStages): dff.append( DFlipFlop() )

# start with '0100'
for i in range(nStages): dff[i].clear()
dff[1].preset()

# data in
dataIn_L = 0  # hold low
dataIn_R = 1  # hold high
dataIn_Parallel = [
	[1,0,1,0],
	[1,1,0,0],
	[1,1,1,0]
]
dataIdx = len(dataIn_Parallel) - 1 # load RtoL

# mode selection
s0 = 0
s1 = 0
mode = [ # values over time
	[1,1],
	[1,0],
	[1,0],
	[1,0],
	[0,1],
	[0,1],
	[0,1],
	[0,1],
	[1,1],
	[1,1],
	[0,0],
	[0,0],
	[0,0],
	[1,0],
	[1,0],
	[1,1],
	[0,1],
	[0,1],
	[0,1],
]
modeIdx = len(mode) - 1 # load RtoL

def logMode(s1, s0):
	mode = str(s1) + str(s0)
	if mode == '00': return( "inhibit" )
	elif mode == '01': return( "shift right" )
	elif mode == '10': return( "shift left" )
	elif mode == '11': return( "parallel load" )


def SR(clk):

	# see 74194 datasheet, http://www.ti.com/lit/ds/symlink/sn54s194.pdf

	global s0
	global s1
	global modeIdx
	global dataIdx
	global dataIn_L
	global dataIn_R
	global dataIn_Parallel

	# Handle mode
	s1 = mode[modeIdx][0]
	s0 = mode[modeIdx][1]
	_s1 = not_(s1)
	_s0 = not_(s0)
	load = nor_( _s1, _s0 )
	disable = and_( _s1, _s0 )
	clk2 = nor_( disable, not_(clk) )


	# Shift or load
	dff[0].doTheThing( 
		clk2,
		or3_( 
			and_( _s1, dataIn_R ),
			and_( _s0, dff[1].q1 ),
			and_( load, dataIn_Parallel[dataIdx][0] )
		)
	)
	dff[1].doTheThing( 
		clk2,
		or3_( 
			and_( _s1, dff[0].q1 ),
			and_( _s0, dff[2].q1 ),
			and_( load, dataIn_Parallel[dataIdx][1] )
		)
	)
	dff[2].doTheThing( 
		clk2,
		or3_( 
			and_( _s1, dff[1].q1 ),
			and_( _s0, dff[3].q1 ),
			and_( load, dataIn_Parallel[dataIdx][2] )
		)
	)
	dff[3].doTheThing( 
		clk2,
		or3_( 
			and_( _s1, dff[2].q1 ),
			and_( _s0, dataIn_L ),
			and_( load, dataIn_Parallel[dataIdx][3] )
		)
	)

	
	# go to next mode (simulation)
	if modeIdx > 0 : modeIdx -= 1
	if dataIdx > 0 : dataIdx -= load


	# Read outputs
	global delayRecording
	time.sleep(delayRecording)	
	print( toString( [dff[0].q1, dff[1].q1, dff[2].q1, dff[3].q1] ), logMode( s1, s0 ) )



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