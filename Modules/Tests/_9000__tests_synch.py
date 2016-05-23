'''
	In the spirit of
	  http://www.diveintopython3.net/unit-testing.html
	  http://www.diveintopython3.net/refactoring.html
	The tutorials show how maintainable and refactorable code becomes when use tests
'''

''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import os


''''''''''''''''''''''''''' tests '''''''''''''''''''''''''''''

files = [

	# Memory
	'_9001__tests_register.py',
	'_9001__tests_registerN.py',
	'_9001__tests_ram8N.py',
	'_9001__tests_ramXN.py',

	# Program counter
	'_9001__tests_programCounterN.py',

]


for file in files:
	print( '>> Running ', file )
	cmd = 'python ' + file
	os.system( cmd )