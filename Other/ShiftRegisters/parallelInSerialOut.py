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

dataIn = [
	1,0,1,0,
	1,1,0,0,
	1,1,1,0
]
dataIn.extend( [0]*nStages*12 ) # fluff

# start with all gates reset
for i in range(nStages): dff[i].clear()

load, shift = None, None

def SR(clk):

	global load
	global shift
	global dataIn
	global nStages

	# Handle parallel load
	if clock.currentCycle % nStages == 0:
		load = True
		print('~')
	else:
		load = False
	shift = not_(load)


	# Handle serial shift
	idx = clock.currentCycle

	dff[0].doTheThing( 
		clk,
		and_( not_(shift), dataIn[idx+0] ) 
	)
	dff[1].doTheThing(
		clk,
		or_( and_( not_(shift), dataIn[idx+1] ), and_( shift, dff[0].q1 )  )
	)
	dff[2].doTheThing(
		clk,
		or_( and_( not_(shift), dataIn[idx+2] ), and_( shift, dff[1].q1 )  )
	)
	dff[3].doTheThing(
		clk,
		or_( and_( not_(shift), dataIn[idx+3] ), and_( shift, dff[2].q1 )  )
	)

	# Read outputs
	global delayRecording
	time.sleep(delayRecording)
	print( toString( [dff[0].q1, dff[1].q1, dff[2].q1, dff[3].q1] ) )



''''''''''''''''''''''''' run '''''''''''''''''''''''''

def main():
	global clock 
	clock.halfTick()

	if clock.isRising:
		SR(clock.value)

	clock.keepTicking(1, main)  # seconds


# Run
if __name__ == '__main__':
	main()

# python latchTest.py > output.txt