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



print( AClass.a )

B = AClass( 99 )

print( B.a )

AClass.notSpecific()
# B.notSpecific()  # throws error

# AClass.specific()  # throws error
B.specific()

B.specific2()
