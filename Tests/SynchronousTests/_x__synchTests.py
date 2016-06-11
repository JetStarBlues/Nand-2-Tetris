'''
    In the spirit of
      http://www.diveintopython3.net/unit-testing.html
      http://www.diveintopython3.net/refactoring.html
    The tutorials show how maintainable and refactorable code becomes when use tests
'''

''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import multiprocessing ###


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''


files = [

	# Memory
	# '_1__register',
	# '_2__registerN',
	# '_3__ram8N',
	# '_4__ramXN',

	# Program counter
	# '_5__programCounterN',

	# Computer
	# '_6__computerN__1',
	# '_6__computerN__2',
	# '_6__computerN__3',
	# '_6__computerN__4',
	# '_6__computerN__5',
	# '_6__computerN__5a',
	# '_6__computerN__6',

	# Computer > Screen ... have to run individually?
	# '_6__computerN__8',
	'_6__computerN__9',

]

def runTests():

	# from .filename import start
	# start()	

	for file in files:

		cmd = 'from .' + file + ' import start'
		exec( cmd )
		exec( 'start()' )

		# startTest = None
		# cmd = 'from .' + file + ' import start as startTest'
		# exec( cmd )

		# multiprocessing.Process( 
		# 	target = startTest 
		# ).start()