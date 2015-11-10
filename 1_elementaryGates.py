''''''''''''''''''''' The elementary logic gates '''''''''''''''''''''

def _and(a,b):
	return (a & b)

def _or(a,b):
	return (a | b)	

def _xor(a,b):
	return (a ^ b)

def _not(x):
	if x == 0:
		return 1
	else:
		return 0	


''''''''''''''''''''''''' And their inverses '''''''''''''''''''''''''

def _nand(a,b):
	return _not(a & b)

def _nor(a,b):
	return _not(a | b)

def _xnor(a,b):
	return _not(a ^ b)


''''''''''''''''''''''' Other elementary gates '''''''''''''''''''''''

# def _1to2Decoder(a):
# 	return (a, _not(a))

def _mux(a,b,sel):
	''' 2to1 multiplexor is equivalent to an if/else statement of form,
			out = a if sel == 0
				  b if sel == 1

		Or in boolean algebra
			out = ( s * b ) + ( !s * a )

		See http://electronics.stackexchange.com/a/15410
	''' 
	sb = _and( sel, b )
	nsa = _and( _not(sel), a )
	return _or( sb, nsa )

def _4to1Mux(a,b,c,d,s1,s2):

	''' out = a if sel == 00
		      b if sel == 01
		      c if sel == 10
		      d if sel == 11  '''

	# ''' using elementary gates '''
	# p1 = _and( _and( a, _not(s1) ), _not(s2) )
	# p2 = _and( _and( b, _not(s1) ),      s2  )
	# p3 = _and( _and( c,      s1  ), _not(s2) )
	# p4 = _and( _and( d,      s1  ),      s2  )
	# return _or( _or( p1, p2 ), _or( p3, p4 ) )

	''' using other mux chips '''
	p1 = _mux(a,b,s2)
	p2 = _mux(c,d,s2)
	return _mux(p1,p2,s1)

def _8to1Mux(a,b,c,d,e,f,g,h,s1,s2,s3):

	''' out = a if sel == 000
		      b if sel == 001
		      c if sel == 010
		      d if sel == 011
		      e if sel == 100
		      f if sel == 101
		      g if sel == 110
		      h if sel == 111  '''

	# ''' using elementary gates '''
	# p1 = _and( _and( a, _not(s1) ), _and( _not(s2), _not(s3) ) )
	# p2 = _and( _and( b, _not(s1) ), _and( _not(s2),      s3  ) )
	# p3 = _and( _and( c, _not(s1) ), _and(      s2 , _not(s3) ) )
	# p4 = _and( _and( d, _not(s1) ), _and(      s2 ,      s3  ) )
	# p5 = _and( _and( e,      s1  ), _and( _not(s2), _not(s3) ) )
	# p6 = _and( _and( f,      s1  ), _and( _not(s2),      s3  ) )
	# p7 = _and( _and( g,      s1  ), _and(      s2 , _not(s3) ) )
	# p8 = _and( _and( h,      s1  ), _and(      s2 ,      s3  ) )
	# return _or8Way( [p1,p2,p3,p4,p5,p6,p7,p8] )

	''' using other mux chips '''
	p1 = _4to1Mux(a,b,c,d,s2,s3)
	p2 = _4to1Mux(e,f,g,h,s2,s3)
	return _mux(p1,p2,s1)

def _dMux(x,sel):
	'''	[a, b] = [x, 0] if sel == 0
				 [0, x] if sel == 1
	'''
	a = _and( x, _not(sel) )
	b = _and( x, sel )
	return (a,b)

def _1to4DMux(x,s1,s2):

	# ''' using elementary gates '''
	# a = _and( _and( x, _not(s1)), _not(s2) )
	# b = _and( _and( x, _not(s1)),      s2  )
	# c = _and( _and( x,      s1 ), _not(s2) )
	# d = _and( _and( x,      s1 ),      s2  )
	# return (a,b,c,d)

	''' using other dMux chips 
	      www.allaboutcircuits.com/textbook/digital/chpt-9/demultiplexers
	'''
	p1 = _dMux(x,s1)
	p2 = _dMux(p1[0],s2)
	p3 = _dMux(p1[1],s2)
	return ( p2[0], p2[1], p3[0], p3[1] )

def _1to8DMux(x,s1,s2,s3):
	p1 = _dMux(x,s1)
	p2 = _1to4DMux(p1[0],s2,s3)
	p3 = _1to4DMux(p1[1],s2,s3)
	return ( p2[0],p2[1],p2[2],p2[3],p3[0],p3[1],p3[2],p3[3] )



''''''''''''''''''''''''''' N-bit variants '''''''''''''''''''''''''''

# Basically not4() is equivalenet to having 4 not gates each processing
#   a bit in parallel (same time)

def _notN(N,x):
	return ''.join( str( _not( int(x[i]) ) ) for i in range(N) )

def _andN(N,a,b):
	return ''.join( str( _and( int(a[i]), int(b[i]) ) ) for i in range(N) )

def _orN(N,a,b):
	return ''.join( str( _or( int(a[i]), int(b[i]) ) ) for i in range(N) )

def _muxN(N,a,b,sel):
	return ''.join( str( _mux( int(a[i]), int(b[i]), int(sel) ) ) for i in range(N) )

def _4to1MuxN(N,a,b,c,d,s1,s2):
	return ''.join( str( _4to1Mux( 
									int(a[i]), int(b[i]), int(c[i]), int(d[i]),
									int(s1), int(s2)
							     ) ) for i in range(N) )

def _8to1MuxN(N,a,b,c,d,e,f,g,h,s1,s2,s3):
	return ''.join( str( _8to1Mux( 
									int(a[i]), int(b[i]), int(c[i]), int(d[i]),
									int(e[i]), int(f[i]), int(g[i]), int(h[i]),
									int(s1), int(s2), int(s3)
							     ) ) for i in range(N) )


''''''''''''''''''''''''' multi-way variants '''''''''''''''''''''''''

def _orNWay(x):
	# technically, could break once reach a one ...
	#   but is break doable with logic gates???
	out = int( x[0] )
	for i in range(1, len(x)):
		out = _or( out, int( x[i] ) )
	return out

	''' alternate way, takes advantage of using gates in parallel 
		> speed savings if physical implementation
	    https://github.com/havivha/Nand2Tetris/blob/master/02/Or8Way.hdl
	    t1 = or (in[0], in[1])
	    t2 = or (in[2], in[3])
	    t3 = or (in[4], in[5])
	    t4 = or (in[6], in[7])
	    t5 = or (t1, t2)
	    t6 = or (t3, t4)
	    t7 = or (t5, t6)
	    return t7  '''

def _or8Way(x):
	t1 = _or( int(x[0]), int(x[1]) )
	t2 = _or( int(x[2]), int(x[3]) )
	t3 = _or( int(x[4]), int(x[5]) )
	t4 = _or( int(x[6]), int(x[7]) )
	t5 = _or( t1, t2 )
	t6 = _or( t3, t4 )
	t7 = _or( t5, t6 )
	return t7
