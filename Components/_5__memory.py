'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''---------------------------- Registers ----------------------------'''

''' Words are stored as tuples (array) of bits (msb to lsb).
    Each bit is represented by an integer.
    Ex. 6 is stored as [ 0, 0, 0, 0, 0, 1, 1, 0 ]
'''

class Register_():

	''' 1 bit register '''

	def __init__( self ):

		self.ff = DFlipFlop()

		self.ff.clear()  # start with out = 0


	def write( self, clk, x, write ):

		d = mux_( x, self.ff.q1, write )

		self.ff.doTheThing( clk, 0, 0, d )
		

	def read( self ):

		# as fx cause have to wait for values to 'settle'
		return self.ff.read()


class RegisterN_():

	''' N bit register '''

	def __init__( self, N ):

		self.N = N

		self.registers = [ Register_() for i in range( self.N ) ]


	def write( self, clk, x, write ):

		for i in range( self.N ):

			self.registers[ i ].write( clk, x[ i ], write )


	def read( self ):

		return tuple( register.read() for register in self.registers )


	def readDecimal( self ):

		out = self.read()  # index in binary

		return int( ''.join( map( str, out ) ), 2 )  # index in decimal



'''------------------------------- RAM -------------------------------'''

class RAMXN_():

	''' X register N bit RAM '''

	'''
		Cheating by using array.
		In the physical implementation, choosing which register to enable would be
		via combo of decoder and tristate buffer.
	'''

	def __init__( self, X, N ):

		self.registers = [ RegisterN_( N ) for i in range( X ) ]


	def bitArrayToInt( self, x ):

		return int( ''.join( map( str, x ) ), 2 )


	def write( self, clk, x, write, address ):

		self.registers[ self.bitArrayToInt( address ) ].write( clk, x, write )


	def read( self, address ):

		return self.registers[ self.bitArrayToInt( address ) ].read()


ROMXN_ = RAMXN_  # alias
