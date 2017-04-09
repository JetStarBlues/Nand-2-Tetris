# TODO ===================================

def and_( a, b ):
	return ( int( a ) & int( b ) )

def or_( a, b ):
	return ( int( a ) | int( b ) )	

def xor_( a, b ):
	return ( int( a ) ^ int( b ) )

def or3_( a, b, c ):
	return ( or_( a, or_( b, c ) ) )

def orNto1_( x ):
	out = x[0]
	for i in range( 1, len( x ) ):
		out = or_( out, x[i] )
	return out

def and3_( a, b, c ):
	return ( and_( a, and_( b, c ) ) )

def andNto1_( x ):
	out = x[0]
	for i in range( 1, len( x ) ):
		out = and_( out, x[i] )
	return out

def toBin_( N, x ):

	return bin(x)[2:].zfill( N )

def toDec_( x ):

	return int( ''.join( map( str, x ) ), 2 )

def fullAdderCLA_( a, b, cIn ):

	''' Modified fullAdder
	     Does not compute carry, instead returns propogate and generate values '''

	propogate = or_( a, b )
	generate = and_( a, b )

	summ = xor_( xor_( a, b ), cIn )

	return ( summ, propogate, generate )


def carryLookaheadAdder4_( a, b, c0 ):

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


def carryLookaheadAdder16_( a, b ):

	c0 = 0
# def carryLookaheadAdder16_( a, b, c0 ):

	_, _, p0, g0 = carryLookaheadAdder4_( a[12:  ], b[12:  ], '0' )
	_, _, p1, g1 = carryLookaheadAdder4_( a[ 8:12], b[ 8:12], '0' )
	_, _, p2, g2 = carryLookaheadAdder4_( a[ 4:8 ], b[ 4:8 ], '0' )
	_, _, p3, g3 = carryLookaheadAdder4_( a[  :4 ], b[  :4 ], '0' )

	c1 = or_(       g0, and_( p0, c0 ) )
	c2 = or3_(      g1, and_( p1, g0 ), and3_( p1, p0, c0 ) )
	c3 = orNto1_( ( g2, and_( p2, g1 ), and3_( p2, p1, g0 ), andNto1_( ( p2, p1, p0, c0 ) ) ) )
	c4 = orNto1_( ( g3, and_( p3, g2 ), and3_( p3, p2, g1 ), andNto1_( ( p3, p2, p1, g0 ) ), andNto1_( ( p3, p2, p1, p0, c0 ) ) ) )

	s0, _, _, _ = carryLookaheadAdder4_( a[12:  ], b[12:  ], c0 )
	s1, _, _, _ = carryLookaheadAdder4_( a[ 8:12], b[ 8:12], c1 )
	s2, _, _, _ = carryLookaheadAdder4_( a[ 4:8 ], b[ 4:8 ], c2 )
	s3, _, _, _ = carryLookaheadAdder4_( a[  :4 ], b[  :4 ], c3 )

	cOut = c4
	summ = s3 + s2 + s1 + s0

	# p = andNto1_( ( p3, p2, p1, p0 ) )
	# g = orNto1_( ( g3, and_( p3, g2 ), and3_( p3, p2, g1 ), andNto1_( ( p3, p2, p1, g0 ) ) ) )

	# return ( summ, cOut, p, g )
	return ( summ )



N = 16

x = 0
y = 2**16 - 1

# a0 = carryLookaheadAdder( N, toBin_( N, x ), toBin_( N, y ) )
a1 = carryLookaheadAdder16_( toBin_( N, x ), toBin_( N, y ) )

# print( toDec_( a0 ), a0 )
# print( toDec_( a1 ), a1 )




''' 
	c1 = g0 + p0c0
	c2 = g1 + p1g0 + p1p0c0
	c3 = g2 + p2g1 + p2p1g0 + p2p1p0c0
	c4 = g3 + p3g2 + p3p2g1 + p3p2p1g0 + p3p2p1p0c0
'''

def G( n ):

	return 'G{}'.format( n )

def P( n ):

	return 'P{}'.format( n )

def hmm( n ):

	for i in range( n + 1 ):

		print( '---' )

		if i < n:

			print( G( n - i - 1 ) )

		if i > 0:

			for j in range( n - 1, n - 1 - i, -1 ):

				print( P( j ) )

		if i == n:

			print( 'C0' )



	print( '\n====gg' )

	for i in range( n ):

		print( '---' )

		if i < n:

			print( G( n - i - 1 ) )

		if i > 0:

			for j in range( n - 1, n - 1 - i, -1 ):

				print( P( j ) )

hmm(4)
