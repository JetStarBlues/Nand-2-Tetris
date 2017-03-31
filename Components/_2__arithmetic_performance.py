''' Arithmetic implemented using Python builtin functions instead of logic gates '''

'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''------------------------- Shift Registers -------------------------'''

def shiftRight_( x, y ):

	return x >> y


def shiftLeft_( x, y ):
	
	z = x << y

	# Cap at N_BITS since operating system that emulator is running on
	#  likely has a different nBits ( ex. 32/64bit )
	z = bin( z )[ 2 : ]  # convert to binary string and remove '0B' header
	z = z[ - N_BITS : ]  # get last N_BITS

	return int( z, 2 )



'''--------------------- Arithmetic Logic Unit ---------------------'''

# MSB to LSB

def ALU_( N, x, y, fub1, fub0, zx, nx, zy, ny, f, no ):

	''' N bit ALU '''

	if fub1 == 1 :

		if fub0 == 1 :

			if zx == 1 :   x = 0
			if nx == 1 :   x = notN_( x )
			if zy == 1 :   y = 0
			if ny == 1 :   y = notN_( y )
			if  f == 1 : out = x + y
			if  f == 0 : out = x & y
			if no == 1 : out = notN_( out )

		elif fub0 == 0 :

			out = x ^ y

	elif fub1 == 0 :

		if fub0 == 1 : 

			out = shiftLeft_( x, y )

		elif fub0 == 0 : 

			out = shiftRight_( x, y )

	zr = 1 if out == 0 else 0

	ng = 1 if out  < 0 else 0

	return ( out, zr, ng ) 

