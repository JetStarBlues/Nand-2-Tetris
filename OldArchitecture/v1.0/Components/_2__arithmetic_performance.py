''' Arithmetic implemented using Python builtin functions instead of logic gates '''

'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''----------------------------- Helpers -----------------------------'''

largestInt_ = 2 ** ( N_BITS - 1 ) - 1  # two's complement

def isNegative_( x ):

	''' 2s complement -> MSB is one if negative '''
	return int( x > largestInt_ )

def trim_( x ):

	''' discard overflow bits '''
	return x & negativeOne_



'''------------------------- Shift Registers -------------------------'''

def shiftRight_( x, y ):

	return x >> y  # logical shift


def shiftLeft_( x, y ):
	
	z = x << y

	return trim( z )



'''--------------------- Arithmetic Logic Unit ---------------------'''

# MSB to LSB

def ALU_( N, x, y, fub1, fub0, zx, nx, zy, ny, f, no ):

	''' N bit ALU '''

	out = None

	if fub1 == 1 :

		if fub0 == 1 :

			if  zx == 1 : x = 0
			if  nx == 1 : x = notN_( x )
			if  zy == 1 : y = 0
			if  ny == 1 : y = notN_( y )
			if   f == 1 : out = trim( x + y )
			elif f == 0 : out = x & y
			if  no == 1 : out = notN_( out )

		elif fub0 == 0 :

			out = x ^ y

	elif fub1 == 0 :

		if fub0 == 1 :

			out = shiftLeft_( x, y )

		elif fub0 == 0 :

			out = shiftRight_( x, y )

	zr = 1 if out == 0 else 0

	ng = isNegative_( out )

	return ( out, zr, ng )
