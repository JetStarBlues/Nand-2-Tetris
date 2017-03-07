'''
	As shown in this tutorial by Sentdex,
	 www.youtube.com/watch?v=NwH0HvMI4EA
	And
	 https://pymotw.com/3/queue/
'''

import threading
from queue import Queue

class execInParallel():

	def run( self, nThreads, fx, args ):

		self.q = Queue()

		self.action = fx

		self.createJobs( args )

		self.createThreads( nThreads )  # create workers

		self.q.join()

	def performJob( self ):

		while True:

			# Get job from queue
			item = self.q.get()

			# Perform job
			self.action( item )

			# Job completed, indicate available to perform another
			self.q.task_done()

	def createThreads( self, nThreads ):

		for _ in range( nThreads ):

			# Worker
			t = threading.Thread( 

				# name = 'worker-{}'.format( _ ),
				target = self.performJob
			)

			t.daemon = True  # die when main thread dies

			t.start()

	def createJobs( self, jobs ):

		for job in jobs:

			self.q.put( job )


# --------------------------------------------------------

# Example...
'''
s = list( "hello_ryden" )

def printChar( c ): print( c )

def printChar2( c ): print( c * 3 )

e = execInParallel()
e.run( 2, printChar, s )
e.run( 5, printChar2, s )
'''