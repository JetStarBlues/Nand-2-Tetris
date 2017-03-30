'''----------------------------- Imports -----------------------------'''

# Built ins
import threading, time

# Hack computer
from ._x__components import *


'''------------------------------ Clock ------------------------------'''

class Clock():
	
	''' Uses Python logic and modules ...
	     In mechanical and/or FPGA implementation, this would be
	     handled by an external clock (crsytal oscillator) '''

	def __init__( self ):

		# time stuff
		self.duration = 1e99  	  # seconds
		self.currentCycle = -1    # start at 0

		# wave shape
		self.value = 0
		self.halfPeriod = CLOCK_HALF_PERIOD   # seconds

		# psuedo edges
		self.isRising = False
		self.isFalling = False

		# functions to call on edges
		self.callbackRising = None
		self.callbackFalling = None


	def halfTick( self ):

		self.value = 1 - self.value  # flip

		self.currentCycle += self.value  # count clock cycles

		# pseudo edges
		if self.value == 1:		 	 # 0 to 1
			self.isRising = True
			self.isFalling = False
		else: 					  	 # 1 to 0
			self.isRising = False
			self.isFalling = True

		# print("clock half tick at", round(time.time(),8), self.isRising)


	def stop( self ):

		self.duration = time.clock()


	def run( self ):

		threading.Thread(
			target = self.run_,
			name = 'clock_thread'
		).start()


	def run_( self ):	

		while time.clock() < self.duration:

			self.halfTick()

			if self.isRising and self.callbackRising:
				self.callbackRising()

			elif self.isFalling and self.callbackFalling:
				self.callbackFalling()

			time.sleep( self.halfPeriod )
