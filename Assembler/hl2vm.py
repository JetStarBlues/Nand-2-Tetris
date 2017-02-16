keywords = [

	'class',        #.
	'constructor',  #.
	'method',       #.
	'this',
	'field',
	'static',
	
	'function',     #.
	'var',

	'let',
	'do',
	'if',
	'else',
	'while',
	# 'for',
	'return',

	'int',
	'char',
	'boolean',
	'void',
	
	'true',
	'false',
	'null',
]

symbols = [ seperators, unary_operators, binary_operators ]

seperators = [

	'{', '}', '(', ')', '[', ']', '.', ',', ';'
]

unary_operators = [

	'-', '!',
	'~' # for compatability 
]

binary_operators = [

	'+', '-', '*', '/', '%', '>>', '<<',
	'<', '>', '==', '>=', '<=',
	'&', '|', '^',
	'=' # for compatability
]

types = [
	
	# Standard
	'int',
	'char',
	'boolean',
]



# Grammar ==================================================================================================

'''
 ? -> apeears 0 or 1 times
 * -> appears 0+ times
'''

'''
	Ignores spaces, newlines, and comments

	Comments:
	  -> // to end of line
	  -> /* everything inside */

'''

## stringConstant_

# r_string = ???

## integerConstant_

r_integer = '[0-9]+'

## className_ | variableName_ | subroutineName_ 

r_identifier = '[A-Za-z_][A-Za-z_0-9]*'


## class

( 'class' ) ( className_ ) ( '{' ) ( classVariableDeclerations_ )* ( subroutineDeclerations_ )* ( '}' )

	## classVariableDeclerations_

	( 'static' | 'field' ) ( type_ ) ( variableName_ ) (  ( ',' ) ( variableName_ )  )* ( ';' )

	## type_  -> see types[]
	
	( 'int' | 'char' | 'boolean' | className_ )

	## subroutineDeclerations_

	( 'constructor' | 'method' | 'function' ) ( 'void' | type_ ) ( subroutineName_ ) ( '(' ) ( parameterList_ ) ( ')' ) ( subroutineBody_ )

	## parameterList_

	(  (  ( type_ ) ( variableName_ )  ) (  ( ',' ) ( type_ ) ( variableName_ )  )*  )?

	## subroutineBody_

	( '{' ) ( variableDeclerations_ )* ( statements_ ) ( '}' )

	## variableDeclerations_

	( 'var' ) ( type_ ) ( variableName ) (  ( ',' ) ( variableName )  )* ( ';' )

	## statements_

	( statement_ )*

	## statement_

	( letStatement_ | ifStatement_ | whileStatement_ | doStatement_ | returnStatement_ )*

	## letStatement_

	( 'let' ) ( variableName_ ) (  ( '[' ) ( expression_ ) ( ']' )  )? ( '=' ) ( expression_ ) ( ';' )

	## ifStatement_

	( 'if' ) ( '(' ) ( expression_ ) ( ')' ) ( '{' ) ( statements_ ) ( '}' ) (  ( 'else' ) ( '{' ) ( statements_ ) ( '}' )  )?

	## whileStatement_

	( 'while' ) ( '(' ) ( expression_ ) ( ')' ) ( '{' ) ( statements_ ) ( '}' )

	## doStatement_

	( 'do' ) ( subroutineCall_ ) ( ';' )

	## returnStatement_

	( 'return' ) ( expression_ )? ( ';' )

	## expression_

	( term_ ) (  ( binaryOp_ ) ( term_ )  )*

	## term_

	( integerConstant_ | stringConstant_ | keywordConstant_ | subroutineCall_ | variableName_ |
	  (  ( variableName_ ) ( '[' ) ( expression_ ) ( ']' )  ) |
	  (  ( '(' ) ( expression_ ) ( ')' )                    ) |
	  (  ( unaryOp_ ) ( term_ )                             )

	## subroutineCall_

	(  ( className_ | variableName_ ) ( '.' )  )? ( subroutineName ) ( '(' ) ( expressionList_ )? ( ')' )

	## expressionList_

	(  ( expression_ ) (  ( ',' ) ( expression_ )  )*  )?


	## binaryOp_  -> see binary_operators[]

	( '+' | '-' | '*' | '/' | '%' ... )

	## unaryOp_  -> see unary_operators[]

	( '-' | '!' | '~' )

	# keywordConstant_

	( 'true' | 'false' | 'null' | 'this' )



'''
	class
		classVariableDeclerations_
		subroutineDeclerations_
			parameterList_
			variableDeclerations_
			statements_
				do
				let
				while
				if
				return
'''

##################

r_className = '''

	class    # find the kwd class
	\s+      # followed by one or more spaces
	(\w+)    # capture subsequent sequence of alphanumeric and/or underscore characters

'''




'''
	# Class scope variables (static, field)

	Name | Type | Segment | idx


	# Subroutine scope variables (arg, local)
	
	Name | Type | Segment | idx

'''




parseStatement()
parseWhileStatement()
parseIfStatement()
parseStatementSequence()
parseExpression()
