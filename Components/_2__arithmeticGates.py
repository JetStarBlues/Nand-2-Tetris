'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''----------------------------- Helpers -----------------------------'''


zeroN = [0] * N_BITS

oneN  = [0] * ( N_BITS - 1 ) + [1]

def isZero_( x ):
	return not_( orNto1_( x ) )



'''----------------------------- Adders -----------------------------'''

# MSB to LSB

def halfAdder_( a, b ):

	summ = xor_( a, b )
	carry = and_( a, b )
	return ( summ, carry )


def fullAdder_( a, b, cIn ):

	if PERFORMANCE_MODE:

		sm = int( a ) + int( b ) + int( cIn )
		summ  = sm % 2
		cOut = sm // 2
		return( summ, cOut )

	else:

		summ1, carry1 = halfAdder_( a, b )
		summ2, carry2 = halfAdder_( summ1, cIn )
		cOut = or_( carry1, carry2 )
		return ( summ2, cOut )


def rippleAdderN_( N, a, b ):

	''' N bit ripple adder '''
	summ = [None] * N
	carry = 0

	for i in range( N - 1, -1, -1 ):  # (N - 1)..0, R to L
		summ[i], carry = fullAdder_( a[i], b[i], carry )
	return summ


def fullAdderCLA_( a, b, cIn ):

	''' Modified fullAdder
	     Does not compute carry, instead returns propogate and generate values '''

	# TODO - if/else if performance terrible

	propogate = or_( a, b )
	generate = and_( a, b )

	summ = xor_( xor_( a, b ), cIn )

	return ( summ, propogate, generate )


def carryLookAheadAdder4_( a, b, c0 ):

	# https://www.cs.umd.edu/class/sum2003/cmsc311/Notes/Comb/lookahead.html
	# http://www.utdallas.edu/~poras/courses/ee3320/xilinx/upenn/lab4-CarryLookAheadAdder.htm

	'''
		Description from - http://www.edaboard.com/thread101846.html#post444410
		Step 1 - FAs take in a,b and output p,g (in parallel)
		Step 2 - CL takes in various p,g and computes carry for all FAs (in parallel)
		Step 3 - FAs calculate sum (in parallel)
	'''

	''' 
		c1 = g0 + p0c0
		c2 = g1 + p1g0 + p1p0c0
		c3 = g2 + p2g1 + p2p1g0 + p2p1p0c0
		c4 = g3 + p3g2 + p3p2g1 + p3p2p1g0 + p3p2p1p0c0
	'''

	'''
	_, p0, g0 = fullAdderCLA_( a[3], b[3], '0' )
	_, p1, g1 = fullAdderCLA_( a[2], b[2], '0' )
	_, p2, g2 = fullAdderCLA_( a[1], b[1], '0' )
	_, p3, g3 = fullAdderCLA_( a[0], b[0], '0' )

	c1 = or_(       g0, and_( p0, c0 ) )
	c2 = or3_(      g1, and_( p1, g0 ), and3_( p1, p0, c0 ) )
	c3 = orNto1_( ( g2, and_( p2, g1 ), and3_( p2, p1, g0 ), andNto1_( ( p2, p1, p0, c0 ) ) ) )
	c4 = orNto1_( ( g3, and_( p3, g2 ), and3_( p3, p2, g1 ), andNto1_( ( p3, p2, p1, g0 ) ), andNto1_( ( p3, p2, p1, p0, c0 ) ) ) )

	s0, _, _ = fullAdderCLA_( a[3], b[3], c0 )
	s1, _, _ = fullAdderCLA_( a[2], b[2], c1 )
	s2, _, _ = fullAdderCLA_( a[1], b[1], c2 )
	s3, _, _ = fullAdderCLA_( a[0], b[0], c3 )

	summ = [ s3, s2, s1, s0 ]
	cOut = c4

	p = andNto1_( ( p3, p2, p1, p0 ) )
	g = orNto1_( ( g3, and_( p3, g2 ), and3_( p3, p2, g1 ), andNto1_( ( p3, p2, p1, g0 ) ) ) )

	return ( summ, cOut, p, g )
	'''

	e = execInParallel()

	p = [ None ] * 4
	g = [ None ] * 4
	s = [ None ] * 4
	c = [ c0 ] + [ None ] * 4
	idx = list( range( 4 ) )

	def fx( i ):

		j = 3 - i
		_, p[i], g[i] = fullAdderCLA_( a[j], b[j], '0' )

	e.run( 4, fx, idx )

	# print( "huh", p, g )

	c[1] = or_(       g[0], and_( p[0], c[0] ) )
	c[2] = or3_(      g[1], and_( p[1], g[0] ), and3_( p[1], p[0], c[0] ) )
	c[3] = orNto1_( ( g[2], and_( p[2], g[1] ), and3_( p[2], p[1], g[0] ), andNto1_( ( p[2], p[1], p[0], c[0] ) ) ) )
	c[4] = orNto1_( ( g[3], and_( p[3], g[2] ), and3_( p[3], p[2], g[1] ), andNto1_( ( p[3], p[2], p[1], g[0] ) ), andNto1_( ( p[3], p[2], p[1], p[0], c[0] ) ) ) )

	def fx2( i ):

		j = 3 - i
		s[i], _, _ = fullAdderCLA_( a[j], b[j], c[i] )

	e.run( 4, fx2, idx )

	summ = tuple( s )
	cOut = c[4]

	pp = andNto1_( p )
	gg = orNto1_( ( g[3], and_( p[3], g[2] ), and3_( p[3], p[2], g[1] ), andNto1_( ( p[3], p[2], p[1], g[0] ) ) ) )

	# print( "hmm", summ, cOut, pp, gg )

	return ( summ, cOut, pp, gg )


def carryLookAheadAdder16_( a, b, c0 ):

	_, _, p0, g0 = carryLookAheadAdder4_( a[12:  ], b[12:  ], '0' )
	_, _, p1, g1 = carryLookAheadAdder4_( a[ 8:12], b[ 8:12], '0' )
	_, _, p2, g2 = carryLookAheadAdder4_( a[ 4:8 ], b[ 4:8 ], '0' )
	_, _, p3, g3 = carryLookAheadAdder4_( a[  :4 ], b[  :4 ], '0' )

	c1 = or_(       g0, and_( p0, c0 ) )
	c2 = or3_(      g1, and_( p1, g0 ), and3_( p1, p0, c0 ) )
	c3 = orNto1_( ( g2, and_( p2, g1 ), and3_( p2, p1, g0 ), andNto1_( ( p2, p1, p0, c0 ) ) ) )
	c4 = orNto1_( ( g3, and_( p3, g2 ), and3_( p3, p2, g1 ), andNto1_( ( p3, p2, p1, g0 ) ), andNto1_( ( p3, p2, p1, p0, c0 ) ) ) )

	s0, _, _, _ = carryLookAheadAdder4_( a[12:  ], b[12:  ], c0 )
	s1, _, _, _ = carryLookAheadAdder4_( a[ 8:12], b[ 8:12], c1 )
	s2, _, _, _ = carryLookAheadAdder4_( a[ 4:8 ], b[ 4:8 ], c2 )
	s3, _, _, _ = carryLookAheadAdder4_( a[  :4 ], b[  :4 ], c3 )

	cOut = c4
	summ = s3 + s2 + s1 + s0

	# p = andNto1_( ( p3, p2, p1, p0 ) )
	# g = orNto1_( ( g3, and_( p3, g2 ), and3_( p3, p2, g1 ), andNto1_( ( p3, p2, p1, g0 ) ) ) )

	# return ( summ, cOut, p, g )
	return ( summ )





def addN_( N, a, b ):

	# return rippleAdderN_( N, a, b )

	return carryLookAheadAdder16_( a, b, '0' )


def incrementN_( N, x ):

	''' add one '''
	if PERFORMANCE_MODE:
		return fastIncrement_( x )   # use shortcut

	else:
		return addN_( N, x, oneN )   # use addN_


def fastIncrement_( x ):

	''' Keep flipping RtoL till flip a zero '''

	# Is this implementable with logic gates? See vid 2.3
	#  Doubt it atm due to break-statement

	summ = list( x ) # mutable
	for i in range ( len( summ ) - 1, -1, -1 ): # RtoL
		summ[i] = not_( summ[i] )
		if summ[i] == 1: break # flipped a zero
	return summ



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



'''--------------------------- Negation ---------------------------'''

# MSB to LSB

def negateN_( N, x ):

	''' 2s complement ->  -x = 2^n - x = ( 2^n - 1 ) - x + 1 '''

	## ( 2^n - 1 ) - x aka flip x's bits
	temp = tuple( not_( b ) for b in x )

	## Add 1
	return incrementN_( N, temp )


def isNegative_( x ):

	''' 2s complement -> MSB is one if negative '''
	return x[0]



'''------------------------- Shift Register -------------------------'''

# MSB to LSB

'''
	As is can shift max '1111' -> 15 on one command...
	So a call like shift(20) would need to be split up...
	  Thinking the user should do this when coding... or
	  could be stdlib fx that does this...

	If want to do shift(16) in one cycle, can add s4 support
	(and correspoinding 16muxes) to hardware... revusit as needed
'''

def shiftRightN_( N, x, y ):

	''' Barrel shifter '''

	t0 = [None] * N
	t1 = [None] * N
	t2 = [None] * N
	t3 = [None] * N

	y = y[::-1] # make life simpler by matching array access to MSB-to-LSB format

	#
	for i in range( N - 1, 0, -1 ):
		t0[i] = mux_( x[i - 1], x[i], y[0] )

	t0[0] = mux_( 0, x[0], y[0] )

	#
	for i in range( N - 1, 1, -1 ):
		t1[i] = mux_( t0[i - 2], t0[i], y[1] )

	t1[1] = mux_( 0, t0[1], y[1] )
	t1[0] = mux_( 0, t0[0], y[1] )

	#
	for i in range( N - 1, 3, -1 ):
		t2[i] = mux_( t1[i - 4], t1[i], y[2] )

	t2[3] = mux_( 0, t1[3], y[2] )
	t2[2] = mux_( 0, t1[2], y[2] )
	t2[1] = mux_( 0, t1[1], y[2] )
	t2[0] = mux_( 0, t1[0], y[2] )	

	#
	for i in range( N - 1, 7, -1 ):
		t3[i] = mux_( t2[i - 8], t2[i], y[3] )

	t3[7] = mux_( 0, t2[7], y[3] )
	t3[6] = mux_( 0, t2[6], y[3] )
	t3[5] = mux_( 0, t2[5], y[3] )
	t3[4] = mux_( 0, t2[4], y[3] )
	t3[3] = mux_( 0, t2[3], y[3] )
	t3[2] = mux_( 0, t2[2], y[3] )
	t3[1] = mux_( 0, t2[1], y[3] )
	t3[0] = mux_( 0, t2[0], y[3] )

	#
	return t3


def shiftLeftN_( N, x, y ):

	''' Barrel shifter '''

	t0 = [None] * N
	t1 = [None] * N
	t2 = [None] * N
	t3 = [None] * N

	y = y[::-1] # make life simpler by matching array access to MSB-to-LSB format

	#
	t0[N - 1] = mux_( 0, x[N - 1], y[0] )
	
	for i in range( N - 2, -1, -1 ):
		t0[i] = mux_( x[i + 1], x[i], y[0] )

	#
	t1[N - 1] = mux_( 0, t0[N - 1], y[1] )
	t1[N - 2] = mux_( 0, t0[N - 2], y[1] )

	for i in range( N - 3, -1, -1 ):
		t1[i] = mux_( t0[i + 2], t0[i], y[1] )

	#
	t2[N - 1] = mux_( 0, t1[N - 1], y[2] )
	t2[N - 2] = mux_( 0, t1[N - 2], y[2] )
	t2[N - 3] = mux_( 0, t1[N - 3], y[2] )
	t2[N - 4] = mux_( 0, t1[N - 4], y[2] )

	for i in range( N - 5, -1, -1 ):
		t2[i] = mux_( t1[i + 4], t1[i], y[2] )

	#
	t3[N - 1] = mux_( 0, t2[N - 1], y[3] )
	t3[N - 2] = mux_( 0, t2[N - 2], y[3] )
	t3[N - 3] = mux_( 0, t2[N - 3], y[3] )
	t3[N - 4] = mux_( 0, t2[N - 4], y[3] )
	t3[N - 5] = mux_( 0, t2[N - 5], y[3] )
	t3[N - 6] = mux_( 0, t2[N - 6], y[3] )
	t3[N - 7] = mux_( 0, t2[N - 7], y[3] )
	t3[N - 8] = mux_( 0, t2[N - 8], y[3] )

	for i in range( N - 9, -1, -1 ):
		t3[i] = mux_( t2[i + 8], t2[i], y[3] )

	#
	return t3



'''--------------------- Arithmetic Logic Unit ---------------------'''

# MSB to LSB

def ALU_( N, x, y, fub1, fub0, zx, nx, zy, ny, f, no ):

	''' N bit ALU '''

	'''
	 out, zr, ng = [ None, 0, 0 ]

	 if fub1 == 1 :
	 	if fub0 == 1 :
 	 		if zx == 1 :   x = zeroN_( N )
 	 		if nx == 1 :   x = notN_( N, x )
 	 		if zy == 1 :   y = zeroN_( N )
 	 		if ny == 1 :   y = notN_( N, y )
 	 		if  f == 1 : out = addN_( N, x, y )  # out = x + y
 	 		if  f == 0 : out = andN_( N, x, y )  # out = x & y
 	 		if no == 1 : out = notN_( N, out )   # out = !out

		if fub0 == 0 :
			out = xorN_( N, x, y )

	 if fub1 == 0 :
	 	if fub0 == 1 : out = shiftLeftN_( N, x, y )
	 	if fub0 == 0 : out = shiftRightN_( N, x, y )

	 if out == 0 : zr = 1
 	 if out < 0  : ng = 1	
	 return ( out, zr, ng ) 
	'''

	if PERFORMANCE_MODE:

		return ALU_performance_( N, x, y, fub1, fub0, zx, nx, zy, ny, f, no )


	x0 = muxN_( N,  zeroN             ,  x                 ,  zx )
	x0 = muxN_( N,  notN_( N, x0 )    ,  x0                ,  nx )
	y0 = muxN_( N,  zeroN             ,  y                 ,  zy )
	y0 = muxN_( N,  notN_( N, y0 )    ,  y0                ,  ny )
	t2 = muxN_( N,  addN_( N, x0, y0 ),  andN_( N, x0, y0 ),  f  )
	t2 = muxN_( N,  notN_( N, t2 )    ,  t2                ,  no )

	t1 = muxN_( N,

		t2,
		xorN_( N, x, y ),
		fub0
	)

	t0 = muxN_( N,

		shiftLeftN_( N, x, y ),
		shiftRightN_( N, x, y ),
		fub0
	)

	out = muxN_( N, t1, t0, fub1 )
	zr =  mux_( 1, 0, isZero_( out ) )
	ng =  mux_( 1, 0, isNegative_( out ) )

	return ( out, zr, ng )


def ALU_performance_( N, x, y, fub1, fub0, zx, nx, zy, ny, f, no ):

	x0 = muxN_performance_( N,  zeroN                   ,  x                       ,  zx )
	x0 = muxN_performance_( N,  ( notN_, ( N, x0 ) )    ,  x0                      ,  nx )
	y0 = muxN_performance_( N,  zeroN                   ,  y                       ,  zy )
	y0 = muxN_performance_( N,  ( notN_, ( N, y0 ) )    ,  y0                      ,  ny )
	t2 = muxN_performance_( N,  ( addN_, ( N, x0, y0 ) ),  ( andN_, ( N, x0, y0 ) ),  f  )
	t2 = muxN_performance_( N,  ( notN_, ( N, t2 ) )    ,  t2                      ,  no )

	t1 = muxN_performance_( N,

		t2,
		( xorN_, ( N, x, y ) ),
		fub0
	)

	t0 = muxN_performance_( N,

		( shiftLeftN_, ( N, x, y ) ),
		( shiftRightN_, ( N, x, y ) ),
		fub0
	)

	out = muxN_performance_( N, t1, t0, fub1 )
	zr =  mux_( 1, 0, isZero_( out ) )
	ng =  mux_( 1, 0, isNegative_( out ) )

	return ( out, zr, ng )


# def ALU_( N, x, y, zx, nx, zy, ny, f, no ):

# 	''' N bit ALU '''

# 	'''
# 	 out, zr, ng = [ None, 0, 0 ]
#  	 if zx == 1 : x = zeroN_( N )
#  	 if nx == 1 : x = notN_( N, x )
#  	 if zy == 1 : y = zeroN_( N )
#  	 if ny == 1 : y = notN_( N, y )
#  	 if  f == 1 : out = addN_( N, x, y )  # out = x + y
#  	 if  f == 0 : out = andN_( N, x, y )  # out = x & y
#  	 if no == 1 : out = notN_( N, out )   # out = !out
#  	 if out == 0: zr = 1
#  	 if out < 0 : ng = 1

# 	 return ( out, zr, ng ) 
# 	'''

# 	# mux_( d1, d0, sel ) -> if( sel ): d1, else: d0

# 	x =   muxN_( N,  zeroN_( N )     ,  x               ,  zx                 )
# 	x =   muxN_( N,  notN_( N, x )   ,  x               ,  nx                 )
# 	y =   muxN_( N,  zeroN_( N )     ,  y               ,  zy                 )
# 	y =   muxN_( N,  notN_( N, y )   ,  y               ,  ny                 )
# 	out = muxN_( N,  addN_( N, x, y ),  andN_( N, x, y ),  f                  )
# 	out = muxN_( N,  notN_( N, out ) ,  out             ,  no                 )
# 	zr =  mux_(      1               ,  0               ,  isZero_( out )     )
# 	ng =  mux_(      1               ,  0               ,  isNegative_( out ) )

# 	return ( out, zr, ng )
