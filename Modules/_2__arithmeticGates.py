''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Computer files
from _1__elementaryGates import *


''''''''''''''''''''''''''''''' adders '''''''''''''''''''''''''''''''

def halfAdder_( a, b ):
	summ = xor_( a, b )
	carry = and_( a, b )
	return ( summ, carry )


def fullAdder_( a, b, c ):
	sumTemp, carryTemp1 = halfAdder_( a, b )
	summ, carryTemp2 = halfAdder_( c, sumTemp )
	carry = or_( carryTemp1, carryTemp2 )
	return ( summ, carry )


def addN_( N, a, b ):
	''' N bit adder, takes and outputs Nbit numbers '''
	summ = [None] * N
	c = 0
	for i in range( N - 1, -1, -1 ):  # (N - 1)..0
		summ[i], c = fullAdder_( a[i], b[i], c )
	return summ


# def add16_( a, b ):
# 	''' 16 bit adder, takes and outputs 16bit numbers '''
# 	return addN_( 16, a, b )


def zeroN_( N ):
	return [0] * N


def oneN_( N ):
	return [0] * ( N - 1 ) + [1]


def increment_( x ):
	''' increment by one bit '''
	N = len( x )
	b = oneN_( N )
	return addN_( N, x, b )


''''''''''''''''''''''''''''' negation '''''''''''''''''''''''''''''

def addOne_( x ):
	''' is this implementable with logic gates? See vid 2.3
		Doubt it atm due to break-statement '''
	# special case, keep flipping RtoL till flip a zero

	summ = list( x ) # mutable
	for i in range ( len( summ ) - 1, -1, -1 ): # RtoL
		summ[i] = not_( summ[i] )
		if summ[i]: break # flipped a zero
	return summ


def negate_( x ):
	''' 2s complement ->  -x = 2^n - x = ( 2^n - 1 ) - x + 1 '''

	## ( 2^n - 1 ) - x aka flip x's bits
	temp = tuple( not_( b ) for b in x )

	## Add 1
	return addOne_( temp )   	  # uses addOne_, shortcut?
	# return increment_( temp )   # uses fullAdder_

'''
  implement carry-lookahead adder for faster speeds 
  -> even though more calcs takes less time see vid 2.6 '''


''''''''''''''''''''''' Arithmetic Logic Unit '''''''''''''''''''''''

def isZero_( x ):
	return not_( orNto1_( x ) )


def ALU_( x, y, zx, nx, zy, ny, f, no ):
	N = 16 # 16 bit ALU

	'''
	out, zr, ng = [ None, 0, 0 ]
	if zx == 1 : x = zeroN_( N )
	if nx == 1 : x = notN_( N, x )
	if zy == 1 : y = zeroN_( N )
	if ny == 1 : y = notN_( N, y )
	if  f == 1 : out = addN_( N, x, y )
	if  f == 0 : out = andN_( N, x, y )
	if no == 1 : out = notN_( N, out )
	if out == 0: zr = 1
	if out < 0 : ng = 1

	return ( out, zr, ng ) '''

	x =   muxN_( N, x,                zeroN_( N ),        zx             )
	x =   muxN_( N, x,                notN_( N, x ),      nx             )
	y =   muxN_( N, y,                zeroN_( N ),        zy             )
	y =   muxN_( N, y,                notN_( N, y ),      ny             )
	out = muxN_( N, andN_( N, x, y ), addN_( N, x, y ),   f              )
	out = muxN_( N, out,              notN_( N, out ),    no             )
	zr =  muxN_( N, zeroN_( N ),      oneN_( N ),         isZero_( out ) )
	ng =  muxN_( N, zeroN_( N ),      oneN_( N ),         out[0]         )  # leftmost bit is a one (2's complement)

	return ( out, zr, ng )
