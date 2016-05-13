''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys

# Computer files
sys.path.append('../Modules')
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _3__clock import *
from _4__flipFlops import *


''''''''''''''''''''''''' helpers '''''''''''''''''''''''''

def toString(array):
	return ''.join( map(str, array) )

def toDecimal(bitSeq):
	return int(bitSeq, 2)

def toBinary(N, x):
	return bin(x)[2:].zfill(N)


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

has_quit = False

def getInput():
	user_input = input()
	parseCmd( user_input )


def parseCmd( cmd ):
	
	cmd = cmd.split() # assume args seperated by spaces

	if cmd[0] == 'quit': 
		quit()

	elif cmd[0] == 'add':
		add( cmd[1], cmd[2] )

	elif cmd[0] == 'hello':
		hello()

	else:
		print('n/a')

	#
	if not has_quit: getInput()


def quit():
	global has_quit
	has_quit = True

def hello():
	print("hi there")

def add(a, b):
	sum_ = float(a) + float(b)
	print( sum_ )


##
getInput()
