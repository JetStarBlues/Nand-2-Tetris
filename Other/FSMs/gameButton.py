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
dataIn = [1,1,1,0,1] # button activity (1 isPressed)
dataIdx = len(dataIn) - 1  # load RtoL

def FSM(clk):

	global dataIn
	global dataIdx

	global score

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
	else:
		# treat no input as 0
		
		print(0) #

		dA.doTheThing( clk, 0 )
		dB.doTheThing( clk, 0 )


	global delayRecording
	time.sleep(delayRecording)
	logState( dA.q1, dB.q1 )

	score += and_( dA._q1, dB.q1 )  # could do this with counter circuit
	print("score ", score)


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