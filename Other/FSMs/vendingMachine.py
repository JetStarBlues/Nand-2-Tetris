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

user_input = [0,1,1,1,0,1,1,0,1,0,0,1,1,0,0,0,0,0,1,1,1,1,0,1,0,1,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,1]
user_input_idx = 0
x = [0] * 5

def logState( thing, state ):
	state = toString( state )

	if thing == 'state':
		if state == '000': print( 'rst' )
		elif state == '001': print( 'D' )
		elif state == '010': print( 'DN' )
		elif state == '011': print( 'N' )
		elif state == '100': print( 'ND' )
		elif state == '101': print( 'NNN' )
		elif state == '110': print( 'NN' )

	elif thing == 'input':
		if state == '00': print( 'you inserted a nickel' )
		elif state == '01': print( 'you inserted a dime' )
		elif state == '10': print( 'you inserted a quarter' )
		else: print( 'you inserted an invalid coin, say adios to your previous money' )

	elif thing == 'dispense':
		if state == '0': print( 'need moar cash' )
		elif state == '1': print( '*** tasty snack of your choice has been dispensed ***')

	elif thing == 'change':
		if state == '000': pass # print( 'no change bud' )
		elif state == '001': print( 'your change is 5 cents' )
		elif state == '010': print( 'your change is 10 cents' )
		elif state == '011': print( 'your change is 15 cents' )
		elif state == '100': print( 'your change is 20 cents' )


def customPLA( x4, x3, x2, x1, x0 ):

	# https://www.cs.umd.edu/class/sum2003/cmsc311/Notes/Comb/pla.html
	'''
	z6 = 01100 + 01100 + 11000 # s2
	z5 = 00000 + 00100 + 01100 # s1
	z4 = 00000 + 00001 + 11000 # s0

	z3 = 00010 + 00101 + 00110 + 01000 + 01001 + 01010 + 01110 + 10000 + 10001 + 10010 + 10100 + 10101 + 10110 + 11001 + 11010 # dispense

	z2 = 01010 + 10010 + 10110 # c2
	z1 = 00110 + 01110 + 11010 # c1
	z0 = 00010 + 00110 + 01001 + 10001 + 10101 + 11010 # c0  '''

	# s2 s1 s0
	z6 = orNto1_( [
		andNto1_( [ not_( x4 ), x3, x2, not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, x2, not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ x4, x3, not_( x2 ), not_( x1 ), not_( x0 ) ] ),
	] )
	z5 = orNto1_( [
		andNto1_( [ not_( x4 ), not_( x3 ), not_( x2 ), not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), not_( x3 ), x2, not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, x2, not_( x1 ), not_( x0 ) ] )
	] )
	z4 = orNto1_( [
		andNto1_( [ not_( x4 ), not_( x3 ), not_( x2 ), not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), not_( x3 ), not_( x2 ), not_( x1 ), x0 ] ),
		andNto1_( [ x4, x3, not_( x2 ), not_( x1 ), not_( x0 ) ] )
	] )

	# dispense
	z3 = orNto1_( [
		andNto1_( [ not_( x4 ), not_( x3 ), not_( x2 ), x1, not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), not_( x3 ), x2, not_( x1 ), x0 ] ),
		andNto1_( [ not_( x4 ), not_( x3 ), x2, x1, not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, not_( x2 ), not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, not_( x2 ), not_( x1 ), x0 ] ),
		andNto1_( [ not_( x4 ), x3, not_( x2 ), x1, not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, x2, x1, not_( x0 ) ] ),
		andNto1_( [ x4, not_( x3 ), not_( x2 ), not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ x4, not_( x3 ), not_( x2 ), not_( x1 ), x0 ] ),
		andNto1_( [ x4, not_( x3 ), not_( x2 ), x1, not_( x0 ) ] ),
		andNto1_( [ x4, not_( x3 ), x2, not_( x1 ), not_( x0 ) ] ),
		andNto1_( [ x4, not_( x3 ), x2, not_( x1 ), x0 ] ),
		andNto1_( [ x4, not_( x3 ), x2, x1, not_( x0 ) ] ),
		andNto1_( [ x4, x3, not_( x2 ), not_( x1 ), x0 ] ),
		andNto1_( [ x4, x3, not_( x2 ), x1, not_( x0 ) ] )
	] )

	#c2 c1 c0
	z2 = orNto1_( [
		andNto1_( [ not_( x4 ), x3, not_( x2 ), x1, not_( x0 ) ] ),
		andNto1_( [ x4, not_( x3 ), not_( x2 ), x1, not_( x0 ) ] ),
		andNto1_( [ x4, not_( x3 ), x2, x1, not_( x0 ) ] )
	] )
	z1 = orNto1_( [
		andNto1_( [ not_( x4 ), not_( x3 ), x2, x1, not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, x2, x1, not_( x0 ) ] ),
		andNto1_( [ x4, x3, not_( x2 ), x1, not_( x0 ) ] )
	] )
	z0 = orNto1_( [
		andNto1_( [ not_( x4 ), not_( x3 ), not_( x2 ), x1, not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), not_( x3 ), x2, x1, not_( x0 ) ] ),
		andNto1_( [ not_( x4 ), x3, not_( x2 ), not_( x1 ), x0 ] ),
		andNto1_( [ x4, not_( x3 ), not_( x2 ), not_( x1 ), x0 ] ),
		andNto1_( [ x4, not_( x3 ), x2, not_( x1 ), x0 ] ),
		andNto1_( [ x4, x3, not_( x2 ), x1, not_( x0 ) ] )
	] )

	return ( z6, z5, z4, z3, z2, z1, z0 )


def VM(clk):
	'''vending machine'''

	global user_input
	global user_input_idx
	global x
	
	x[1] = user_input[user_input_idx]
	x[0] = user_input[user_input_idx + 1]
	x[4] = dff[0].q1
	x[3] = dff[1].q1
	x[2] = dff[2].q1

	out = customPLA( x[4], x[3], x[2], x[1], x[0] )
	
	dff[0].doTheThing( clk, out[0] )
	dff[1].doTheThing( clk, out[1] )
	dff[2].doTheThing( clk, out[2] )

	#
	if user_input_idx < len( user_input ) - 2: 

		user_input_idx += 2

		# Record output
		global delayRecording
		time.sleep(delayRecording)
		logState( 'input', [ x[1], x[0] ] )
		# logState( 'state', [ out[0], out[1], out[2] ] )
		logState( 'dispense', [ out[3] ] )
		logState( 'change', [ out[4], out[5], out[6] ] )
		print('---')

	else:
		print(".")


''''''''''''''''''''''''' run '''''''''''''''''''''''''


# Things to execute on clock edges
def callOnRising():
	VM(clock.value)

def callOnFalling():
	pass


clock.callbackRising = callOnRising
clock.callbackFalling = callOnFalling


# Start program
clock.duration = 1 # seconds
clock.run()