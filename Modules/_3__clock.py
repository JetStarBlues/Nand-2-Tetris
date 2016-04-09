''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import threading, time


''''''''''''''''''''''''''''''' clock '''''''''''''''''''''''''''''''

class Clock():
	''' Uses Python logic and modules ...
		 In mechanical and/or FPGA implementation, this would be
		 handled by an external clock (crsytal oscillator) '''

	def __init__(self):

		self.value = 0
		self.halfPeriod = 1e-4   # seconds

		self.currentCycle = -1   # start at 0

		# psuedo edges
		self.isRising = False
		self.isFalling = False


	def halfTick(self):

		self.value = 1 - self.value  # flip

		self.currentCycle += self.value  # count clock cycles

		# pseudo edges
		if self.value: 			 	 # 0 to 1
			self.isRising = True
			self.isFalling = False
		else: 					  	 # 1 to 0
			self.isRising = False
			self.isFalling = True


	def keepTicking(self, duration, callback):

		if time.clock() < duration: # seconds
			threading.Timer( self.halfPeriod, callback ).start()
