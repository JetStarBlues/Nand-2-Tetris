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

def programCounter_( x, inc, write, rst ): pass




''''''''''''''''''''''''' Other '''''''''''''''''''''''''

# def tristateBuffer_( c, x ):
# 	# www.cs.umd.edu/class/sum2003/cmsc311/Notes/CompOrg/tristate.html
# 	return ( and_( c, x ) )