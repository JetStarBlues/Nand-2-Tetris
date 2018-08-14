'''
    In the spirit of
      http://www.diveintopython3.net/unit-testing.html
      http://www.diveintopython3.net/refactoring.html
    The tutorials show how maintainable and refactorable code becomes when use tests
'''

'''------------------------- Shared functions -------------------------'''

# Formatting ---

def toString( array ):
	return ''.join( map(str, array) )

def toDecimal( bitSeq ):
	return int(bitSeq, 2)

def toDecimal_( iter ):
	return toDecimal( toString( iter ) )	

def toBinary( N, x ):
	if x < 0: x = 2**N + x  # 2s complement
	return bin(x)[2:].zfill(N)

def toBitArray( bitSeq ):
	return tuple( [ int( b ) for b in bitSeq ] )



# Logging ---

def fileName( nestedName ):
	return nestedName.split('.')[-1]

class FailLogger():

	def __init__( self ):

		self.fails = []


	def record( self, expected, result, idx ):

		self.fails.append( [ expected, result, idx ] )


	def report( self, testName ):

		print( '\n-- Finished test ' + testName )

		if self.fails:

			print( '\n--- {} values failed for test {} --- \n'.format( len(self.fails), testName ) )

			for fail in self.fails:
				print( 'exp {}  got {}  at {}'.format( fail[0], fail[1], fail[2] ) )

		else:
					
			print( 'Success! All values match.')
