'''----------------------------- Imports -----------------------------'''

# Built ins
import math

# Hack computer
from ._x__components import *



'''----------------------------- Helpers -----------------------------'''

def zeroN_( N ):

	return ( 0, ) * N

def oneN_( N ):

	return ( 0, ) * ( N - 1 ) + ( 1, )

def isZeroN_( N, x ):

	return not_( orNto1_( N, x ) )

def isNegative_( x ):

	# Twos complement, MSB is one if negative
	return x[ 0 ]



'''----------------------------- Adders -----------------------------'''

# MSB to LSB

def halfAdder_( a, b ):

	summ = xor_( a, b )
	carry = and_( a, b )
	return ( summ, carry )


def fullAdder_( a, b, cIn ):

	summ1, carry1 = halfAdder_( a, b )
	summ2, carry2 = halfAdder_( summ1, cIn )
	cOut = or_( carry1, carry2 )
	return ( summ2, cOut )


def rippleCarryAdderN_( N, a, b ):

	''' N bit ripple adder '''

	summ = [ None ] * N
	carry = 0

	for i in range( N - 1, - 1, - 1 ):  # (N - 1)..0, R to L

		summ[i], carry = fullAdder_( a[i], b[i], carry )

	return summ


def addN_( N, a, b ):

	return rippleCarryAdderN_( N, a, b )


def incrementN_( N, x ):

	''' Add one '''

	# Use addN_ --
	# return addN_( N, x, oneN_( N ) )

	# Use shortcut --
	# return fastIncrement_( x )

	# Use cascaded half adders --
	summ = [ None ] * N
	carry = 1  # add one

	for i in range ( N - 1, - 1, - 1 ):  # (N - 1)..0, R to L

		summ[i], carry = halfAdder_( x[i], carry )

	return summ


def fastIncrement_( x ):

	''' Keep flipping RtoL till flip a zero '''

	# Is this implementable with logic gates? See vid 2.3
	#  Doubt it atm due to break-statement

	x = list( x )  # mutable

	for i in range ( len( x ) - 1, - 1, - 1 ): # RtoL

		x[i] = not_( x[i] )

		if x[i] == 1: # flipped a zero

			break

	return tuple( x )



'''--------------------------- Subtractors ---------------------------'''

# MSB to LSB

def halfSubtractor_( a, b ):

	# a - b
	diff = xor_( a, b )
	borrow = and_( not_( a ), b )
	return ( diff, borrow )


def fullSubtractor_( a, b, c ):

	# c is the borrow bit from the previous circuit
	diff1, borrow1 = halfSubtractor_( a, b )
	diff2, borrow2 = halfSubtractor_( diff1, c )
	borrow = or_( borrow1, borrow2 )
	return ( diff2, borrow )


def subtractN_( N, a, b ):

	''' N bit subractor, takes and outputs Nbit numbers
	     if a < b, answer returned is in 2s complement
	'''
	diff = [ None ] * N
	borrow = 0

	for i in range( N - 1, - 1, - 1 ):  # (N - 1)..0, R to L

		diff[i], borrow = fullSubtractor_( a[i], b[i], borrow )

	return diff


def subtractN_v2_( N, a, b ):

	''' 2s complement addition
	     ex. 7 - 5 = 7 + (-5) = 7 + (2**n - 5) 
	'''
	b_2s = negateN_( N, b )  # 2s complement
	return addN_( N, a, b_2s )



'''--------------------------- Negation ---------------------------'''

# MSB to LSB

def negateN_( N, x ):

	''' 2s complement ->  -x = 2^n - x = ( 2^n - 1 ) - x + 1 '''

	## ( 2^n - 1 ) - x aka flip x's bits
	temp = tuple( not_( b ) for b in x )

	## Add 1
	return incrementN_( N, temp )



'''------------------------- Shift Registers -------------------------'''

# MSB to LSB

def shiftRightN_( N, x, y ):

	''' N bit barrel shifter (right) '''

	ns = int( math.log( N , 2 ) )  # number of shift bits

	t = []

	for i in range( ns ):

		t.append( [ None ] * N )

	for j in range( ns ):

		p2 = 2 ** j

		h = x if j == 0 else t[ j - 1 ]

		y_idx = N - j - 1

		for i in range( N - 1, p2 - 1, - 1 ):

			t[ j ][ i ] = mux_( h[ i - p2 ], h[ i ], y[ y_idx ] )

		for k in range( p2 - 1, - 1, - 1 ):

			t[ j ][ k ] = mux_( 0, h[ k ], y[ y_idx ] )

	return t[ ns - 1 ]


def shiftLeftN_( N, x, y ):

	''' N bit barrel shifter (left) '''

	ns = int( math.log( N , 2 ) )  # number of shift bits

	t = []

	for i in range( ns ):

		t.append( [ None ] * N )

	for j in range ( ns ):

		p2 = 2 ** j

		h = x if j == 0 else t[ j - 1 ]

		y_idx = N - j - 1

		for k in range( N - 1, N - 1 - p2 , - 1 ):

			t[ j ][ k ] = mux_( 0, h[ k ], y[ y_idx ] )

		for i in range( N - 1 - p2, - 1, - 1 ):

			t[ j ][ i ] = mux_( h[ i + p2 ], h[ i ], y[ y_idx ] )

	return t[ ns - 1 ]



'''--------------------- Arithmetic Logic Unit ---------------------'''

# MSB to LSB

def ALU_( N, x, y, control ):

	''' N bit ALU '''

	'''
		fx
			 0 -  add
			 1 -  and
			 2 -  xor
			 3 -  lsr
			 4 -  lsl
			 5 -  mul
			 6 -  div
			 7 -  fpAdd
			 8 -  fpSub
			 9 -  fpMul
			10 -  fpDiv

		lookup ROM
			op       fsel   flags                composite
			-----    ----   -----                ----------
			0        add    zx,     zy           0000 10100
			1        add    zx, nx, zy, ny, no   0000 11111
			- 1      add    zx, nx, zy           0000 11100
			x        and            zy, ny       0001 00110
			! x      and            zy, ny, no   0001 00111
			- x      add            zy, ny, no   0000 00111
			x + 1    add        nx, zy, ny, no   0000 01111
			x - 1    add            zy, ny       0000 00110
			x + y    add                         0000 00000
			x - y    add        nx,         no   0000 01001
			x & y    and                         0001 00000
			x | y    and        nx,     ny, no   0001 01011
			x ^ y    xor                         0010 00000
			x >> y   lsr                         0011 00000
			x << y   lsl                         0100 00000
			x * y    mul                         0101 00000
			x / y    div                         0110 00000

	'''

	# decode
	fx = control[ 0 : 4 ]
	zx = control[ 4 ]
	nx = control[ 5 ]
	zy = control[ 6 ]
	ny = control[ 7 ]
	no = control[ 8 ]

	# constants, not, negate, and, or, add, sub
	x0 = muxN_( N,  zeroN_( N ),     x,   zx )
	x0 = muxN_( N,  notN_( N, x0 ),  x0,  nx )
	y0 = muxN_( N,  zeroN_( N ),     y,   zy )
	y0 = muxN_( N,  notN_( N, y0 ),  y0,  ny )

	z0 = addN_( N, x0, y0 )
	z0 = muxN_( N,  notN_( N, z0 ),  z0,  no )

	z1 = andN_( N, x0, y0 )
	z1 = muxN_( N,  notN_( N, z1 ),  z1,  no )

	# xor
	z2 = xorN_( N, x, y )

	# logical shift
	z3 = shiftRightN_( N, x, y )
	z4 = shiftLeftN_( N, x, y )

	# Select output
	out = muxN16to1_(

		N,

		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		zeroN_( N ),
		z4,
		z3,
		z2,
		z1,
		z0,

		fx[ 0 ], fx[ 1 ], fx[ 2 ], fx[ 3 ]
	)

	out_zr = mux_( 1, 0, isZeroN_( N, out ) )
	out_ng = mux_( 1, 0, isNegative_( out ) )

	return ( out, out_zr, out_ng )
