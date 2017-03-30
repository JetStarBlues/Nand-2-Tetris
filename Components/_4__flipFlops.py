'''----------------------------- Imports -----------------------------'''

# Built ins
import threading, time
from random import random

# Hack computer
from ._x__components import *


'''--------------------------- Flip flops ---------------------------'''

class JKFlipFlop():

	def __init__( self ):

		# Assign random start values
		#  Truer to indeterminate startup state
		#  http://forum.allaboutcircuits.com/threads/sr-latch-initial-output-values.80855/
		self.q0  = 0 if random() >= 0.5 else 1
		self._q0 = not_( self.q0 )

		# Output. Initialize with random value
		self.q1  = 0 if random() >= 0.5 else 1
		self._q1 = not_( self.q1 )

		# Faux mechanical delay
		self.propogationDelay = CLOCK_HALF_PERIOD * 0.2 #seconds


	def doTheThing( self, e, j, k ):
		
		# https://pymotw.com/2/threading/

		# execute only after delay...
		t = threading.Timer(

			self.propogationDelay,
			self.doTheThing_,
			args = ( e, j, k )
		)
		t.setName( 'jkff_thread' )
		t.start()


	def doTheThing_( self, e, j, k ):

		# print( "executing ", threading.currentThread().getName() )

		#
		r = and_( e, k )
		s = and_( e, j )
		# feedback to prevent 'invalid'
		r = and_( r, self.q0 )
		s = and_( s, self._q0 )

		#
		self.q1  = nor_( r, self._q0 )
		self._q1 = nor_( s, self.q0 )

		# do it twice (write requires twice)
		#  see math/logic here https://youtu.be/XETZoRYdtkw
		self.q0  = self.q1;
		self._q0 = self._q1;
		self.q1  = nor_( r, self._q0 );
		self._q1 = nor_( s, self.q0 );

		# Set cur to prev in prep for next call
		self.q0  = self.q1
		self._q0 = self._q1


	def clear( self ):

		self.q1  = 0
		self._q1 = 1


	def preset( self ):

		self.q1  = 1
		self._q1 = 0


class DFlipFlop():

	def __init__( self ):

		# Assign random start values
		#  Truer to indeterminate startup state
		#  http://forum.allaboutcircuits.com/threads/sr-latch-initial-output-values.80855/
		self.q0  = 0 if random() >= 0.5 else 1
		self._q0 = not_( self.q0 )

		# Output. Initialize with random value
		self.q1  = 0 if random() >= 0.5 else 1
		self._q1 = not_( self.q1 )

		# Faux mechanical delay
		self.propogationDelay = CLOCK_HALF_PERIOD * 0.2 #seconds


	def doTheThing( self, e, d ):
		
		# execute only after delay...
		t = threading.Timer(

			self.propogationDelay,
			self.doTheThing_,
			args = ( e, d )
		)
		t.setName( 'dff_thread' )
		t.start()


	def doTheThing_( self, e, d ):

		#
		r = and_( e, not_( d ) )
		s = and_( e, d )

		#
		self.q1  = nor_( r, self._q0 )
		self._q1 = nor_( s, self.q0 )

		# do it twice (write requires twice)
		#  see math/logic here https://youtu.be/XETZoRYdtkw
		self.q0  = self.q1;
		self._q0 = self._q1;
		self.q1  = nor_( r, self._q0 );
		self._q1 = nor_( s, self.q0 );

		# Set cur to prev in prep for next call
		self.q0  = self.q1
		self._q0 = self._q1


	def clear( self ):

		self.q1  = 0
		self._q1 = 1


	def preset( self ):

		self.q1  = 1
		self._q1 = 0
