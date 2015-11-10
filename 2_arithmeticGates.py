''''''''''''''''''''''''''''''' adders '''''''''''''''''''''''''''''''

def _halfAdder(a,b):
	sum = _xor(a,b)
	carry = _and(a,b)
	return (sum, carry)

def _fullAdder(a,b,c):
	sumTemp, carryTemp1 = _halfAdder(a,b)
	sum, carryTemp2 = _halfAdder(c, sumTemp)
	carry = _or(carryTemp1, carryTemp2)
	return (sum, carry)

def _addN(N,a,b):
	''' N bit adder, takes and outputs Nbit numbers '''
	sum = [None]*N
	c = 0
	for i in range(N-1, -1, -1):  #(N-1)..0
		sum[i], c = _fullAdder( int(a[i]), int(b[i]), c )
	return ''.join(str(b) for b in sum)

# def _add16(a,b):
# 	''' 16 bit adder, takes and outputs 16bit numbers '''
# 	return _addN(16,a,b)

def zero(N):
	return [0]*N

def one(N):
	return [0]*(N-1) + [1]

def _increment(x):
	''' increment by one bit '''
	N = len(x)
	b = one(N)
	return _addN(N,x,b)


''''''''''''''''''''''''''''' negation '''''''''''''''''''''''''''''

def _add1(x):
	''' is this implementable with logic gates? See vid 2.3
		Doubt it atm due to if-statement '''
	# special case, keep flipping RtoL till flip a zero
	sum = [int(b) for b in x]
	for i in range( len(sum)-1, -1, -1):
		if sum[i] == 0:   # Todo: change this to use logic gates
			sum[i] = _not(sum[i])
			break
		sum[i] = _not(sum[i])
	return ''.join(str(b) for b in sum)

def _negate(x):
	''' 2s complement ->  -x = 2^n - x = (2^n - 1) - x + 1 '''
	## (2^n - 1) - x aka flip x's bits
	temp = [int(b) for b in x]
	for i in range( len(temp) ):
		temp[i] = _not(temp[i])

	## Add 1
	return _add1(temp)   		# uses _add1 (shortcut?)
	# return _increment(temp)   # uses _fullAdder

'''
  implement carry-lookahead adder for faster speeds 
  -> even though more calcs takes less time see vid 2.6 '''


''''''''''''''''''''''' Arithmetic Logic Unit '''''''''''''''''''''''
def _isZero(x):
	''' how to do this with logic gates??? 
           ...how check equality if two numbers?
		'''
	isZ = 1
	for b in x:
		if int(b) == 1:
			isZ = 0
			break
	return isZ


def _ALU (x,y,zx,nx,zy,ny,f,no):
	N = 16 # 16 bit ALU

	'''
	out, zr, ng = [None, 0, 0]
	if zx == 1 : x = zero(N)
	if nx == 1 : x = _notN(N,x)
	if zy == 1 : y = zero(N)
	if ny == 1 : y = _notN(N,y)
	if  f == 1 : out = _addN(N,x,y)
	if  f == 0 : out = _andN(N,x,y)
	if no == 1 : out = _notN(N,out)
	if out == 0: zr = 1
	if out < 0 : ng = 1

	return (out, zr, ng) '''

	x = _muxN( N, x, zero(N), zx )
	x = _muxN( N, x, _notN( N, x ), nx )
	y = _muxN( N, y, zero(N), zy )
	y = _muxN( N, y, _notN( N, y ), ny )
	out = _muxN( N, _andN( N, x, y), _addN( N, x, y), f )
	out = _muxN( N, out, _notN( N, out ), no )
	zr = _muxN( N, zero(N), one(N), _isZero(out) )
	ng = _muxN( N, zero(N), one(N), int(out[0]) )  # leftmost bit is a one

	# return (out, int(zr[N-1]), int(ng[N-1]) )
	return (out, zr, ng )
