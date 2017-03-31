# The various components of the Hack computer

from ._0__globalConstants import *
from ._3__clock import *
from ._8__computer import *

if PERFORMANCE_MODE:

	from ._1__elementaryGates_performance import *
	from ._2__arithmetic_performance import *
	from ._5__memory_performance import *
	from ._6__programCounter_performance import *
	from ._7__cpu_performance import *
	from ._9__inputOutput_performance import *

else:

	from ._1__elementaryGates import *
	from ._2__arithmetic import *
	from ._4__flipFlops import *
	from ._5__memory import *
	from ._6__programCounter import *
	from ._7__cpu import *
	from ._9__inputOutput import *
