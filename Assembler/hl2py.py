# TODO
'''
	Python class not same as Jack class...
	this does not refer to same thing as self
	this
		. Array idx 0
		. Object instance field 0
	self
		. ???

	Need some kind of custom Python class that emulates Jack class
'''

'''
	For perfomance, bypass vm language
	
	Generate equivalent python code

		ex. def fxName ( arg0, arg1 ):
				...

	Use arithmetic class for functions

		ex.

			ALU = NBitArith ( N )

			...

			z = ALU._add( x, y )

	Python/HL emulator

		. RAM as array
		. ...

'''

# TODO: tab levels


'ALU = NBitArithmetic( nBits )'


def compile_classDeclaration ( self, exp ):

	s = ''

	className = exp[ 'name' ]

	s += 'class {}:\n'.format( className )
	s += '\n'

	# constant declarations
	for constant in exp[ 'constDec' ]:

		s += '\t{} = {}\n'.format( constant[ 'name' ], constant[ 'value' ] )

	# static declarations
	for static in exp[ 'varDec' ]:

		s += '\t{} = None\n'.format( static[ 'name' ] )

	#
	s += '\n'


	# subroutine declarations
	for subDec in exp[ 'subDec' ]:

		s += self.compile_subroutineDeclaration( subDec )

	return s


def compile_subroutineDeclaration ( self, exp ):

	s = ''

	fxType = exp[ 'fx_type' ]
	fxName = exp[ 'name' ]

	params = []
	for param in exp[ 'params' ]:

		params.append( param[ 'name' ] )


	'''
		Super kludgy
		1) Treat quirky 'Array.new' as 'constructor' instead of 'function'
		   Kludgy because any code that seeks to exploit behaviour similarly will not work
		   ... no __init__ unless 'constructor'
		2) Overwriting whole function so that can change
		   'return DataMemory.alloc( size )' to
		   self.base = DataMemory.alloc( size )
		   This means any changes in Array.new code need to be mirrored here
	'''
	if self.curClassName == 'Array' and fxName == 'new':

		s += '\tdef __init__ ( self, size ):\n'
		s += '\t\n'
		s += '\t\tif ALU._lte( size, 0 ):\n'
		s += '\t\n'
		s += '\t\t\tSys.error( 2 )\n'
		s += '\t\n'
		s += '\t\tself.base = DataMemory.alloc( size )\n'

		s += '\n'

		return s


	# def
	if fxType == 'method':

		s += 'def {} ( self{} ):\n'.format( 

			fxName,
			( ', ' + ', '.join( params ) ) if params else ''
		)

	elif fxType == 'constructor':  # TODO... check multiple constructors in class???

		s += 'def __init__ ( self{} ):\n'.format(

			( ', ' + ', '.join( params ) ) if params else ''
		)

	elif fxType == 'function':

		s += 'def {} ({}):\n'.format(

			fxName,
			( ' ' + ', '.join( params ) + ' ' ) if params else ''
		)

	s += '\n'


	# local constant declarations
	for constant in exp[ 'constDec' ]:

		s += '\t{} = {}\n'.format( constant[ 'name' ], constant[ 'value' ] )

	# local variable declarations
	for local in exp[ 'varDec' ]:

		s += '\t{} = None\n'.format( local[ 'name' ] )

	s += '\n'


	# statements
	s += self.compile_statements( exp[ 'statements' ] )

	return s


def compile_statements ( self, statements ):

	s = ''

	if statements:

		for statement in statements:

			s += self.compile_statement( statement )

	return s


def compile_statement ( self, exp ):

	if   exp[ 'type' ] == 'subroutineCall'    : return self.compile_subroutineCall( exp )
	elif exp[ 'type' ] == 'assignment'        : return self.compile_letStatement( exp )
	elif exp[ 'type' ] == 'whileStatement'    : return self.compile_whileStatement( exp )
	elif exp[ 'type' ] == 'ifStatement'       : return self.compile_ifStatement( exp )
	elif exp[ 'type' ] == 'forStatement'      : return self.compile_forStatement( exp )
	elif exp[ 'type' ] == 'returnStatement'   : return self.compile_returnStatement( exp )
	elif exp[ 'type' ] == 'breakStatement'    : return self.compile_breakStatement( exp )
	elif exp[ 'type' ] == 'continueStatement' : return self.compile_continueStatement( exp )

	else:
		raise Exception ( "Error: Don't know how to compile the statement " + exp[ 'type' ] )


def compile_subroutineCall ( self, exp ):

	s = ''

	subName = exp[ 'name' ]

	if '.' not in subName:

		# Method of current class
		subName = 'self.' + subName

	# Kludgy workaround for use of 'this' to reference an array's base address
	if subName == 'DataMemory.dealloc':

		if self.curClassName == 'Array':

			# replace 'this' keyword with 'self.base'
			s = 'DataMemory.dealloc( self.base )'

		else:

			# ignore all other calls (typically by object instances to dispose self)
			s = ''

		return

	# args
	args = exp[ 'args' ]

	s_args = []

	if args:
		
		for expr in args:

			s.append( self.compile_expression( expr ) )


	s = '{}({})'.format(

		subName,
		( ' ' + ', '.join( s_args ) + ' ' ) if args else ''
	)

	return s


def compile_letStatement ( self, exp ):

	s = ''



	return s




....

ALUFxLookup_unary = {

	'!'  : '_not',
	'~'  : '_not',
	'-'  : '_neg'
}

ALUFxLookup_binary = {

	# logic
	'&'  : '_and',
	'|'  : '_or',
	'^'  : '_xor',

	# arithmetic
	'+'  : '_add',
	'-'  : '_sub',
	'*'  : '_mul',
	'/'  : '_div',
	'>>' : '_lsr',
	'<<' : '_lsl',
	'%'  : ?,

	# comparison
	'='  : '_eq',
	'==' : '_eq',
	'>'  : '_gt',
	'<'  : '_lt',
	'>=' : '_gte',
	'<=' : '_lte',
	'!=' : '_ne'
}

def compile_binaryOp ( self, op, a, b ):

	if op in ALUFxLookup_binary():

		ALUFx = ALUFxLookup_binary[ op ]

		return 'ALU.{}( {}, {} )'.format( ALUFx, a, b )

	elif op == '%':

		return 'Math.mod( {}, {} )'.format( a, b )

	else:

		raise Exception ( "Error: Don't know how to compile the binaryOp " + op )


def compile_expression ( self, exp ):

	s = ''

	if exp == None:

		return ''

	elif isinstance( exp, dict ):

		return self.compile_expressionTerm( exp )

	else:

		s_a = self.compile_expression( exp[ 0 ] )

		for i in range( 1, len( exp ), 2 ):

			s_b = self.compile_expression( exp[ i + 1 ] )

			s_ab = self.compile_binaryOp( exp[ i ][ 'value' ], s_a, s_b )

			s += s_ab

			s_a = s_ab

	return s


def compile_expressionTerm ( self, exp ):

	s = ''

	expType  = exp[ 'type' ]
	expValue = exp[ 'value' ]

	if expType == 'integerConstant':

		s = exp[ 'value' ]

	elif expType == 'stringConstant':

		'String()' ... ??

		for c in expValue:

			'?.appendChar( {} )'.format( ord( c ) )

	elif expType == 'charConstant':

		s = str( ord( expValue ) )  # Ascii code

	elif expType == 'keywordConstant':

		if expValue == 'true':

			s = 'ALU.negativeOne'

		elif expValue == 'false' or expValue == 'null':

			s = '0'

		elif expValue == 'this':

			... self?

	elif expType == 'identifier':

		name = exp[ 'name' ]

		arrIdx = exp[ 'arrIdx' ]

		if arrIdx:

			s_idx = self.compile_expression( arrIdx )

			s = '{}[ {} ]'.format( name, s_idx )

			... ???

		else:

			s = name

	elif expType == 'subroutineCall':

		return self.compile_subroutineCall( exp )

	elif expType == 'unaryOp':

		s_operand = self.compile_expression( exp[ 'operand' ] )

		op = exp[ 'op' ]

		ALUFx = ALUFxLookup_unary[ op ]

		s = 'ALU.{}( {} )'.format( ALUFx, s_operand )

	else:

		raise Exception ( "Error: Don't know how to compile the expressionTerm " + expType )

	return s

