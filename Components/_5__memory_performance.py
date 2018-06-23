'''' 
    Memory is implemented using Python lists instead of flip flop instances.
    Data is stored/represented as integers instead of binary.
'''

'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''---------------------------- Registers ----------------------------'''

# Words are stored as equivalent integer

class Register_():

	''' 1 bit register '''

	def __init__( self ):

		self.register = 0


	def write( self, clk, x, write ):
		
		if clk == 1 and write == 1:

			self.register = x


	def read( self ):

		return self.register


class RegisterN_():

	''' N bit register '''

	def __init__( self, N ):

		self.register = 0


	def write( self, clk, x, write ):
		
		if clk == 1 and write == 1:

			# print( 'writing', x )

			self.register = x


	def read( self ):

		# print( 'reading', self.register )

		return self.register



'''------------------------------- RAM -------------------------------'''

class RAMXN_():

	''' X register N bit RAM '''

	def __init__( self, X, N ):

		self.registers = [ 0 for _ in range( X ) ]


	def write( self, clk, x, write, address ):

		if clk == 1 and write == 1:
		
			# print( 'writing,', address, x )
			
			self.registers[ address ] = x


	def read( self, address ):

		# print( 'reading,', address, self.registers[ address ] )

		return self.registers[ address ]


ROMXN_ = RAMXN_  # alias
