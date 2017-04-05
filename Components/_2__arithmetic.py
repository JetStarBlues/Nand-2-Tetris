'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''----------------------------- Helpers -----------------------------'''

def zeroN_( N ):

	return ( '0', ) * N

def oneN_( N ):

	return ( '0', ) * ( N - 1 ) + ( '1', )

def isZero_( x ):

	return not_( orNto1_( x ) )

def isNegative_( x ):

	''' 2s complement -> MSB is one if negative '''
	return x[0]



'''----------------------------- Adders -----------------------------'''

# MSB to LSB

def halfAdder_( a, b ):

	summ = xor_( a, b )
	carry = and_( a, b )
	return ( summ, carry )


def fullAdder_( a, b, cIn ):

	# if PERFORMANCE_MODE:

	# 	sm = int( a ) + int( b ) + int( cIn )
	# 	summ  = sm % 2
	# 	cOut = sm // 2
	# 	return( summ, cOut )

	# else:

	summ1, carry1 = halfAdder_( a, b )
	summ2, carry2 = halfAdder_( summ1, cIn )
	cOut = or_( carry1, carry2 )
	return ( summ2, cOut )


def rippleCarryAdderN_( N, a, b ):

	''' N bit ripple adder '''
	summ = [ None ] * N
	carry = 0

	for i in range( N - 1, -1, -1 ):  # (N - 1)..0, R to L

		summ[i], carry = fullAdder_( a[i], b[i], carry )

	return summ


def addN_( N, a, b ):

	return rippleCarryAdderN_( N, a, b )


def incrementN_( N, x ):

	''' add one '''
	return addN_( N, x, oneN_( N ) )  # use addN_
	# return fastIncrement_( x )      # use shortcut


def fastIncrement_( x ):

	''' Keep flipping RtoL till flip a zero '''

	# Is this implementable with logic gates? See vid 2.3
	#  Doubt it atm due to break-statement

	summ = list( x ) # mutable

	for i in range ( len( summ ) - 1, -1, -1 ): # RtoL

		summ[i] = not_( summ[i] )

		if summ[i] == 1: # flipped a zero

			break

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
	diff = [ None ] * N
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

		for i in range( N - 1, p2 - 1, -1 ):

			t[ j ][ i ] = mux_( h[ i - p2 ], h[ i ], y[ y_idx ] )

		for k in range( p2 - 1, -1, -1 ):

			t[ j ][ k ] = mux_( 0, h[ k ], y[ y_idx ] )

	return t[ ns - 1 ]


def shiftLeftN_( N, x, y ):

	''' N bit barrel shifter (left) '''

	ns = int( math.log( N , 2 ) )  # number of shift bits

	N1 = N - 1

	t = []

	for i in range( ns ):

		t.append( [ None ] * N )

	for j in range ( ns ):

		p2 = 2 ** j

		h = x if j == 0 else t[ j - 1 ]

		y_idx = N - j - 1

		for k in range( p2 - 1, -1, -1 ):

			t[ j ][ N1 - k ] = mux_( 0, h[ N1 - k ], y[ y_idx ] )

		for i in range( N1 - p2, - 1, -1 ):

			t[ j ][ i ] = mux_( h[ i + p2 ], h[ i ], y[ y_idx ] )

	return t[ ns - 1 ]	



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

	x0 = muxN_( N,  zeroN_( N )       ,  x                 ,  zx )
	x0 = muxN_( N,  notN_( N, x0 )    ,  x0                ,  nx )
	y0 = muxN_( N,  zeroN_( N )       ,  y                 ,  zy )
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
