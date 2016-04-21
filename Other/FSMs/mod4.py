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

# http://www.csee.umbc.edu/courses/undergraduate/313/Fall03/cpatel2/slides/slides20.pdf

dA = DFlipFlop()
dB = DFlipFlop()

# start with all gates reset
dA.clear()
dB.clear()

def logState(a, b):
	state = str(a) + str(b)
	# return( toDecimal(state) )
	return( state + "   " + str( toDecimal(state) ) )

reset = [0,0,1,1,1,0,0,0,0,0,0] # active high
idx = len(reset) - 1  # load RtoL

def FSM(clk):

	global reset
	global idx

	#
	dA.doTheThing( 
		clk, 
		or_( 
			and3_( not_(reset[idx]), dA.q1, dB._q1 ),
			and3_( not_(reset[idx]), dA._q1, dB.q1 )
		)
	)

	dB.doTheThing(
		clk,
		and_( not_(reset[idx]), dB._q1 )
	)

	#
	if idx >= 0 : idx -= 1

	
	# Record output
	global delayRecording
	time.sleep(delayRecording)
	print( logState( dA.q1, dB.q1 ) )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

def main():
	global clock 
	clock.halfTick()

	if clock.isRising:
		FSM(clock.value)

	clock.keepTicking(1, main)  # seconds


# Run
if __name__ == '__main__':
	main()

# python latchTest.py > output.txt