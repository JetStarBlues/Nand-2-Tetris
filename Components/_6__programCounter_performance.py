'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''------------------------- Program counter -------------------------'''

class ProgramCounterN_():

	''' N bit program counter '''

	def __init__( self, N ):

		self.N = N	
		
		self.register = RegisterN_( N )


	def doTheThing( self, clk, x, rst, write, inc ):

		change = rst | write | inc

		if rst:  # reset

			d = 0

		elif write:  # jump

			d = x

		elif inc:  # increment

			d = self.register.read() + 1

		else:

			# d = self.register.read()

			d = None  # don't care what assigned as won't be written

		self.register.write( clk, d, change )


	def read( self ):
		
		return self.register.readDecimal()

		# out = self.register.readDecimal()
		# print( out )
		# return( out )
