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

	'''
		def __init__( self ):

			self.ff = DFlipFlop()

			self.ff.clear()  # start with out = 0


		def write( self, clk, x, write ):

			d = mux_( x, self.ff.q1, write )

			self.ff.doTheThing( clk, 0, 0, d )
			

		def read( self ):

			# as fx cause have to wait for values to 'settle'
			return self.ff.read()
	'''

	# Cheating. DFFs too slow...
	def __init__( self ):

		self.register = 0


	def write( self, clk, x, write ):
		
		if clk == 1 and write == 1:

			self.register = x


	def read( self ):

		return self.register


class RegisterN_():

	''' N bit register '''

	'''
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

			return int( ''.join( map( str, out ) ), 2 )  # decimal
	'''

	# Cheating. Register_ instances take up too much space...
	def __init__( self, N ):

		self.register = ( 0, ) * N


	def write( self, clk, x, write ):
		
		if clk == 1 and write == 1:

			self.register = x


	def read( self ):

		return self.register


	def readDecimal( self ):

		return int( ''.join( map( str, self.register ) ), 2 )  # decimal



'''------------------------------- RAM -------------------------------'''

class RAMXN_():

	''' X register N bit RAM '''

	'''
		Cheating by using array.
		In the physical implementation, choosing which register to enable would be
		via combo of decoder and tristate buffer.
	'''

	'''
		def __init__( self, X, N ):

			self.registers = [ RegisterN_( N ) for i in range( X ) ]


		def bitArrayToInt( self, x ):

			return int( ''.join( map( str, x ) ), 2 )  # decimal


		def write( self, clk, x, write, address ):

			self.registers[ self.bitArrayToInt( address ) ].write( clk, x, write )

		def read( self, address ):

			return self.registers[ self.bitArrayToInt( address ) ].read()
	'''

	# Cheating. RegisterN_ instances take up too much space...
	def __init__( self, X, N ):

		self.registers = [ ( ( 0, ) * N ) for _ in range( X ) ]


	def bitArrayToInt( self, x ):

		return int( ''.join( map( str, x ) ), 2 )  # decimal


	def write( self, clk, x, write, address ):

		if clk == 1 and write == 1:

			if not isinstance( address, int ):

				address = self.bitArrayToInt( address )

			self.registers[ address ] = x


	def read( self, address ):

		if not isinstance( address, int ):

			address = self.bitArrayToInt( address )

		return self.registers[ address ]


	def readDecimal( self, address ):

		out = self.read( address )  # index in binary

		return int( ''.join( map( str, out ) ), 2 )  # decimal


ROMXN_ = RAMXN_  # alias
