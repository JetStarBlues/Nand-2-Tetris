'''
	In the spirit of
	  http://www.diveintopython3.net/unit-testing.html
	  http://www.diveintopython3.net/refactoring.html
	The tutorials show how maintainable and refactorable code becomes when use tests
'''

''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

import unittest


# stackoverflow.com/a/13533236/2354735
pattern = '_1__elementary_arithmetic.py'
testsuite = unittest.TestLoader().discover( '.', pattern )


def runTests():
	
	unittest.TextTestRunner().run( testsuite )