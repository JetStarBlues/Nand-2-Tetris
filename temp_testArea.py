from Tests import *

s = bin(34241)[2:].zfill(16)

# print(s)

for i in range(20):
	# s = shiftRightN_( 16, s, 0, 1, 0, 1 )
	s = shiftLeftN_( 16, s, 0, 0, 1, 0 )
	print(s)