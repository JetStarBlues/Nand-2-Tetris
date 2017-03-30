''''
	Memory components implemented with Python arrays instead of flip flop instances.
	  Used to vastly improve the emulator's speed.
	  For ff based memory, see '_5__memory.py'
'''


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
		
		change = or3_( write, inc, rst )

		# TODO --- Replace mux with if statements

		# d = muxN_performance_(

		# 		self.N,
		# 		zeroN,
		# 		muxN_performance_(

		# 			self.N,
		# 			x[ -self.N : ],  # turn x to N bit by trimming signifcant bits
		# 			muxN_performance_(

		# 				self.N,
		# 				( incrementN_, ( self.N, self.register.read() ) ),
		# 				( self.register.read, () ),

		# 				inc 
		# 			),

		# 			write
		# 		),

		# 		rst
		# 	)

		self.register.write( clk, d, change )


	def read( self ):
		
		return self.register.readDecimal()

		# out = self.register.readDecimal()
		# print( out )
		# return( out )