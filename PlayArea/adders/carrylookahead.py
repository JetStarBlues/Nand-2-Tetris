'''
	Slower than ripple in software given serial/sequential execution
'''

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

	c[1] = or_(       g[0], and_( p[0], c[0] ) )
	c[2] = or3_(      g[1], and_( p[1], g[0] ), and3_( p[1], p[0], c[0] ) )
	c[3] = orNto1_( ( g[2], and_( p[2], g[1] ), and3_( p[2], p[1], g[0] ), andNto1_( ( p[2], p[1], p[0], c[0] ) ) ) )
	c[4] = orNto1_( ( g[3], and_( p[3], g[2] ), and3_( p[3], p[2], g[1] ), andNto1_( ( p[3], p[2], p[1], g[0] ) ), andNto1_( ( p[3], p[2], p[1], p[0], c[0] ) ) ) )

	def fx2( i ):

		j = 3 - i
		s[i], _, _ = fullAdderCLA_( a[j], b[j], c[i] )

	e.run( 4, fx2, idx )

	summ = tuple( s[::-1] )
	cOut = c[4]

	pp = andNto1_( p )
	gg = orNto1_( ( g[3], and_( p[3], g[2] ), and3_( p[3], p[2], g[1] ), andNto1_( ( p[3], p[2], p[1], g[0] ) ) ) )

	return ( summ, cOut, pp, gg )
	'''

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