'''----------------------------- Imports -----------------------------'''

# Hack computer
# from ._x__components import *


'''----------------------------- Helpers -----------------------------'''


'''----------------------------- Adders -----------------------------'''


'''--------------------- Arithmetic Logic Unit ---------------------'''

# MSB to LSB

def ALU_( N, x, y, fub1, fub0, zx, nx, zy, ny, f, no ):

	''' N bit ALU '''

	if fub1 == 1 :

		if fub0 == 1 :

			if zx == 1 :   x = 0
			if nx == 1 :   x = not_( x )
			if zy == 1 :   y = 0
			if ny == 1 :   y = not_( y )
			if  f == 1 : out = add_( x, y )
			if  f == 0 : out = and_( x, y )
			if no == 1 : out = not_( out )

		elif fub0 == 0 :

			out = xor_( x, y )

	elif fub1 == 0 :

		if fub0 == 1 : 

			out = shiftLeft_( x, y )

		elif fub0 == 0 : 

			out = shiftRight_( x, y )

	if out == 0 : zr = 1
	if out < 0  : ng = 1

	return ( out, zr, ng ) 

