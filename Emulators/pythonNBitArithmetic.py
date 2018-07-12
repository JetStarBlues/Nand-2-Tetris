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


	# Local helpers
	def isDiffZrNg( self, a, b ):

		diff = self._sub( a, b )
		zr   = diff == 0
		ng   = self.isNegative( diff )

		return ( zr, ng )

	def isOppositeSigns( self, a, b ):

		return self.isNegative( a ) ^ self.isNegative( b )


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

		zr, ng = self.isDiffZrNg( a, b )

		return zr

	def _ne ( self, a, b ):

		zr, ng = self.isDiffZrNg( a, b )

		return not zr

	# For gt, gte, lt, lte see discussion here,
	#  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Greater-or-less-than-when-comparing-numbers-with-different-signs-td4031520.html

	def _gt ( self, a, b ):

		# value = not( zr or ng )  # simple, but inaccurate for opposite signs

		zr, ng        = self.isDiffZrNg( a, b )
		oppositeSigns = self.isOppositeSigns( a, b )
		aIsNeg        = self.isNegative( a )

		if oppositeSigns:

			value = not aIsNeg

		else:  # same signs

			value = not ( zr or ng )

		return value


	def _gte ( self, a, b ):

		# value = not( ng )        # simple, but inaccurate for opposite signs

		zr, ng        = self.isDiffZrNg( a, b )
		oppositeSigns = self.isOppositeSigns( a, b )
		aIsNeg        = self.isNegative( a )

		if oppositeSigns:

			value = not aIsNeg

		else:  # same signs

			value = not ng

		return value

	def _lt ( self, a, b ):

		# value = ng               # simple, but inaccurate for opposite signs

		zr, ng        = self.isDiffZrNg( a, b )
		oppositeSigns = self.isOppositeSigns( a, b )
		aIsNeg        = self.isNegative( a )

		if oppositeSigns:

			value = aIsNeg

		else:  # same signs

			value = ng

		return value

	def _lte ( self, a, b ):

		# value = zr or ng         # simple, but inaccurate for opposite signs

		zr, ng        = self.isDiffZrNg( a, b )
		oppositeSigns = self.isOppositeSigns( a, b )
		aIsNeg        = self.isNegative( a )

		if oppositeSigns:

			value = aIsNeg

		else:  # same signs

			value = zr or ng

		return value

