''''
	Memory components implemented with Python arrays instead of flip flop instances.
	  Used to vastly improve the emulator's speed.
	  For ff based memory, see '_5__memory.py'
'''


'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''---------------------------- Registers ----------------------------'''

class RegisterN_():

	''' N bit register '''

	def __init__( self, N ):

		self.register = '0' * N


	def write( self, clk, x, write ):
		
		if clk == 1 and write == 1:

			self.register = x


	def read( self ):

		return self.register


	def readDecimal( self ):

		# used by A_register and program_counter, as haven't implemented binary indexing

		out = self.read()  # index in binary

		out = int( ''.join( map( str, out ) ), 2 )  # index in decimal

		return out



'''------------------------------- RAM -------------------------------'''

class RAMXN_():

	''' X register N bit RAM '''

	def __init__( self, X, N ):

		self.registers = [ '0' * N for _ in range( X ) ]


	def write( self, clk, x, write, address ):
		
		if clk == 1 and write == 1:
			
			self.registers[address] = x


	def read( self, address ):

		return self.registers[address]
