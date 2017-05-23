'''------------------------------ Imports ------------------------------'''

import HardwareTests

import multiprocessing



'''------------------------------- Main -------------------------------'''

print( '\n=== Running synchronous tests ===')


tests = HardwareTests.SynchronousTests._x__synchTests.files

if __name__ == '__main__':

	for test in tests:

		startTest = None
		cmd = 'from HardwareTests.SynchronousTests.' + test + ' import start as startTest'
		exec( cmd )

		multiprocessing.Process(
			target = startTest
		).start()
