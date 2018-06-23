'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''----------------------------- Counter -----------------------------'''

class CounterN_():

	''' N bit counter 

	        if    rst(t-1)   : out(t) = 0
	        elif  write(t-1) : out(t) = in(t-1)
	        elif  inc(t-1)   : out(t) = out(t-1) + 1
	        else             : out(t) = out(t-1)
	'''

	def __init__( self, N ):

		self.N = N

		self.register = RegisterN_( N )


	def doTheThing( self, clk, rst, x, write, inc ):
		
		change = or3_( write, inc, rst )

		d = muxN_(

			# Reset
			self.N,
			zeroN_( self.N ),
			muxN_(

				# Jump
				self.N,
				x,
				muxN_(

					# Increment
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
		
		return self.register.read()


	def readDecimal( self ):
		
		return self.register.readDecimal()
