'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''---------------------------- Registers ----------------------------'''

class Register_():

	''' 1 bit register '''

	def __init__( self ):

		self.ff = DFlipFlop()

		self.ff.clear()  # start with out = 0


	def write( self, clk, x, write ):

		d = mux_( x, self.ff.q1, write )

		self.ff.doTheThing( clk, d )
		

	def read( self ):

		# as fx cause have to wait for values to 'settle'
		return self.ff.q1


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

		# used by A_register and program_counter, as haven't implemented binary indexing

		out = self.read()  # index in binary

		out = int( ''.join( map( str, out ) ), 2 )  # index in decimal

		return out



'''------------------------------- RAM -------------------------------'''

class RAM8_():

	''' 8 register 1 bit RAM '''

	def __init__( self ):

		self.registers = [ Register_() for i in range( 8 ) ]


	def write( self, clk, x, write, address ):

		'''
		 In the physical implementation, choosing which register to enable would be
		 via combo use of decoder and tristate buffer.
		 Unable atm to represent z-state of tristate buffer in this emulator.
		'''
		
		self.registers[ address ].write( clk, x, write )


	def read( self, address ):

		return self.registers[ address ].read()


class RAM8N_():

	''' 8 register N bit RAM '''

	def __init__( self, N ):

		self.registers = [ RegisterN_( N ) for i in range( 8 ) ]


	def write( self, clk, x, write, address ):
		
		self.registers[ address ].write( clk, x, write )


	def read( self, address ):

		return self.registers[ address ].read()


class RAMXN_():

	''' X register N bit RAM '''

	def __init__( self, X, N ):

		self.registers = [ RegisterN_( N ) for i in range( X ) ]


	def write( self, clk, x, write, address ):
		
		self.registers[ address ].write( clk, x, write )


	def read( self, address ):

		return self.registers[ address ].read()
