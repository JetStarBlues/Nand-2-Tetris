# Hack Computer
from Components import *

#
if PERFORMANCE_MODE:

	raise Exception( 'HardwareTests only work when GC.PERFORMANCE_MODE is False' )


# Tests
from HardwareTests._x__testingHelpers import *
from HardwareTests.KnownValues import *
import HardwareTests.AsynchronousTests