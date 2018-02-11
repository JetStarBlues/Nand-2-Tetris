'''
# Original

s = 300
for x in xrange(s):
    for y in xrange(s):
        screen.set_at( (x, y), (red, green, blue) )


# Faster?
screenarray = np.zeros((s,s))
for x in range(100):
    screenarray.fill(?)
    pygame.surfarray.blit_array(screen, screenarray)

'''

import numpy as np

nRows = 2
nCols = 4
z = 3

bgCol = ( 0, 0, 0 )

a = np.full( ( nRows, nCols, z ), bgCol )  # init with value

# print( a )

col2 = ( 9, 9, 9 )

a[1][2] = col2  # change specific location


print( a )

