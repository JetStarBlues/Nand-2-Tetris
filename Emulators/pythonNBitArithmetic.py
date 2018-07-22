class NBitArithmetic ():

	'''
		Emulate N-bit arithmetic using Python's standard arithmetic
		Used by the VM and HL emulators
	'''

	def __init__ ( self, N ):

		self.N = N

		# Keep in sync with 'commonHelpers.py'
		self.negativeOne = 2 ** N - 1
		self.largestInt  = 2 ** ( N - 1 ) - 1


	# Keep in sync with 'commonHelpers.py'
	def trim( self, x ):

		return x & self.negativeOne  # discard overflow bits

	def negate( self, x ):

		return self.trim( ( x ^ self.negativeOne ) + 1 )  # twos complement

	def isNegative( self, x ):

		return x > self.largestInt


	# Arithmetic and logic
	def _not( self, a ):

		return a ^ self.negativeOne  # flip bits

	def _neg( self, a ):

		return self.negate( a )

	def _and( self, a, b ):

		return a & b

	def _or( self, a, b ):

		return a | b

	def _xor( self, a, b ):

		return a ^ b

	def _lsl( self, a, b ):

		return self.trim( a << b )

	def _lsr( self, a, b ):

		return a >> b  # logical shift (assuming a is positive)

	def _add( self, a, b ):

		return self.trim( a + b )

	def _sub( self, a, b ):

		return self.trim( a + self.negate( b ) )

	def _mul( self, a, b ):

		return self.trim( a * b )

	def _div( self, a, b ):

		# Divide using absolutes and add signs after

		aIsNeg = self.isNegative( a )
		bIsNeg = self.isNegative( b )

		# Get absolute values
		if aIsNeg: a = self.negate( a )
		if bIsNeg: b = self.negate( b )

		# Divide
		value = a // b

		# If opposite signs, negate answer
		if aIsNeg ^ bIsNeg:

			value = self.negate( value )

		return value

	def _eq ( self, a, b ):

		d = self._sub( a, b )

		return d == 0

	def _ne ( self, a, b ):

		d = self._sub( a, b )

		return d != 0

	# For gt, gte, lt, lte see discussion here,
	#  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Greater-or-less-than-when-comparing-numbers-with-different-signs-td4031520.html
	#  Code based on @cadet1620's answer

	def _lt ( self, a, b ):

		# return ng               # simple, but inaccurate for opposite signs

		if self.isNegative( a ):

			if not self.isNegative( b ):

				return True

			# aIsNeg and bIsNeg

		else:

			if self.isNegative( b ):

				return False

			# aIsNotNeg and bIsNotNeg

		# same signs
		d = self._sub( a, b )  # won't oveflow

		if self.isNegative( d ):

			return True

		else:

			return False

	def _lte ( self, a, b ):

		# return zr or ng         # simple, but inaccurate for opposite signs

		if self.isNegative( a ):

			if not self.isNegative( b ):

				return True

			# aIsNeg and bIsNeg

		else:

			if self.isNegative( b ):

				return False

			# aIsNotNeg and bIsNotNeg

		# same signs
		d = self._sub( a, b )  # won't oveflow

		if self.isNegative( d ):

			return True

		else:

			return d == 0

	def _gt ( self, a, b ):

		# return not( zr or ng )  # simple, but inaccurate for opposite signs

		return not self._lte( a, b )

	def _gte ( self, a, b ):

		# return not( ng )        # simple, but inaccurate for opposite signs

		return not self._lt( a, b )
