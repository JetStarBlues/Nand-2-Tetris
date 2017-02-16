''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import sys

# Computer files
sys.path.append('../../Modules')
from _1__elementaryGates import *
from _2__arithmeticGates import *


''''''''''''''''''''''''' main '''''''''''''''''''''''''

# https://en.wikipedia.org/wiki/Digital_comparator

'''
	doesn't work when comparing (1)negative to (0)positive numbers
	 as under 2's complement, negative will always be larger
	  positive range(0, 2**(n-1))
	  negative range(2**(n-1), 2**n)
	MSB doubles as sign... maybe could use to make a workaround ? =/
'''


# -- using logic gates ---
# 1Bit
def comp_( a, b ):
	eq = xnor_( a, b ) 		# a == b
	lt = and_( not_(a), b ) # a < b
	gt = and_( a, not_(b) ) # a > b
	return( eq, lt, gt )

# nBit
def compN_( N, a, b ):

	# individual
	comps = []
	for i in range(N):
		comps.append( comp_( a[i], b[i] ) )
	# print(comps)

	# equal
	eqB = [ c[0] for c in comps ]
	eq = andNto1_( eqB )
	# print( eq, eqB )

	# less than
	parts = []
	for i in range(N):
		part = eqB[:i]
		# print(part)
		part.insert( 0, comps[i][1] )
		parts.append( andNto1_( part ) )
	lt = orNto1_( parts )

	# greater than
	gt = xnor_( eq, lt )

	#
	return( eq, lt, gt )	


# --- using mux ---
# 1Bit
def comp2_( a, b ):
	eq = mux4to1_( 1, 0, 0, 1, a, b )	# a == b
	lt = mux4to1_( 0, 1, 0, 0, a, b )	# a < b
	gt = mux4to1_( 0, 0, 1, 0, a, b )	# a > b
	return( eq, lt, gt ) 

# nBit
def compN2_( N, a, b ):
	''' Exact same as compN_(),
		 just swap comp_() with comp2_() '''
	pass



''''''''''''''''''''''''' test '''''''''''''''''''''''''

def dec2BinN( N, x ):
	if x < 0: x = 2**N - abs(x) # two's complement negation
	b = bin(x)[2:] # strip leading '0b'
	return b.zfill( N ) # pad with zeros as needed

testVals = [
	[ 1,  0, 1  ],
	[10, 15, 4  ],
	[-5, -8, 3+1],
	[-7, -7, 3+1],
	[-9,  0, 4+1],  # fails
	[55, 80, 7  ]
]

for vals in testVals:
# for i in range(3):
# 	vals = testVals[i]
	v1 = vals[0]
	v2 = vals[1]
	N = vals[2]
	expected = [ v1 == v2, v1 < v2, v1 > v2 ]
	result = compN_( N, dec2BinN( N, v1 ), dec2BinN( N, v2 ) )
	print( expected[0] == result[0], ">", expected[0], result[0] )
	print( expected[1] == result[1], ">", expected[1], result[1] )
	print( expected[2] == result[2], ">", expected[2], result[2] )
	print( "---" )
