'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''----------------------------- Helpers -----------------------------'''

# Two's complement
negativeOneN = 2 ** N_BITS - 1



'''------------------- The elementary logic gates -------------------'''

def not_( x ):

	return 1 if int( x ) == 0 else 0	



'''------------------ Multiplexers & Demultiplexers ------------------'''

def mux8to1_( d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0 ):

	sel = '{}{}{}'.format( s2, s1, s0 )

	out = d0 if sel == '000' else
	      d1 if sel == '001' else
	      d2 if sel == '010' else
	      d3 if sel == '011' else
	      d4 if sel == '100' else
	      d5 if sel == '101' else
	      d6 if sel == '110' else
	      d7 if sel == '111'

	return out



'''------------------------- N-bit variants -------------------------'''

def notN_( x ):
	
	# stackoverflow.com/a/27958372
	return x ^ negativeOneN
