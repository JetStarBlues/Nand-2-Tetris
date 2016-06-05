'''
    In the spirit of
      http://www.diveintopython3.net/unit-testing.html
      http://www.diveintopython3.net/refactoring.html
    The tutorials show how maintainable and refactorable code becomes when use tests
'''

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
	'_6__computerN'

]

def runTests():

	# from .filename import start
	# start()	

	for file in files:

		cmd = 'from .' + file + ' import start'
		exec( cmd )
		exec( 'start()' )