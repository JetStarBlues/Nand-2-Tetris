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

dataIn_L = 0  # hold low
dataIn_R = 1  # hold high
right = [1,1,1,1,0,0,0,0,1,1,1,0,1,0] # values over time
idx = len(right) - 1 # load RtoL

def SR(clk):

	global right
	global idx
	global dataIn_L
	global dataIn_R

	if idx >= 0 :

		# Shift
		dff[0].doTheThing( 
			clk,
			or_( 
				and_( right[idx], dataIn_R ),
				and_( not_(right[idx]), dff[1].q1 )
			)
		)
		dff[1].doTheThing( 
			clk,
			or_( 
				and_( right[idx], dff[0].q1 ),
				and_( not_(right[idx]), dff[2].q1 )
			)
		)
		dff[2].doTheThing( 
			clk,
			or_( 
				and_( right[idx], dff[1].q1 ),
				and_( not_(right[idx]), dff[3].q1 )
			)
		)
		dff[3].doTheThing( 
			clk,
			or_( 
				and_( right[idx], dff[2].q1 ),
				and_( not_(right[idx]), dataIn_L )
			)
		)

		idx -= 1
	
	else:
		# do nothing
		pass


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