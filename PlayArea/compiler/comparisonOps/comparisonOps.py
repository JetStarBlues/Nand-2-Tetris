'''
	Accurate comparisons

	  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Greater-or-less-than-when-comparing-numbers-with-different-signs-td4031520.html
'''

uns = {
	
	  0 : 0,
	  1 : 1,
	  2 : 2,
	  3 : 3,
	- 4 : 4,
	- 3 : 5,
	- 2 : 6,
	- 1 : 7,
}

def isNeg ( x ):

	# x < 0
	return x & 0b100

def isZero ( x ):

	return x == 0

def lt ( x, y ):

	x = uns[ x ]
	y = uns[ y ]

	d = x - y

	if isNeg( x ):

		if not isNeg( y ):

			return True

		# isNeg( x ) and isNeg( y ) - aka same signs

	else:

		if isNeg( y ):

			return False

		# not isNeg( x ) and not isNeg( y ) - aka same signs

	# same signs
	if isNeg( d ):

		return True

	else:

		return False


def lte ( x, y ):

	x = uns[ x ]
	y = uns[ y ]

	d = x - y

	if isNeg( x ):

		if not isNeg( y ):

			return True

		# isNeg( x ) and isNeg( y ) - aka same signs

	else:

		if isNeg( y ):

			return False

		# not isNeg( x ) and not isNeg( y ) - aka same signs

	# same signs
	if isNeg( d ):

		return True

	else:

		if isZero( d ):

			return True

		else:

			return False


def gt ( x, y ):

	return not lte(x, y )


def gte ( x, y ):

	return not lt( x, y )


print( lt(  2,  3 ) )  # true
print( lt( -2, -3 ) )  # false
print( lt(  3,  2 ) )  # false
print( lt( -3, -2 ) )  # true
print( lt(  2,  2 ) )  # false
print()
print( lte(  2,  3 ) )  # true
print( lte( -2, -3 ) )  # false
print( lte(  3,  2 ) )  # false
print( lte( -3, -2 ) )  # true
print( lte(  2,  2 ) )  # true
print()
print( gt(  2,  3 ) )  # false
print( gt( -2, -3 ) )  # true
print( gt(  3,  2 ) )  # true
print( gt( -3, -2 ) )  # false
print( gt(  2,  2 ) )  # false
print()
print( gte(  2,  3 ) )  # false
print( gte( -2, -3 ) )  # true
print( gte(  3,  2 ) )  # true
print( gte( -3, -2 ) )  # false
print( gte(  2,  2 ) )  # true