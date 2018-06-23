'''----------------------------- Imports -----------------------------'''

# Built ins
from random import random

# Hack computer
from ._x__components import *



'''--------------------------- Flip flops ---------------------------'''

class DFlipFlop():

	def __init__( self ):

		# Assign random start values. Truer to indeterminate startup state
		self.q  = 0 if random() >= 0.5 else 1
		self._q = not_( self.q )


	def doTheThing( self, e, clear_, set_, d ):

		if clear_:

			self.clear()
			return

		elif set_:

			self.set()
			return

		else:

			self.q = d
			self._q = not_( self.q )


	def read( self ):

		return self.q


	def clear( self ):

		self.q  = 0
		self._q = 1


	def set( self ):

		self.q  = 1
		self._q = 0
