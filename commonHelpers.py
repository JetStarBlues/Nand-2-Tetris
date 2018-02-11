'''------------------------------ Imports ------------------------------'''

import Components._0__globalConstants as GC


'''----------------------------- Main -----------------------------------'''

negativeOne = 2 ** GC.N_BITS - 1

largestInt = 2 ** ( GC.N_BITS - 1 ) - 1

def trim( x ):

	return x & negativeOne  # discard overflow bits

def negate( x ):

	return trim( ( x ^ negativeOne ) + 1 )  # twos complement

def isNegative( x ):

	return x > largestInt

def toBinary( x, N ):

	return bin( x )[ 2 : ].zfill( N )