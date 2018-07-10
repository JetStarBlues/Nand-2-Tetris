# https://stackoverflow.com/a/68672

class AClass:

	a = 5  # declare outside method

	def __init__ ( self, moi ):

		self.a = moi

	def specific( self ):

		print( 'Huh' )

	def notSpecific():  # omit self arg

		print( 'Hmmm' )

	def specific2( self ):

		print( 'Oy', AClass.a )

	def getSelf( self ):

		return self

	def overrideTest( self ):  # https://stackoverflow.com/a/17757360

		print( 'Override failed' )



print( AClass.a )

B = AClass( 99 )

print( B.a )

AClass.notSpecific()
# B.notSpecific()  # throws error

# AClass.specific()  # throws error
B.specific()

B.specific2()

C = B.getSelf()
print( B == C )
print( C.a )
C.a = 50
print( B.a )

def overrideTest( self ):

	print( 'Override success' )

AClass.overrideTest = overrideTest

B.overrideTest()
