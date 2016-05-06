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

	''' n bit register '''

	def __init__( self, N ):

		self.N = N

		self.registers = [ Register_() for i in range( self.N ) ]


	def doTheThing( self, clk, x, write ):

		for i in range( self.N ): # fix me

			self.registers[i].doTheThing( clk, x[i], write )  # read or write


	def out( self ):

		return tuple( register.out() for register in self.registers )




'''''''''''''''''''''''''''' RAM '''''''''''''''''''''''''''''

def RAM8_( x, addr, write ): pass
def RAMN8_(): pass

def RAMX_(): pass
def RAMNX_(): pass


''''''''''''''''''''''''' program counter '''''''''''''''''''''''''''

def programCounter_( x, inc, write, rst ): pass




''''''''''''''''''''''''' Other '''''''''''''''''''''''''

# def tristateBuffer_( c, x ):
# 	# www.cs.umd.edu/class/sum2003/cmsc311/Notes/CompOrg/tristate.html
# 	return ( and_( c, x ) )