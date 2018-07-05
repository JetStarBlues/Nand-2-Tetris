# TODO
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


def compile_classDeclaration( self, exp ):

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


def compile_subroutineDeclaration( self, exp ):

	s = ''

	fxType = exp[ 'fx_type' ]
	fxName = exp[ 'name' ]

	params = []
	for param in exp[ 'params' ]:

		params.append( param[ 'name' ] )


	# def
	if fx_type == 'method':

		s += 'def {} ( self{} ):\n'.format( 

			fxName,
			( ', ' + ', '.join( params ) ) if params else ''
		)

	elif fx_type == 'constructor':

		s += 'def __init__ ( self{} ):\n'.format(

			( ', ' + ', '.join( params ) ) if params else ''
		)

	elif fx_type == 'function':

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


def compile_statements( self, statements ):

	s = ''

	if statements:

		for statement in statements:

			s += self.compile_statement( statement )

	return s


def compile_statement( self, exp ):

	if   exp[ 'type' ] == 'subroutineCall'    : return self.compile_subroutineCall( exp )
	elif exp[ 'type' ] == 'assignment'        : return self.compile_letStatement( exp )
	elif exp[ 'type' ] == 'whileStatement'    : return self.compile_whileStatement( exp )
	elif exp[ 'type' ] == 'ifStatement'       : return self.compile_ifStatement( exp )
	elif exp[ 'type' ] == 'forStatement'      : return self.compile_forStatement( exp )
	elif exp[ 'type' ] == 'returnStatement'   : return self.compile_returnStatement( exp )
	elif exp[ 'type' ] == 'breakStatement'    : return self.compile_breakStatement( exp )
	elif exp[ 'type' ] == 'continueStatement' : return self.compile_continueStatement( exp )

	else:
		self.croak( "Error: Don't know how to compile the statement " + exp[ 'type' ] )


def compile_subroutineCall( self, exp ):

	s = ''

	subName = exp[ 'name' ]

	if '.' not in subName:

		# Method of current class
		subName = 'self.' + subName


	# args
	args = exp[ 'args' ]

	s_args = ''  # TODO ???

	if args:
		
		for expr in args:

			s += self.compile_expression( expr )


	s = '{}({})'.format(  # tab levels??

		subName,
		( ' ' + ', '.join( args ) + ' ' ) if args else ''
	)

	return s


....


def compile_binaryOp( self, op ):

	# Logic ---
	if   op == '&':
	elif op == '|':
	elif op == '^':

	# Arithmetic ---
	elif op == '+':
	elif op == '-':
	elif op == '%':
	elif op == '*':
	elif op == '/':
	elif op == '>>':
	elif op == '<<':

	# Comparison ---
	elif op == '=' or op == '==':
	elif op == '>':
	elif op == '<':
	elif op == '>=':
	elif op == '<=':
	elif op == '!=':

	# ---
	else:
		self.croak( "Error: Don't know how to compile the binaryOp " + op )


def compile_expression( self, exp ):

	s = ''




	return s



