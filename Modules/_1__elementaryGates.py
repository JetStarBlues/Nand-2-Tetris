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

def decoder1to2_( a ):
	q1 = a
	q0 = not_( a )
	return ( q1, q0 )


def decoder2to4_( d1, d0 ):
	a, b = d1, d0
	q3 = and_(       a  ,       b   )
	q2 = and_(       a  , not_( b ) )
	q1 = and_( not_( a ),       b   )
	q0 = and_( not_( a ), not_( b ) )
	return ( q3, q2, q1, q0 )


def decoder3to8_( d2, d1, d0 ):
	a, b, c = d2, d1, d0
	q7 = and3_(       a  ,       b  ,       c   )
	q6 = and3_(       a  ,       b  , not_( c ) )
	q5 = and3_(       a  , not_( b ),       c   )
	q4 = and3_(       a  , not_( b ), not_( c ) )
	q3 = and3_( not_( a ),       b  ,       c   ) 
	q2 = and3_( not_( a ),       b  , not_( c ) )
	q1 = and3_( not_( a ), not_( b ),       c   )
	q0 = and3_( not_( a ), not_( b ), not_( c ) )
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
	return( q2, q1, q0 )



''''''''''''''''''''''''''''' Multiplexers '''''''''''''''''''''''''''''

def mux_( a, b, sel ):
	''' 2to1 multiplexor is equivalent to an if/else statement of form,
			out = a if sel == 0
				  b if sel == 1

		Or in boolean algebra
			out = ( s * b ) + ( !s * a )

		See http://electronics.stackexchange.com/a/15410
	''' 
	sb = and_( sel, b )
	nsa = and_( not_( sel ), a )
	return or_( sb, nsa )


def mux4to1_( a, b, c, d, s1, s2 ):

	''' out = a if sel == 00
		      b if sel == 01
		      c if sel == 10
		      d if sel == 11  '''

	# ''' using elementary gates '''
	# p1 = and_( and_( a, not_( s1 ) ), not_( s2 ) )
	# p2 = and_( and_( b, not_( s1 ) ),       s2   )
	# p3 = and_( and_( c,       s1   ), not_( s2 ) )
	# p4 = and_( and_( d,       s1   ),       s2   )
	# return or_( or_( p1, p2 ), or_( p3, p4 ) )

	''' using other mux chips '''
	p1 = mux_( a, b, s2 )
	p2 = mux_( c, d, s2 )
	return mux_( p1, p2, s1 )


def mux8to1_( a, b, c, d, e, f, g, h, s1, s2, s3 ):

	''' out = a if sel == 000
		      b if sel == 001
		      c if sel == 010
		      d if sel == 011
		      e if sel == 100
		      f if sel == 101
		      g if sel == 110
		      h if sel == 111  '''

	# ''' using elementary gates '''
	# p1 = and_( and_( a, not_( s1 ) ), and_( not_( s2 ), not_( s3 ) ) )
	# p2 = and_( and_( b, not_( s1 ) ), and_( not_( s2 ),       s3   ) )
	# p3 = and_( and_( c, not_( s1 ) ), and_(       s2  , not_( s3 ) ) )
	# p4 = and_( and_( d, not_( s1 ) ), and_(       s2  ,       s3   ) )
	# p5 = and_( and_( e,       s1   ), and_( not_( s2 ), not_( s3 ) ) )
	# p6 = and_( and_( f,       s1   ), and_( not_( s2 ),       s3   ) )
	# p7 = and_( and_( g,       s1   ), and_(       s2  , not_( s3 ) ) )
	# p8 = and_( and_( h,       s1   ), and_(       s2  ,       s3   ) )
	# return or8Way_( [ p1, p2, p3, p4, p5, p6, p7, p8 ] )

	''' using other mux chips '''
	p1 = mux4to1_( a, b, c, d, s2, s3 )
	p2 = mux4to1_( e, f, g, h, s2, s3 )
	return mux_( p1, p2, s1 )


def dMux_( x, sel ):
	'''	[ a, b ] = [ x, 0 ] if sel == 0
				   [ 0, x ] if sel == 1
	'''
	a = and_( x, not_( sel ) )
	b = and_( x, sel )
	return ( a, b )


def dMux1to4_( x, s1, s2 ):

	# ''' using elementary gates '''
	# a = and_( and_( x, not_( s1 ) ), not_( s2 ) )
	# b = and_( and_( x, not_( s1 ) ),       s2   )
	# c = and_( and_( x,       s1   ), not_( s2 ) )
	# d = and_( and_( x,       s1   ),       s2   )
	# return ( a, b, c, d )

	''' using other dMux chips 
	      www.allaboutcircuits.com/textbook/digital/chpt-9/demultiplexers
	'''
	p1 = dMux_( x, s1 )
	p2 = dMux_( p1[0], s2 )
	p3 = dMux_( p1[1], s2 )
	return ( p2[0], p2[1], p3[0], p3[1] )


def dMux1to8_( x, s1, s2, s3 ):
	p1 = dMux_( x, s1 )
	p2 = dMux1to4_( p1[0], s2, s3 )
	p3 = dMux1to4_( p1[1], s2, s3 )
	return ( p2[0], p2[1], p2[2], p2[3], p3[0], p3[1], p3[2], p3[3] )



''''''''''''''''''''''''''' N-bit variants '''''''''''''''''''''''''''

# Basically not4() is equivalenet to having 4 not gates each processing
#   a bit in parallel (same time)

def notN_( N, x ):
	return tuple( not_( x[i] ) for i in range( N ) )

def andN_( N, a, b ):
	return tuple( and_( a[i], b[i] ) for i in range( N ) )

def orN_( N, a, b ):
	return tuple( or_( a[i], b[i] ) for i in range( N ) )

def muxN_( N, a, b, sel ):
	return tuple( mux_( a[i], b[i], sel ) for i in range( N ) )

def muxN4to1_( N, a, b, c, d, s1, s2 ):
	return tuple( mux4to1_( a[i], b[i], c[i], d[i], s1, s2 ) for i in range( N ) )

def muxN8to1_( N, a, b, c, d, e, f, g, h, s1, s2, s3 ):
	return tuple( mux8to1_( a[i], b[i], c[i], d[i], e[i], f[i], g[i], h[i], s1, s2, s3 ) for i in range( N ) )



''''''''''''''''''''''''' multi-way variants '''''''''''''''''''''''''

def or3_( a, b, c ):
	return( or_( a, or_( b, c ) ) )

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
	return( and_( a, and_( b, c ) ) )

def andNto1_( x ):
	# technically, could break once reach a zero ...
	#   but is break doable with logic gates???
	out = x[0]
	for i in range( 1, len( x ) ):
		out = and_( out, x[i] )
	return out