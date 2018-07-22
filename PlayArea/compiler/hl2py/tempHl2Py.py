# Array

def __init__ ( self, size ):  # array is unicorn and doesn't use 'constructor'
def new ( self, size ):

	if size <= 0:

		Sys.error( 2 )

	self.base = DataMemory.alloc( size )

def dispose ( self ):

	DataMemory.dealloc( self.base )

# Array access in lieu of ...
c[b] = 5
... RAM[ c.base + b ] = 5

# HashTable
# LinkedList
# Node
# String
def dispose ( self ):

	self.str.dispose()

	DataMemory.dealloc( self.base )



constructor

	this = DataMemory.alloc( nFields )

	return this


ignore .dispose
ignore DataMemory.alloc/dealloc


def dispose ( self ):

	pass()

String.dispose = dispose





Class ...

	# constants
	p = 789
	q = 5000
	r = - 9

	# statics
	a = 0
	b = 1
	c = 2
	
	def __init__:

		# fields
		self.x = 0
		self.y = 1
		self.z = 2


	def ....:

		# x = 20
		RAM[ self.base + self.x ] = 20



