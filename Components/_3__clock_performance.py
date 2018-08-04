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

		self.tick = True

		self.currentCycle = 0    # start at 0

		self.value = False

		self.callbackRising = None
		# self.callbackFalling = None


	def halfTick( self ):

		self.value = not( self.value )  # flip

		self.currentCycle += 0.5  # count clock cycles


	def stop( self ):

		self.tick = False


	def run( self ):

		threading.Thread(

			target = self.run_,
			name = 'clock_thread',
			daemon = False

		).start()


	def run_( self ):	

		while self.tick:

			self.halfTick()

			# rising edge
			if self.value and self.callbackRising:
				self.callbackRising()

			# falling edge
			# if not( self.value ) and self.callbackFalling:
			# 	self.callbackFalling()
