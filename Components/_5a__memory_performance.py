''''
	Memory components implemented with Python arrays instead of flip flop instances.
	  Used to vastly improve the simulator's speed.
	  For ff based memory, see '_5__memory.py'
'''


'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *



'''---------------------------- Registers ----------------------------'''

class RegisterN_performance_():

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

class RAMXN_performance_():

	''' X register N bit RAM '''

	def __init__( self, X, N ):

		self.registers = [ '0' * N for _ in range( X ) ]


	def write( self, clk, x, write, address ):
		
		if clk == 1 and write == 1:
			
			self.registers[address] = x


	def read( self, address ):

		return self.registers[address]



'''------------------------- Program counter -------------------------'''

class ProgramCounterN_performance_():

	''' N bit program counter '''

	def __init__( self, N ):

		self.N = N	
		
		self.register = RegisterN_performance_( N )


	def doTheThing( self, clk, x, rst, write, inc ):
		
		change = or3_( write, inc, rst )

		d = muxN_performance_(

				self.N,
				zeroN,
				muxN_performance_(

					self.N,
					x[ -self.N : ],  # turn x to N bit by trimming signifcant bits
					muxN_performance_(

						self.N,
						( incrementN_, ( self.N, self.register.read() ) ),
						( self.register.read, () ),

						inc 
					),

					write
				),

				rst
			)

		self.register.write( clk, d, change )


	def read( self ):
		
		# return self.register.readDecimal()

		out = self.register.readDecimal()
		# print( out )
		return( out )