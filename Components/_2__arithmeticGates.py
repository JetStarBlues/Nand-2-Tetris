''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Hack computer
from ._x__components import *


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


def incrementN_( N, x ):

	''' add one '''
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
	b_2s = negateN_( N, b )  # 2s complement
	return addN_( N, a, b_2s )



''''''''''''''''''''''''''''' negation '''''''''''''''''''''''''''''

# MSB to LSB

def negateN_( N, x ):

	''' 2s complement ->  -x = 2^n - x = ( 2^n - 1 ) - x + 1 '''

	## ( 2^n - 1 ) - x aka flip x's bits
	temp = tuple( not_( b ) for b in x )

	## Add 1
	return fastIncrement_( temp )     # uses shortcut
	# return incrementN_( N, temp )   # uses fullAdder_


def isNegative_( x ):

	''' 2s complement -> MSB is one if negative '''
	return x[0]



''''''''''''''''''''''''''' shift register '''''''''''''''''''''''''''

'''
	As is can shift max '1111' -> 15 on one command...
	So a call like shift(20) would need to be split up...
	  Thinking the user should do this when coding... or
	  could be stdlib fx that does this...

	If want to do shift(16) in one cycle, can add s4 support
	(and correspoinding 16muxes) to hardware... revusit as needed
'''

def shiftRightN_( N, x, s3, s2, s1, s0 ):

	''' Barrel shifter '''

	t0 = [None] * N
	t1 = [None] * N
	t2 = [None] * N
	t3 = [None] * N

	#
	for i in range( N - 1, 0, -1 ):
		t0[i] = mux_( x[i - 1], x[i], s0 )

	t0[0] = mux_( 0, x[0], s0 )

	#
	for i in range( N - 1, 1, -1 ):
		t1[i] = mux_( t0[i - 2], t0[i], s1 )

	t1[1] = mux_( 0, t0[1], s1 )
	t1[0] = mux_( 0, t0[0], s1 )

	#
	for i in range( N - 1, 3, -1 ):
		t2[i] = mux_( t1[i - 4], t1[i], s2 )

	t2[3] = mux_( 0, t1[3], s2 )
	t2[2] = mux_( 0, t1[2], s2 )
	t2[1] = mux_( 0, t1[1], s2 )
	t2[0] = mux_( 0, t1[0], s2 )	

	#
	for i in range( N - 1, 7, -1 ):
		t3[i] = mux_( t2[i - 8], t2[i], s3 )

	t3[7] = mux_( 0, t2[7], s3 )
	t3[6] = mux_( 0, t2[6], s3 )
	t3[5] = mux_( 0, t2[5], s3 )
	t3[4] = mux_( 0, t2[4], s3 )
	t3[3] = mux_( 0, t2[3], s3 )
	t3[2] = mux_( 0, t2[2], s3 )
	t3[1] = mux_( 0, t2[1], s3 )
	t3[0] = mux_( 0, t2[0], s3 )

	#
	return t3


def shiftLeftN_( N, x, s3, s2, s1, s0 ):

	''' Barrel shifter '''

	t0 = [None] * N
	t1 = [None] * N
	t2 = [None] * N
	t3 = [None] * N

	#
	t0[N - 1] = mux_( 0, x[N - 1], s0 )
	
	for i in range( N - 2, -1, -1 ):
		t0[i] = mux_( x[i + 1], x[i], s0 )

	#
	t1[N - 1] = mux_( 0, t0[N - 1], s1 )
	t1[N - 2] = mux_( 0, t0[N - 2], s1 )

	for i in range( N - 3, -1, -1 ):
		t1[i] = mux_( t0[i + 2], t0[i], s1 )

	#
	t2[N - 1] = mux_( 0, t1[N - 1], s2 )
	t2[N - 2] = mux_( 0, t1[N - 2], s2 )
	t2[N - 3] = mux_( 0, t1[N - 3], s2 )
	t2[N - 4] = mux_( 0, t1[N - 4], s2 )

	for i in range( N - 5, -1, -1 ):
		t2[i] = mux_( t1[i + 4], t1[i], s2 )

	#
	t3[N - 1] = mux_( 0, t2[N - 1], s3 )
	t3[N - 2] = mux_( 0, t2[N - 2], s3 )
	t3[N - 3] = mux_( 0, t2[N - 3], s3 )
	t3[N - 4] = mux_( 0, t2[N - 4], s3 )
	t3[N - 5] = mux_( 0, t2[N - 5], s3 )
	t3[N - 6] = mux_( 0, t2[N - 6], s3 )
	t3[N - 7] = mux_( 0, t2[N - 7], s3 )
	t3[N - 8] = mux_( 0, t2[N - 8], s3 )

	for i in range( N - 9, -1, -1 ):
		t3[i] = mux_( t2[i + 8], t2[i], s3 )

	#
	return t3



''''''''''''''''''''''' Arithmetic Logic Unit '''''''''''''''''''''''

# MSB to LSB

def ALU_( N, x, y, zx, nx, zy, ny, f, no ):

	''' N bit ALU '''

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

	 return ( out, zr, ng ) 
	'''

	# mux_( d1, d0, sel ) -> if( sel ): d1, else: d0

	x =   muxN_( N,  zeroN_( N )     ,  x               ,  zx                 )
	x =   muxN_( N,  notN_( N, x )   ,  x               ,  nx                 )
	y =   muxN_( N,  zeroN_( N )     ,  y               ,  zy                 )
	y =   muxN_( N,  notN_( N, y )   ,  y               ,  ny                 )
	out = muxN_( N,  addN_( N, x, y ),  andN_( N, x, y ),  f                  )
	out = muxN_( N,  notN_( N, out ) ,  out             ,  no                 )
	zr =  mux_(      1               ,  0               ,  isZero_( out )     )
	ng =  mux_(      1               ,  0               ,  isNegative_( out ) )

	return ( out, zr, ng )
