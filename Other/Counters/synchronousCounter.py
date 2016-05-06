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


''''''''''''''''''''''''' main '''''''''''''''''''''''''

clock = Clock()

jk1 = JKFlipFlop()
jk2 = JKFlipFlop()
jk3 = JKFlipFlop()
jk4 = JKFlipFlop()

# start with all gates reset
jk1.clear()
jk2.clear()
jk3.clear()
jk4.clear()

n_iterations = 0


def C1(clk):

	jk1.doTheThing( clk, 1, 1 )
	jk2.doTheThing( clk, jk1._q1, jk1._q1 )
	jk3.doTheThing( clk, and_(jk2._q1, jk1._q1), and_(jk2._q1, jk1._q1) )
	jk4.doTheThing( clk, and3_(jk3._q1, jk2._q1, jk1._q1), and3_(jk3._q1, jk2._q1, jk1._q1) )

	global n_iterations
	n_iterations += 1
	if n_iterations >= 1000: clock.stop() # stop the clock


def record():
	bitSeq = toString( [jk4.q1, jk3.q1, jk2.q1, jk1.q1] )
	print( toString( [bitSeq, "    ", toDecimal(bitSeq)] ) )


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	C1(clock.value)

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


if __name__ == '__main__': 

	# Start program
	clock.run()