'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''------------------------- Program counter -------------------------'''

class ProgramCounterN_():

	''' N bit program counter 

	        if    rst(t-1)   : out(t) = 0
	        elif  write(t-1) : out(t) = in(t-1)
	        elif  inc(t-1)   : out(t) = out(t-1) + 1
	        else             : out(t) = out(t-1)
	'''

	def __init__( self, N ):

		self.N = N	

		self.register = RegisterN_( N )


	def doTheThing( self, clk, x, rst, write, inc ):
		
		change = or3_( write, inc, rst )

		d = muxN_(

			self.N,
			zeroN,
			muxN_(

				self.N,
				x[ - self.N : ],  # turn x to N bit by trimming signifcant bits
				muxN_(

					self.N,
					incrementN_( self.N, self.register.read() ),
					self.register.read(),

					inc 
				),

				write
			),

			rst
		)

		self.register.write( clk, d, change )


	def read( self ):
		
		return self.register.readDecimal()

		# out = self.register.readDecimal()
		# print( out )
		# return( out )