'''
	As shown in this tutorial by Sentdex,
	 www.youtube.com/watch?v=NwH0HvMI4EA
'''

import threading
from queue import Queue


def threader( q, fx, args ):

	while True:

		jobNumber = q.get()  # Worker commits to performing job

		j = ( jobNumber, )  # append to args...

		fx( * ( args + j ) )  # Worker performs job

		q.task_done() # Worker completed job, available to perform another


def createThreads( q, nThreads, fx, args ):

	for _ in range( nThreads ):

		# Worker
		t = threading.Thread( 

			target = threader,
			args = ( q, fx, args )

		)

		t.daemon = True  # die when main thread dies

		t.start()


def createJobs( q, nJobs ):

	for jobNumber in range(nJobs):

		q.put( jobNumber )

	q.join()


def execInParallel( nThreads, fx, args ):

	q = Queue()

	createThreads( q, nThreads, fx, args )

	createJobs( q, nThreads )  # one job per thread
