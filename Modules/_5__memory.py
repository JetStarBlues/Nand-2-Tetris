''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Computer files
from _1__elementaryGates import *
from _2__arithmeticGates import *
from _4__flipFlops import *


''''''''''''''''''''''''''' registers '''''''''''''''''''''''''''''

class register_():

	''' 1 bit register '''

	def __init__(self):

		self.ff = DFlipFlop()


	def doTheThing(self, clk, x, write):

		d = mux_( x, self.ff.q1, write )

		self.ff.doTheThing( clk, d )



def registerN_( N ): pass


''''''''''''''''''''''''''''''' RAM ''''''''''''''''''''''''''''''''

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