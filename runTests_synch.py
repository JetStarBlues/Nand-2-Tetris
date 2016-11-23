'''------------------------------ Imports ------------------------------'''

from Tests import *

import multiprocessing



'''------------------------------- Main -------------------------------'''

print( '\n=== Running synchronous tests ===')


tests = Tests.SynchronousTests._x__synchTests.files

if __name__ == '__main__':

	for test in tests:

		startTest = None
		cmd = 'from Tests.SynchronousTests.' + test + ' import start as startTest'
		exec( cmd )

		multiprocessing.Process(
			target = startTest
		).start()
