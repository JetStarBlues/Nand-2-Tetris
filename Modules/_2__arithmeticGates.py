''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Computer files
from _1__elementaryGates import *


''''''''''''''''''''''''''''''' helpers '''''''''''''''''''''''''''''''

def zeroN_( N ):
	return [0] * N

def oneN_( N ):
	return [0] * ( N - 1 ) + [1]

def isZero_( x ):
	return not_( orNto1_( x ) )



''''''''''''''''''''''''''''''' adders '''''''''''''''''''''''''''''''

# MSB to LSB

def halfAdder_( a, b ):

	summ = xor_( a, b )
	carry = and_( a, b )
	return ( summ, carry )


def fullAdder_( a, b, c ):

	# c is the carry bit from the previous circuit
	summ1, carry1 = halfAdder_( a, b )
	summ2, carry2 = halfAdder_( summ1, c )
	carry = or_( carry1, carry2 )
	return ( summ2, carry )


def addN_( N, a, b ):

	''' N bit adder, takes and outputs Nbit numbers '''
	summ = [None] * N
	carry = 0

	for i in range( N - 1, -1, -1 ):  # (N - 1)..0, R to L
		summ[i], carry = fullAdder_( a[i], b[i], carry )
	return summ


def increment_( x ):

	''' add one '''
	N = len( x )
	b = oneN_( N )
	return addN_( N, x, b )


def fastIncrement_( x ):

	''' is this implementable with logic gates? See vid 2.3
		Doubt it atm due to break-statement '''
	# special case, keep flipping RtoL till flip a zero

	summ = list( x ) # mutable
	for i in range ( len( summ ) - 1, -1, -1 ): # RtoL
		summ[i] = not_( summ[i] )
		if summ[i]: break # flipped a zero
	return summ


'''
  implement carry-lookahead adder for faster speeds 
  -> even though more calcs takes less time see vid 2.6 '''



''''''''''''''''''''''''''''' subtractors '''''''''''''''''''''''''''''

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
	diff = [None] * N
	borrow = 0

	for i in range( N - 1, -1, -1 ):  # (N - 1)..0, R to L
		diff[i], borrow = fullSubtractor_( a[i], b[i], borrow )
	return diff


def subtractN_v2_( N, a, b ):

	''' 2s complement addition
	     ex. 7 - 5 = 7 + (-5) = 7 + (2**n - 5) 
	'''
	b_2s = negate_( b )  # 2s complement
	return addN_( N, a, b_2s )



''''''''''''''''''''''''''''' negation '''''''''''''''''''''''''''''

# MSB to LSB

def negate_( x ):

	''' 2s complement ->  -x = 2^n - x = ( 2^n - 1 ) - x + 1 '''

	## ( 2^n - 1 ) - x aka flip x's bits
	temp = tuple( not_( b ) for b in x )

	## Add 1
	return fastIncrement_( temp ) # uses shortcut
	# return increment_( temp )   # uses fullAdder_


def isNegative_( x ):

	''' 2s complement -> MSB is one if negative '''
	return x[0]


''''''''''''''''''''''' Arithmetic Logic Unit '''''''''''''''''''''''

# MSB to LSB

def ALU_( x, y, zx, nx, zy, ny, f, no ):

	N = 16 # 16 bit ALU

	'''
	out, zr, ng = [ None, 0, 0 ]
	if zx == 1 : x = zeroN_( N )
	if nx == 1 : x = notN_( N, x )
	if zy == 1 : y = zeroN_( N )
	if ny == 1 : y = notN_( N, y )
	if  f == 1 : out = addN_( N, x, y )  # out = x + y
	if  f == 0 : out = andN_( N, x, y )  # out = x & y
	if no == 1 : out = notN_( N, out )   # out = !out
	if out == 0: zr = 1
	if out < 0 : ng = 1

	return ( out, zr, ng ) '''

	# mux_( d1, d0, sel ) -> if( sel ): d1, else: d0

	x =   muxN_( N,  zeroN_( N ),       x,                 zx                 )
	x =   muxN_( N,  notN_( N, x ),     x,                 nx                 )
	y =   muxN_( N,  zeroN_( N ),       y,                 zy                 )
	y =   muxN_( N,  notN_( N, y ),     y,                 ny                 )
	out = muxN_( N,  addN_( N, x, y ),  andN_( N, x, y ),  f                  )
	out = muxN_( N,  notN_( N, out ),   out,               no                 )
	zr =  muxN_( N,  oneN_( N ),        zeroN_( N ),       isZero_( out )     )
	ng =  muxN_( N,  oneN_( N ),        zeroN_( N ),       isNegative_( out ) )

	return ( out, zr, ng )
