# FSM using high level programming language

''''''''''''''''''''''''' Helpers '''''''''''''''''''''''''''''''''

class StackFSM():

	''' http://gamedevelopment.tutsplus.com/tutorials/finite-state-machines-theory-and-implementation--gamedev-11867 '''

	def __init__(self):

		self.stack = []


	def getCurrentState(self):

		if len(self.stack) > 0 :
			return self.stack[-1]
		else:
			return None

	def popState(self):

		self.stack.pop()

	def pushState(self, state):

		if self.getCurrentState() != state :
			self.stack.append(state)

	def update(self):

		currentStateFunction = self.getCurrentState()

		if currentStateFunction != None :            
			currentStateFunction()


''''''''''''''''''''''''' Main '''''''''''''''''''''''''''''''''

class Thing():

	# detect 101 or 11

	def __init__(self):

		self.sManager = StackFSM()
		self.sManager.pushState(self.state0)

		self.input = None


	def update(self):

		self.sManager.update()


	def state0(self):

		print("reset")

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state1)

		else :
			pass


	def state1(self):

		print("detected 1")

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state3)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state2)


	def state2(self):

		print("detected 10")

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state4)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state0)



	def state3(self):

		print("detected 11")   

		if self.input :
			pass
			# self.sManager.popState()
			# self.sManager.pushState(self.state1)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state2)


	def state4(self):

		print("detected 101")   

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state3)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state2)


class Thing_stateReduced():

	# detect 101 or 11

	def __init__(self):

		self.sManager = StackFSM()
		self.sManager.pushState(self.state0)

		self.input = None


	def update(self):

		self.sManager.update()


	def state0(self):

		print("reset")

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state1)
		else :
			pass


	def state1(self):

		print("detected 1")

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state3)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state2)


	def state2(self):

		print("detected 10")

		if self.input :
			self.sManager.popState()
			self.sManager.pushState(self.state3)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state0)


	def state3(self):

		print("detected 11 or 101")   

		if self.input :
			pass
			# self.sManager.popState()
			# self.sManager.pushState(self.state1)

		else :
			self.sManager.popState()
			self.sManager.pushState(self.state2)


''''''''''''''''''''''''' Run '''''''''''''''''''''''''''''''''

# sequence = [1,1,0,1,0,1,1,0,1,1,0,1,0,0,1,1,0]

sequence = [0,1,1,1,0,1,1,0,1,0,0,1,1,0]
sequence.reverse()

thing = Thing()

for input in sequence:

	thing.input = input
	thing.update()

	print( input )

print("\n---")

thing2 = Thing_stateReduced()

for input in sequence:

	thing2.input = input
	thing2.update()

	print( input )