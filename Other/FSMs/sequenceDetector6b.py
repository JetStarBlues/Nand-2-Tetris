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

# start with all gates reset
for i in range(nStages): dff[i].clear()

sequence = [1,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0]
sequence.reverse()
dataIn = sequence
# dataIn = [0,1,1,1,0,1,1,0,1,0,0,1,1,0]
dataIdx = len(dataIn) - 1  # load RtoL


def SD(clk):
	'''outputs a 1 when detect 101 or 110 or 011'''

	# non-reduced... what a mess! lol 

	global dataIn
	global dataIdx

	data = dataIn[dataIdx]

	dff[0].doTheThing( 
		clk,
		and_(
			and_( data, dff[1].q1 ),
			xor_( dff[2].q1, dff[3].q1 ),
		)
	)
	dff[1].doTheThing( 
		clk,
		or3_(
			and_(
				dff[3]._q1,
				or_(
					dff[0].q1,
					and_( dff[1].q1, dff[2]._q1 )
				)
			),
			and_(
				and_( data, dff[3].q1 ),
				or_( dff[1]._q1, dff[2].q1 )
			),
			and3_( data, dff[1]._q1, dff[2].q1 )
		)
	)
	dff[2].doTheThing( 
		clk,
		or_(
			not_( data ),
			and_( dff[2].q1, dff[3].q1 )
		)
	)
	dff[3].doTheThing( 
		clk,
		or_(
			and_(
				dff[3]._q1,
				or_(
					and_( 
						not_( data ), 
						or_( dff[0].q1, dff[1].q1 ) 
					),
					and3_( data, dff[0]._q1, dff[1]._q1 )
				)
			),
			and3_( not_( data ), dff[2]._q1, dff[3].q1 )
		)
	)
	out = or3_(
		and_(
			and_( not_( data ), dff[3]._q1 ),
			or_(
				dff[0].q1,
				and_( dff[1].q1, dff[2]._q1 )
			)
		),
		and3_( data, dff[1].q1, dff[2].q1 ),
		and_(
			and_( data, dff[3].q1 ),
			or_( dff[1].q1, dff[2].q1 )
		)
	)

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

def main():
	global clock 
	clock.halfTick()

	if clock.isRising:
		SD(clock.value)

	clock.keepTicking(1, main)  # seconds


# Run
if __name__ == '__main__':
	main()

# python latchTest.py > output.txt