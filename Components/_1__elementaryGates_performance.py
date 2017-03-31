'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''----------------------------- Helpers -----------------------------'''

def flip( b ):

	if b == '0': return '1'

	else: return '0'



'''------------------- The elementary logic gates -------------------'''

def not_( x ):

	return 1 if int( x ) == 0 else 0	



'''------------------ Multiplexers & Demultiplexers ------------------'''

def mux8to1_( d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 ):

	sel = s2 + s1 + s0

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

	# Problematic in terms of speed

	x = bin( x )[ 2 : ].zfill( N_BITS )

	return int( ''.join( flip( b ) for b in x ) , 2 )

