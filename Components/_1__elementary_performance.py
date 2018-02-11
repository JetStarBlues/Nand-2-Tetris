'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''----------------------------- Helpers -----------------------------'''

negativeOne_ = 2 ** N_BITS - 1  # two's complement

def toBin( x ):

	return bin( x )[ 2 : ].zfill( N_BITS )

def toInt( a ):

	return int( ''.join( map( str, a ) ), 2 )



'''------------------- The elementary logic gates -------------------'''

def not_( x ):

	return x ^ 1	



'''------------------ Multiplexers & Demultiplexers ------------------'''

def mux8to1_( d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 ):

	sel = str( s2 ) + str( s1 ) + str( s0 )

	out = d0 if sel == '000' else \
	      d1 if sel == '001' else \
	      d2 if sel == '010' else \
	      d3 if sel == '011' else \
	      d4 if sel == '100' else \
	      d5 if sel == '101' else \
	      d6 if sel == '110' else \
	      d7 # if sel == '111'

	return out



'''------------------------- N-bit variants -------------------------'''

def notN_( x ):

	return x ^ negativeOne_
