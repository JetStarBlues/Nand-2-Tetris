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

jk1 = JKFlipFlop()
jk2 = JKFlipFlop()
jk3 = JKFlipFlop()
jk4 = JKFlipFlop()

def C1(clk):

	jk1.doTheThing( clk, 1, 1 )
	jk2.doTheThing( clk, jk1._q1, jk1._q1 )
	jk3.doTheThing( clk, and_(jk2._q1, jk1._q1), and_(jk2._q1, jk1._q1) )
	jk4.doTheThing( clk, and3_(jk3._q1, jk2._q1, jk1._q1), and3_(jk3._q1, jk2._q1, jk1._q1) )

	global delayRecording
	time.sleep(delayRecording)
	bitSeq = toString( [jk4.q1, jk3.q1, jk2.q1, jk1.q1] )
	print( toString( [bitSeq, "    ", toDecimal(bitSeq)] ) )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	C1(clock.value)

def callOnFalling():
	pass


clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 1 # seconds
clock.run()