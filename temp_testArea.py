from Tests import *

# s = bin(34241)[2:].zfill(16)

# # print(s)

# for i in range(20):
# 	s = shiftRightN_( 16, s, '0001' )
# 	# s = shiftLeftN_( 16, s, '0001' )
# 	print(s)


# from Tests.SynchronousTests._2__registerN import start as startTest



from Tests._x__testingHelpers import toBinary as toBin

N = 16
m = 2 ** N - 1

from random import random as rand
from math import floor

def r(x): return math.floor( rand() * x )

for i in range(5):
	x = r(m)
	y = r(15)
	# z = x ^ y
	z = x >> y

	# print(x, y, z)
	print( toBin(N, x), toBin(N, y), toBin(N, z) )

