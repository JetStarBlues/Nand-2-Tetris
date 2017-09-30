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

dA = DFlipFlop()
dB = DFlipFlop()

# start with all gates reset
dA.clear()
dB.clear()

def logState(a, b):
	state = str(a) + str(b)
	if state == '00': print('waiting for button to be pressed')
	elif state == '01': print('recording press')
	elif state == '10': print('waiting for button to be released')

score = 0
dataIn = [0,1,1,0,0,0,1,1,1,0,1] # button activity (1 isPressed)
dataIdx = len(dataIn) - 1  # load RtoL


def FSM(clk):

	global dataIn
	global dataIdx


	if dataIdx >= 0 :
		print(dataIn[dataIdx]) #

		dA.doTheThing( 
			clk, 
			and_( dataIn[dataIdx], or_( dA.q1, dB.q1 ) )
		)

		dB.doTheThing(
			clk,
			and3_( dataIn[dataIdx], dA._q1, dB._q1 )
		)

		dataIdx -= 1

	else: clock.stop() # stop the clock


def record():

	global score

	logState( dA.q1, dB.q1 )

	score += and_( dA._q1, dB.q1 )  # could do this with counter circuit
	print("score ", score)


''''''''''''''''''''''''' run '''''''''''''''''''''''''

# Things to execute on clock edges
def callOnRising():
	FSM(clock.value)

def callOnFalling():
	record()

clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


if __name__ == '__main__': 

	# Start program
	clock.run()