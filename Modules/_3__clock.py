''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import threading, time


''''''''''''''''''''''''''''''' clock '''''''''''''''''''''''''''''''

class Clock():
	
	''' Uses Python logic and modules ...
		 In mechanical and/or FPGA implementation, this would be
		 handled by an external clock (crsytal oscillator) '''

	def __init__( self ):

		# time stuff
		self.duration = None  	  # seconds
		self.currentCycle = -1    # start at 0

		# wave shape
		self.value = 0
		self.halfPeriod = 1e-4   # seconds

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
		if self.value: 			 	 # 0 to 1
			self.isRising = True
			self.isFalling = False
		else: 					  	 # 1 to 0
			self.isRising = False
			self.isFalling = True


	def run( self ):

		self.halfTick()

		if self.isRising and self.callbackRising:
			self.callbackRising()

		elif self.isFalling and self.callbackFalling:
			self.callbackFalling()

		if time.clock() < self.duration:
			threading.Timer( self.halfPeriod, self.run ).start()
