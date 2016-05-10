'''
	In the spirit of
	  http://www.diveintopython3.net/unit-testing.html
	  http://www.diveintopython3.net/refactoring.html
	The tutorials show how maintainable and refactorable code becomes when use tests
'''

''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys
import unittest


# Computer files
sys.path.append('../')
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _3__clock import *
from _4__flipFlops import *


# Testing files
sys.path.append('KnownValues')
from kv_1__elementaryGates import *
from kv_2__arithmeticGates import *


''''''''''''''''''''''''' testing helpers '''''''''''''''''''''''''

# Formatting ---

def toString(array):
	return ''.join( map(str, array) )

def toDecimal(bitSeq):
	return int(bitSeq, 2)

def toBinary(N, x):
	if x < 0: x = 2**N + x  # 2s complement
	return bin(x)[2:].zfill(N)
	


''''''''''''''''''''''''' elementary gates '''''''''''''''''''''''''''

'''
	and_( a, b )
	or_( a, b )
	xor_( a, b )
	not_( x )
	nand_( a, b )
	nor_( a, b )
	xnor_( a, b )

	decoder1to2_( a )
	decoder2to4_( d1, d0 )
	decoder3to8_( d2, d1, d0 )
	encoder2to1_( d1, d0 )
	encoder4to2_( d3, d2, d1, d0 )
	encoder8to3_( d7, d6, d5, d4, d3, d2, d1, d0 )

	mux_( d1, d0, sel )
	mux4to1_( d3, d2, d1, d0, s1, s0 )
	mux8to1_( d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 )
	dMux_( x, sel )
	dMux1to4_( x, s1, s0 )
	dMux1to8_( x, s2, s1, s0 )

	notN_( N, x )
	andN_( N, a, b )
	orN_( N, a, b )

	muxN_( N, d1, d0, sel )
	muxN4to1_( N, d3, d2, d1, d0, s1, s0 )
	muxN8to1_( N, d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 )

	or3_( a, b, c )
	orNto1_( x )
	and3_( a, b, c )
	andNto1_( x )
'''

'''
	k_and
	k_and16
	k_not
	k_not16
	k_or
	k_or16
	k_xor
	k_decoder1to2
	k_decoder2to4
	k_decoder3to8
	k_encoder2to1
	k_encoder4to2
	k_encoder8to3
	k_dMux
	k_dMux1to4
	k_dMux1to8
	k_mux
	k_mux16
	k_muxN4to1
	k_muxN8to1
	k_or8to1
'''

class Test_ElementaryGates( unittest.TestCase ):

	def test_and( self ):
		''' and gate '''
		for g in k_and:
			result = and_( g[0], g[1] )
			self.assertEqual( result, g[2] )

	def test_or( self ):
		''' or gate '''
		for g in k_or:
			result = or_( g[0], g[1] )
			self.assertEqual( result, g[2] )

	def test_xor( self ):
		''' xor gate '''
		for g in k_xor:
			result = xor_( g[0], g[1] )
			self.assertEqual( result, g[2] )

	def test_not( self ):
		''' not gate '''
		for g in k_not:
			result = not_( g[0] )
			self.assertEqual( result, g[1] )

	def test_nand( self ):
		pass

	def test_nor( self ):
		pass

	def test_xnor( self ):
		pass

	def test_decoder1to2_( self ):
		''' decoder1to2 '''
		for g in k_decoder1to2:
			result = decoder1to2_( g[0] )
			self.assertEqual( toString( result ), g[1] )

	def test_decoder2to4_( self ):
		''' decoder2to4 '''
		for g in k_decoder2to4:
			result = decoder2to4_( g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_decoder3to8_( self ):
		''' decoder3to8 '''
		for g in k_decoder3to8:
			result = decoder3to8_( g[0], g[1], g[2] )
			self.assertEqual( toString( result ), g[3] )

	def test_encoder2to1_( self ):
		''' encoder2to1 '''
		for g in k_encoder2to1:
			result = encoder2to1_( g[0], g[1] )
			self.assertEqual( result, g[2] )

	def test_encoder4to2_( self ):
		''' encoder4to2 '''
		for g in k_encoder4to2:
			result = encoder4to2_( g[0], g[1], g[2], g[3] )
			self.assertEqual( toString( result ), g[4] )

	def test_encoder8to3_( self ):
		''' encoder8to3 '''
		for g in k_encoder8to3:
			result = encoder8to3_( g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7] )
			self.assertEqual( toString( result ), g[8] )

	def test_mux( self ):
		''' mux '''
		for g in k_mux:
			result = mux_( g[0], g[1], g[2] )
			self.assertEqual( result, g[3] )

	def test_mux4to1( self ):
		pass

	def test_mux8to1( self ):
		pass

	def test_dMux_( self ):
		''' dMux '''
		for g in k_dMux:
			result = dMux_( g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_dMux1to4_( self ):
		''' dMux1to4 '''
		for g in k_dMux1to4:
			result = dMux1to4_( g[0], g[1], g[2] )
			self.assertEqual( toString( result ), g[3] )

	def test_dMux1to8_( self ):
		''' dMux1to8 '''
		for g in k_dMux1to8:
			result = dMux1to8_( g[0], g[1], g[2], g[3] )
			self.assertEqual( toString( result ), g[4] )

	def test_notN_( self ):
		''' notN '''
		for g in k_not16:
			result = notN_( 16, g[0] )
			self.assertEqual( toString( result ), g[1] )

	def test_andN_( self ):
		''' andN '''
		for g in k_and16:
			result = andN_( 16, g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_orN_( self ):
		''' orN '''
		for g in k_or16:
			result = orN_( 16, g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_muxN_( self ):
		''' muxN '''
		for g in k_mux16:
			result = muxN_( 16, g[0], g[1], g[2] )
			self.assertEqual( toString( result ), g[3] )

	def test_muxN4to1_( self ):
		''' muxN4to1 '''
		for g in k_muxN4to1:
			result = muxN4to1_( 16, g[0], g[1], g[2], g[3], g[4], g[5] )
			self.assertEqual( toString( result ), g[6] )

	def test_muxN8to1_( self ):
		''' muxN8to1 '''
		for g in k_muxN8to1:
			result = muxN8to1_( 16, g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8], g[9], g[10] )
			self.assertEqual( toString( result ), g[11] )

	def test_or3_( self ):
		pass

	def test_orNto1_( self ):
		''' orNto1 '''
		for g in k_or8to1:
			result = orNto1_( g[0] )
			self.assertEqual( int( result ), g[1] )

	def test_and3_( self ):
		pass

	def test_andNto1_( self ):
		pass



''''''''''''''''''''''''' arithmetic gates '''''''''''''''''''''''''''

'''
	zeroN_( N )
	oneN_( N )
	isZero_( x )

	halfAdder_( a, b )
	fullAdder_( a, b, c )
	addN_( N, a, b )
	incrementN_( N, x )
	fastIncrement_( x )

	halfSubtractor_( a, b )
	fullSubtractor_( a, b, c )
	subtractN_( N, a, b )
	subtractN_v2_( N, a, b )

	negate_( x )
	isNegative_( x )

	ALU_( x, y, zx, nx, zy, ny, f, no )
'''

'''
	k_halfAdder
	k_fullAdder
	k_add16
	k_subract16
	k_increment16
	k_ALU16
'''

class Test_ArithmeticGates( unittest.TestCase ):
	
	def test_zeroN_( self ):
		pass

	def test_oneN_( self ):
		pass

	def test_isZero_( self ):
		pass

	def test_halfAdder( self ):
		''' halfAdder '''
		for g in k_halfAdder:
			result = halfAdder_( g[0], g[1] )
			self.assertEqual( result, g[2] )

	def test_fullAdder_( self ):
		''' fullAdder '''
		for g in k_fullAdder:
			result = fullAdder_( g[0], g[1], g[2] )
			self.assertEqual( result, g[3] )

	def test_addN_( self ):
		''' addN '''
		for g in k_add16:
			result = addN_( 16, g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_subtractN_( self ):
		''' subtractN '''
		for g in k_subtract16:
			result = subtractN_( 16, g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_subtractN_v2_( self ):
		''' subtractN_v2 '''
		for g in k_subtract16:
			result = subtractN_v2_( 16, g[0], g[1] )
			self.assertEqual( toString( result ), g[2] )

	def test_incrementN_( self ):
		''' incrementN '''
		for g in k_increment16:
			result = incrementN_( 16, g[0] )
			self.assertEqual( toString( result ), g[1] )

	def test_fastIncrement_( self ):  # temp unless can make it all with gates
		''' fast increment '''
		for g in k_increment16:
			result = fastIncrement_( g[0] )
			self.assertEqual( toString( result ), g[1] )

	def test_negate_( self ): 
		pass

	def test_isNegative_( self ): 
		pass

	def test_ALU_( self ):
		''' ALU '''
		for g in k_ALU16:
			result = ALU_( g[0], g[1], g[2], g[3], g[4], g[5], g[6], g[7] )
			self.assertEqual( toString( result[0] ), g[8] )
			self.assertEqual( toDecimal( toString( result[1] ) ), g[9] )
			self.assertEqual( toDecimal( toString( result[2] ) ), g[10] )




''''''''''''''''''''''''''' Run the tests '''''''''''''''''''''''''''''

if __name__ == '__main__':
	unittest.main()