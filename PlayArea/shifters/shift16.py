'''
	As is can shift max '1111' -> 15 on one command...
	So a call like shift(20) would need to be split up...
	  Thinking the user should do this when coding... or
	  could be stdlib fx that does this...

	If want to do shift(16) in one cycle, can add s4 support
	(and correspoinding 16muxes) to hardware... revisit as needed
'''

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

	#
	return t3


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