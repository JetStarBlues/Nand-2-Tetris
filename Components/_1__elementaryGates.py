''''''''''''''''''''' The elementary logic gates '''''''''''''''''''''

def and_( a, b ):
	return ( int( a ) & int( b ) )

def or_( a, b ):
	return ( int( a ) | int( b ) )	

def xor_( a, b ):
	return ( int( a ) ^ int( b ) )

def not_( x ):
	return 1 if int( x ) == 0 else 0	


''''''''''''''''''''''''' And their inverses '''''''''''''''''''''''''

def nand_( a, b ):
	return not_( and_( a, b ) )

def nor_( a, b ):
	return not_( or_( a, b ) )

def xnor_( a, b ):
	return not_( xor_( a, b ) )



''''''''''''''''''''''''' Encoders & Decoders '''''''''''''''''''''''''	

# MSB to LSB

def decoder1to2_( d ):
	q1 = d
	q0 = not_( d )
	return ( q1, q0 )


def decoder2to4_( d1, d0 ):
	q3 = and_(       d1  ,       d0   )
	q2 = and_(       d1  , not_( d0 ) )
	q1 = and_( not_( d1 ),       d0   )
	q0 = and_( not_( d1 ), not_( d0 ) )
	return ( q3, q2, q1, q0 )


def decoder3to8_( d2, d1, d0 ):
	q7 = and3_(       d2  ,       d1  ,       d0   )
	q6 = and3_(       d2  ,       d1  , not_( d0 ) )
	q5 = and3_(       d2  , not_( d1 ),       d0   )
	q4 = and3_(       d2  , not_( d1 ), not_( d0 ) )
	q3 = and3_( not_( d2 ),       d1  ,       d0   ) 
	q2 = and3_( not_( d2 ),       d1  , not_( d0 ) )
	q1 = and3_( not_( d2 ), not_( d1 ),       d0   )
	q0 = and3_( not_( d2 ), not_( d1 ), not_( d0 ) )
	return ( q7, q6, q5, q4, q3, q2, q1, q0 )


def encoder2to1_( d1, d0 ):
	return d1

def encoder4to2_( d3, d2, d1, d0 ):
	q1 = or_( d3, d2 )
	q0 = or_( d3, d1 )
	return ( q1, q0 )


def encoder8to3_( d7, d6, d5, d4, d3, d2, d1, d0 ):
	q2 = or_( d7, or3_( d6, d5, d4 ) )
	q1 = or_( d7, or3_( d6, d3, d2 ) )
	q0 = or_( d7, or3_( d5, d3, d1 ) )
	return ( q2, q1, q0 )



''''''''''''''''''''' Multiplexers & Demultiplexers '''''''''''''''''''''

# MSB to LSB

def mux_( d1, d0, sel ):

	''' 2to1 multiplexor is equivalent to an if/else statement of form,
			out = d0 if sel == 0
				  d1 if sel == 1			  

		Or in boolean algebra
			out = ( !s * d0 ) + ( s * d1 )
	''' 
	out = or_( 
		and_( not_( sel ), d0 ),
		and_( sel, d1 )
	)
	return out


def mux4to1_( d3, d2, d1, d0, s1, s0 ):

	''' out = d0 if sel == 00
		      d1 if sel == 01
		      d2 if sel == 10
		      d3 if sel == 11  '''

	''' using elementary gates '''
	p0 = and3_( d0, not_( s1 ), not_( s0 ) )
	p1 = and3_( d1, not_( s1 ),       s0   )
	p2 = and3_( d2,       s1  , not_( s0 ) )
	p3 = and3_( d3,       s1  ,       s0   )
	return or_( or_( p0, p1 ), or_( p2, p3 ) )

	''' using decoder '''
	# q = decoder2to4_( s1, s0 )
	# q = q[::-1] # reverse so that array indices correspond with bit position (aesthetics only)
	# p0 = and_( q[0], d0 )
	# p1 = and_( q[1], d1 )
	# p2 = and_( q[2], d2 )
	# p3 = and_( q[3], d3 )
	# return or_( or_( p0, p1 ), or_( p2, p3 ) )

	''' using other mux chips '''
	# p1 = mux_( d3, d2, s0 )
	# p2 = mux_( d1, d0, s0 )
	# return mux_( p1, p2, s1 )


def mux8to1_( d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 ):

	''' out = d0 if sel == 000
		      d1 if sel == 001
		      d2 if sel == 010
		      d3 if sel == 011
		      d4 if sel == 100
		      d5 if sel == 101
		      d6 if sel == 110
		      d7 if sel == 111  '''

	''' using elementary gates '''
	# p0 = and_( d0, and3_( not_( s2 ), not_( s1 ), not_( s0 ) ) )
	# p1 = and_( d1, and3_( not_( s2 ), not_( s1 ),       s0   ) )
	# p2 = and_( d2, and3_( not_( s2 ),       s1  , not_( s0 ) ) )
	# p3 = and_( d3, and3_( not_( s2 ),       s1  ,       s0   ) )
	# p4 = and_( d4, and3_(       s2  , not_( s1 ), not_( s0 ) ) )
	# p5 = and_( d5, and3_(       s2  , not_( s1 ),       s0   ) )
	# p6 = and_( d6, and3_(       s2  ,       s1  , not_( s0 ) ) )
	# p7 = and_( d7, and3_(       s2  ,       s1  ,       s0   ) )
	# return orNto1_( [ p0, p1, p2, p3, p4, p5, p6, p7 ] )

	''' using decoder '''
	# q = decoder3to8_( s2, s1, s0 )
	# q = q[::-1] # reverse so that array indices correspond with bit position (aesthetics only)
	# p0 = and_( q[0], d0 )
	# p1 = and_( q[1], d1 )
	# p2 = and_( q[2], d2 )
	# p3 = and_( q[3], d3 )
	# p4 = and_( q[4], d4 )
	# p5 = and_( q[5], d5 )
	# p6 = and_( q[6], d6 )
	# p7 = and_( q[7], d7 )
	# return orNto1_( [ p0, p1, p2, p3, p4, p5, p6, p7 ] )

	''' using other mux chips '''
	p1 = mux4to1_( d7, d6, d5, d4, s1, s0 )
	p2 = mux4to1_( d3, d2, d1, d0, s1, s0 )
	return mux_( p1, p2, s2 )


def dMux_( x, sel ):

	'''	out = [ 0, x ] if sel == 0
			  [ x, 0 ] if sel == 1
	'''
	d0 = and_( x, not_( sel ) )
	d1 = and_( x, sel )
	return ( d1, d0 )


def dMux1to4_( x, s1, s0 ):

	'''	out = [ 0, 0, 0, x ] if sel == 00
			  [ 0, 0, x, 0 ] if sel == 01
			  [ 0, x, 0, 0 ] if sel == 10
			  [ x, 0, 0, 0 ] if sel == 11
	'''

	''' using elementary gates '''
	d0 = and3_( x, not_( s1 ), not_( s0 ) )
	d1 = and3_( x, not_( s1 ),       s0   )
	d2 = and3_( x,       s1  , not_( s0 ) )
	d3 = and3_( x,       s1  ,       s0   )
	return ( d3, d2, d1, d0 )

	''' using decoder '''
	# q = decoder2to4_( s1, s0 )
	# q = q[::-1] # reverse so that array indices correspond with bit position (aesthetics only)
	# d0 = and_( q[0], x )
	# d1 = and_( q[1], x )
	# d2 = and_( q[2], x )
	# d3 = and_( q[3], x )
	# return ( d3, d2, d1, d0 )		

	''' using other dMux chips '''
	# p1 = dMux_( x, s1 )
	# p2 = dMux_( p1[0], s0 )
	# p3 = dMux_( p1[1], s0 )
	# return ( p2[0], p2[1], p3[0], p3[1] ) # d3, d2, d1, d0


def dMux1to8_( x, s2, s1, s0 ):
	p1 = dMux_( x, s2 )
	p2 = dMux1to4_( p1[0], s1, s0 )
	p3 = dMux1to4_( p1[1], s1, s0 )
	return ( p2[0], p2[1], p2[2], p2[3], p3[0], p3[1], p3[2], p3[3] ) # d3, d2, d1, d0



''''''''''''''''''''''''''' N-bit variants '''''''''''''''''''''''''''

# Basically not4() is equivalent to having 4 not gates each processing
#   a bit in parallel (same time)

def notN_( N, x ):
	return tuple( not_( x[i] ) for i in range( N ) )

def andN_( N, a, b ):
	return tuple( and_( a[i], b[i] ) for i in range( N ) )

def orN_( N, a, b ):
	return tuple( or_( a[i], b[i] ) for i in range( N ) )

def muxN_( N, d1, d0, sel ):
	return tuple( mux_( d1[i], d0[i], sel ) for i in range( N ) )

def muxN4to1_( N, d3, d2, d1, d0, s1, s0 ):
	return tuple( mux4to1_( d3[i], d2[i], d1[i], d0[i], s1, s0 ) for i in range( N ) )

def muxN8to1_( N, d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 ):
	return tuple( mux8to1_( d7[i], d6[i], d5[i], d4[i], d3[i], d2[i], d1[i], d0[i], s2, s1, s0 ) for i in range( N ) )



''''''''''''''''''''''''' multi-way variants '''''''''''''''''''''''''

def or3_( a, b, c ):
	return ( or_( a, or_( b, c ) ) )

def orNto1_( x ):
	# technically, could break once reach a one ...
	#   but is break doable with logic gates???
	out = x[0]
	for i in range( 1, len( x ) ):
		out = or_( out, x[i] )
	return out

	''' alternate way, takes advantage of using gates in parallel 
		> speed savings if physical implementation
	    https://github.com/havivha/Nand2Tetris/blob/master/02/Or8Way.hdl
	    t1 = or ( in[0], in[1] )
	    t2 = or ( in[2], in[3] )
	    t3 = or ( in[4], in[5] )
	    t4 = or ( in[6], in[7] )
	    t5 = or ( t1, t2 )
	    t6 = or ( t3, t4 )
	    t7 = or ( t5, t6 )
	    return t7  '''


def and3_( a, b, c ):
	return ( and_( a, and_( b, c ) ) )

def andNto1_( x ):
	# technically, could break once reach a zero ...
	#   but is break doable with logic gates???
	out = x[0]
	for i in range( 1, len( x ) ):
		out = and_( out, x[i] )
	return out
