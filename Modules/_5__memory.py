''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import multiprocessing

# Computer files
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _4__flipFlops import *


''''''''''''''''''''''''''' registers '''''''''''''''''''''''''''''

class Register_():

	''' 1 bit register '''

	def __init__( self ):

		self.ff = DFlipFlop()
		self.ff.clear()         # start with out = 0


	def doTheThing( self, clk, x, write ):

		d = mux_( x, self.ff.q1, write ) # read or write

		self.ff.doTheThing( clk, d )
		

	def out( self ):
		# as fx cause have to wait for values to 'settle'
		return self.ff.q1


class RegisterN_():

	''' N bit register '''

	def __init__( self, N ):

		self.N = N

		self.registers = [ Register_() for i in range( self.N ) ]


	def doTheThing( self, clk, x, write ):

		for i in range( self.N ):

			self.registers[i].doTheThing( clk, x[i], write )  # read or write


	def out( self ):

		return tuple( register.out() for register in self.registers )



'''''''''''''''''''''''''''' RAM '''''''''''''''''''''''''''''

class RAM8_():

	''' 8 register 1 bit RAM '''

	def __init__( self ):

		self.registers = [ Register_() for i in range( 8 ) ]

		self.address = None


	def doTheThing( self, clk, x, write, address ):

		'''
		 In the physical implementation, choosing which register to enable would be
		 via combo use of decoder and tristate buffer.
		 Unable atm to represent z-state of tristate buffer in this emulator.
		'''
		
		self.registers[address].doTheThing( clk, x, write )  # read or write
		
		self.address = address


	def out( self ):

		return self.registers[self.address].out()


class RAM8N_():

	''' 8 register N bit RAM '''

	def __init__( self, N ):

		self.registers = [ RegisterN_( N ) for i in range( 8 ) ]

		self.address = None


	def doTheThing( self, clk, x, write, address ):
		
		self.registers[address].doTheThing( clk, x, write )  # read or write
		
		self.address = address


	def out( self ):

		return self.registers[self.address].out()


class RAMXN_():

	''' X register N bit RAM '''

	def __init__( self, X, N ):

		self.registers = [ RegisterN_( N ) for i in range( X ) ]

		self.address = None


	def doTheThing( self, clk, x, write, address ):
		
		self.registers[address].doTheThing( clk, x, write )  # read or write
		
		self.address = address


	def out( self ):

		return self.registers[self.address].out()



''''''''''''''''''''''''' program counter '''''''''''''''''''''''''''

# class ProgramCounterN_():

# 	''' N bit program counter _ v1 
# 		 - Shortfalls: can't handle cases where more than one of the control values is 1 
# 		                (since uses decoder to assign states e.g. 1000 > 11 > write )
# 	'''

# 	def __init__( self, N ):

# 		self.N = N
		
# 		self.register = RegisterN_( N )


# 	def doTheThing( self, clk, x, write, inc, rst ):
		
# 		change = or3_( write, inc, rst )

# 		action = encoder4to2_( write, inc, rst, not_( change ) )

# 		d = muxN4to1_(

# 			self.N,

# 			x,
# 			incrementN_( self.N, self.register.out() ),
# 			zeroN_( self.N ),
# 			self.register.out(),

# 			action[0], action[1]
# 		)

# 		self.register.doTheThing( clk, d, change )


# 	def out( self ):
		
# 		return self.register.out()


class ProgramCounterN_():

	''' N bit program counter _ v2 

			if    rst(t-1)   : out(t) = 0
			elif  write(t-1) : out(t) = in(t-1)
			elif  inc(t-1)   : out(t) = out(t-1) + 1
			else             : out(t) = out(t-1)
	'''

	def __init__( self, N ):

		self.N = N
		
		self.register = RegisterN_( N )


	def doTheThing( self, clk, x, write, inc, rst ):
		
		change = or3_( write, inc, rst )

		d = muxN_(

				self.N,
				zeroN_( self.N ),
				muxN_(

					self.N,
					x,
					muxN_(

						self.N,
						incrementN_( self.N, self.register.out() ),
						self.register.out(),

						inc 
					),

					write
				),

				rst
			)

		self.register.doTheThing( clk, d, change )


	def out( self ):
		
		return self.register.out()
