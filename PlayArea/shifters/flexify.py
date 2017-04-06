import math

def and_( a, b ):
	return ( int( a ) & int( b ) )

def or_( a, b ):
	return ( int( a ) | int( b ) )	

def not_( x ):
	return 1 if int( x ) == 0 else 0	

def mux_( d1, d0, sel ):

	out = or_(
		and_( not_( sel ), d0 ),
		and_( sel, d1 )
	)
	return out

def toBin_( N, x ):

	return bin(x)[2:].zfill( N )

def shiftRight16_( x, y ):

	''' 16 bit barrel shifter (right) '''

	N = 16

	t0 = [ None ] * N
	t1 = [ None ] * N
	t2 = [ None ] * N
	t3 = [ None ] * N

	y = y[::-1] # make life simpler by matching array access to MSB-to-LSB format

	#
	for i in range( N - 1, 0, -1 ):

		t0[i] = mux_( x[ i - 1 ], x[i], y[0] )

	t0[0] = mux_( 0, x[0], y[0] )

	#
	for i in range( N - 1, 1, -1 ):

		t1[i] = mux_( t0[ i - 2 ], t0[i], y[1] )

	t1[1] = mux_( 0, t0[1], y[1] )
	t1[0] = mux_( 0, t0[0], y[1] )

	#
	for i in range( N - 1, 3, -1 ):

		t2[i] = mux_( t1[ i - 4 ], t1[i], y[2] )

	t2[3] = mux_( 0, t1[3], y[2] )
	t2[2] = mux_( 0, t1[2], y[2] )
	t2[1] = mux_( 0, t1[1], y[2] )
	t2[0] = mux_( 0, t1[0], y[2] )	

	#
	for i in range( N - 1, 7, -1 ):

		t3[i] = mux_( t2[ i - 8 ], t2[i], y[3] )

	t3[7] = mux_( 0, t2[7], y[3] )
	t3[6] = mux_( 0, t2[6], y[3] )
	t3[5] = mux_( 0, t2[5], y[3] )
	t3[4] = mux_( 0, t2[4], y[3] )
	t3[3] = mux_( 0, t2[3], y[3] )
	t3[2] = mux_( 0, t2[2], y[3] )
	t3[1] = mux_( 0, t2[1], y[3] )
	t3[0] = mux_( 0, t2[0], y[3] )

	return t3

def shiftRight( N, x, y ):

	''' Shifts y % 16 spaces
	     cause 2**ns and ns is 4 ...
	     ns is 4 cause coded it as such
	'''

	# y = y[ : : -1 ]

	# ns = int( math.log( N, 2 ) )
	ns = 5

	t = []

	for i in range( ns ):

		t.append( [ None ] * N )

	for j in range( ns ):

		p2 = 2 ** j

		h = x if j == 0 else t[ j - 1 ]

		y_idx = N - j - 1

		for i in range( N - 1, p2 - 1, -1 ):

			t[ j ][ i ] = mux_( h[ i - p2 ], h[ i ], y[ y_idx ] )

		for k in range( p2 - 1, -1, -1 ):

			t[ j ][ k ] = mux_( 0, h[ k ], y[ y_idx ] )

	return t[ ns - 1 ]

N = 16

x = 2**15
y = 16  # Should I just use asm code to return 0 when y >= 16 ???

# print( shiftRight( N, toBin_( N, x ), toBin_( N, y ) ) )
# print( shiftRight16_( toBin_( N, x ), toBin_( N, y ) ) )


def shiftLeft16_( x, y ):

	''' 16 bit barrel shifter (left) '''

	N = 16

	t0 = [ None ] * N
	t1 = [ None ] * N
	t2 = [ None ] * N
	t3 = [ None ] * N

	y = y[::-1] # make life simpler by matching array access to MSB-to-LSB format

	#
	t0[N - 1] = mux_( 0, x[N - 1], y[0] )
	
	for i in range( N - 2, -1, -1 ):

		t0[i] = mux_( x[ i + 1 ], x[i], y[0] )

	#
	t1[ N - 1 ] = mux_( 0, t0[ N - 1 ], y[1] )
	t1[ N - 2 ] = mux_( 0, t0[ N - 2 ], y[1] )

	for i in range( N - 3, -1, -1 ):

		t1[i] = mux_( t0[ i + 2 ], t0[i], y[1] )

	#
	t2[ N - 1 ] = mux_( 0, t1[ N - 1 ], y[2] )
	t2[ N - 2 ] = mux_( 0, t1[ N - 2 ], y[2] )
	t2[ N - 3 ] = mux_( 0, t1[ N - 3 ], y[2] )
	t2[ N - 4 ] = mux_( 0, t1[ N - 4 ], y[2] )

	for i in range( N - 5, -1, -1 ):

		t2[i] = mux_( t1[ i + 4 ], t1[i], y[2] )

	#
	t3[ N - 1 ] = mux_( 0, t2[ N - 1 ], y[3] )
	t3[ N - 2 ] = mux_( 0, t2[ N - 2 ], y[3] )
	t3[ N - 3 ] = mux_( 0, t2[ N - 3 ], y[3] )
	t3[ N - 4 ] = mux_( 0, t2[ N - 4 ], y[3] )
	t3[ N - 5 ] = mux_( 0, t2[ N - 5 ], y[3] )
	t3[ N - 6 ] = mux_( 0, t2[ N - 6 ], y[3] )
	t3[ N - 7 ] = mux_( 0, t2[ N - 7 ], y[3] )
	t3[ N - 8 ] = mux_( 0, t2[ N - 8 ], y[3] )

	for i in range( N - 9, -1, -1 ):
		
		t3[i] = mux_( t2[ i + 8 ], t2[i], y[3] )

	#
	return t3

def shiftLeft( N, x, y ):

	ns = 4

	t = []

	for i in range( ns ):

		t.append( [ None ] * N )

	for j in range ( ns ):

		p2 = 2 ** j

		h = x if j == 0 else t[ j - 1 ]

		y_idx = N - j - 1

		for k in range( N - 1, N - 1 - p2 , -1 ):

			t[ j ][ k ] = mux_( 0, h[ k ], y[ y_idx ] )

		for i in range( N - 1 - p2, -1, -1 ):

			t[ j ][ i ] = mux_( h[ i + p2 ], h[ i ], y[ y_idx ] )

	return t[ ns - 1 ]

x = 3
y = 15  # Should I just use asm code to return 0 when y >= 16 ???

print( shiftLeft( N, toBin_( N, x ), toBin_( N, y ) ) )
print( shiftLeft16_( toBin_( N, x ), toBin_( N, y ) ) )



'''
if y < 16
	return x >> y
else
	return 0
'''