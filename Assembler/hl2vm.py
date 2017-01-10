keywords = [

	'class',
	'constructor',
	'method',
	'this',
	'field',
	'static',
	
	'function',
	'var',
	'let',
	'do',
	'if',
	'else',
	'while',
	'return',

	'int',
	'char',
	'boolean',
	'void',
	
	'true',
	'false',
	'null',
]

seperator_symbols = [

	'{', '}', '(', ')', '[', ']', '.', ',', ';'
]

operator_symbols = {

	'unary'  : [ '-', '~' ],
	'binary' : [ 

		'+', '-', '*', '/', '%',
	    '&', '|', '>>', '<<', '^',
	    '<', '>', '==', '>=', '<=',
	]
}

types = [
	
	# Standard
	'int',
	'char',
	'boolean',

	# Class instances, see classNames
]

'''
classNames = [
	
	# Standard Libraries
	'String',
	'Math',
	'Array',
	'Output',
	'Screen',
	'Keyboard',
	'Memory',
	'Sys',

	# Custom Libraries
]
'''


'''
 ? -> apeears 0 or 1 times
 * -> appears 0+ times

'''

# className | variableName | subroutineName 
# -> sequence of letters/digits/underscore not starting with a digit

( 'class' ) ( className ) ( '{' ) ( variableDeclerations_ )* ( subroutineDeclerations_ )* ( '}' )

	# variableDeclerations_

	( 'static' | 'field' ) ( type_ ) ( variableName ) ( ( ',' ) ( variableName ) )* ( ';' )

	# type_
	# -> see types[] and classNames[]

	# subroutineDeclerations_

	( 'constructor' | 'method' | 'function' ) ( 'void' | type_ ) ( subroutineName ) ( '(' ) ( parameterList_ ) ( ')' ) ( subroutineBody_ )

	# parameterList_

	( ( type_ ) ( variableName ) ( ( ',' ) ( type_ ) ( variableName ) )* )?

	# subroutineBody_

	( '{' ) ( variableDeclerations2_ )* ( statements_ ) ( '}' )

	# variableDeclerations2_

	( 'var' ) ( type_ ) ( variableName ) ( ( ',' ) ( variableName ) )* ( ';' )

	# statements_

	( letStatement_ | ifStatement_ | whileStatement_ | doStatement_ | returnStatement_ )*

	# letStatement_

	( 'let' ) ( variableName ) ( ( '[' ) ( expression_ ) ( ']' ) )? ( '=' ) ( expression_ ) ( ';' )

	# ifStatement_

	( 'if' ) ( '(' ) ( expression_ ) ( ')' ) ( '{' ) ( statements_ ) ( '}' ) 
	                            ( ( 'else' ) ( '{' ) ( statements_ ) ( '}' ) )?

	# whileStatement_

	( 'while' ) ( '(' ) ( expression_ ) ( ')' ) ( '{' ) ( statements_ ) ( '}' )

	# doStatement_

	( 'do' ) ( subroutineCall_ ) ( ';' )

	# returnStatement_

	( 'return' ) ( expression_ )? ( ';' )

	# expression_

	( term_ ) ( ( binaryOp_ ) ( term_ ) )*

	# binaryOp_
	# -> see operator_symbols.binary[]

	# term_

	integerConstant_ | stringConstant_ | keywordConstant_ | 
	 unaryOp_ | subroutineCall_ |
	 ( ( '(' ) ( expression_) ( ')') ) |
	 ( ( variableName ) ( ( '[' ) ( expression_ ) ( ']' ) )? ) |

	# integerConstant_
	# -> 0..32767

	# stringConstant_
	# -> unicode sequencec enclosed in double (or single?) quotes.

	# keywordConstant_

	( 'true' | 'false' | 'null' | 'this' )

	# unaryOp_
	# -> see operator_symbols.unary[]

	# subroutineCall_

	( ( className | variableName ) ( '.' ) )? ( subroutineName ) ( '(' ) ( expressionList_ )? ( ')' )

	# expressionList_

	( expression_ ) ( ( ',' ) ( expression_ ) )*


'''
	class
		var decleration
		subroutine
			parameter list
			var decleration
			statements
				do
				let
				while
				if
				return
					expression
						term

'''

##################

# r_identifier = ...

r_className = '''

	class    # find the kwd class
	\s+      # followed by one or more spaces
	(\w+)    # capture subsequent sequence of alphanumeric and/or underscore characters

'''


####################

grammar_js = [

	( 'js', [ 'element', 'js' ] ),
	( 'js', [ ''              ] ),

	( 'element', [ 'function', 'identifier', '(', 'optParams', ')', 'compoundStmt' ] ),
	( 'element', [ 'stmt',     ';'                                                 ] ),

	( 'optParams', [ 'params' ] ),
	( 'optParams', [ ''       ] ),

	( 'params', [ 'identifier', ',', 'params' ] ),
	( 'params', [ 'identifier'                ] ),

	( 'optArgs', [ 'args' ] ),
	( 'optArgs', [ ''     ] ),

	( 'args', [ 'exp', ',', 'args' ] ),
	( 'args', [ 'exp'              ] ),

	( 'stmt', [ 'identifier', '=',   'exp'                                  ] ),
	( 'stmt', [ 'return',     'exp'                                         ] ),
	( 'stmt', [ 'if',         'exp', 'compoundStmt'                         ] ),
	( 'stmt', [ 'if',         'exp', 'compoundStmt', 'else', 'compoundStmt' ] ),

	( 'compoundStmt', [ '{', 'stmts', '}' ] ), 

	( 'stmts', [ 'stmt', ';', 'stmts' ] ),
	( 'stmts', [ ''                   ] ),

	( 'exp', [ 'identifier', '(',   'optArgs', ')' ] ),  
	( 'exp', [ '(',          'exp', ')'            ] ),
	( 'exp', [ 'exp',        '+',   'exp'          ] ),
	( 'exp', [ 'exp',        '-',   'exp'          ] ),
	( 'exp', [ 'exp',        '*',   'exp'          ] ),
	( 'exp', [ 'exp',        '/',   'exp'          ] ),
	( 'exp', [ 'exp',        '<',   'exp'          ] ),
	( 'exp', [ 'exp',        '>',   'exp'          ] ),
	( 'exp', [ 'exp',        '<=',  'exp'          ] ),
	( 'exp', [ 'exp',        '>=',  'exp'          ] ),
	( 'exp', [ 'exp',        '==',  'exp'          ] ),
	( 'exp', [ 'exp',        '!=',  'exp'          ] ),
	( 'exp', [ 'exp',        '&&',  'exp'          ] ),
	( 'exp', [ 'exp',        '||',  'exp'          ] ),
	( 'exp', [ 'number'                            ] ),
	( 'exp', [ 'string'                            ] ),
	( 'exp', [ 'true'                              ] ),
	( 'exp', [ 'false'                             ] ),

]


'''
 ? -> apeears 0 or 1 times
 * -> appears 0+ times

'''

# className | variableName | subroutineName 
# -> sequence of letters/digits/underscore not starting with a digit

( 'class' ) ( className ) ( '{' ) ( variableDeclerations_ )* ( subroutineDeclerations_ )* ( '}' )

	# variableDeclerations_

	( 'static' | 'field' ) ( type_ ) ( variableName ) ( ( ',' ) ( variableName ) )* ( ';' )

	# type_
	# -> see types[] and classNames[]

	# subroutineDeclerations_

	( 'constructor' | 'method' | 'function' ) ( 'void' | type_ ) ( subroutineName ) ( '(' ) ( parameterList_ ) ( ')' ) ( subroutineBody_ )

	# parameterList_

	( ( type_ ) ( variableName ) ( ( ',' ) ( type_ ) ( variableName ) )* )?

	# subroutineBody_

	( '{' ) ( variableDeclerations2_ )* ( statements_ ) ( '}' )

	# variableDeclerations2_

	( 'var' ) ( type_ ) ( variableName ) ( ( ',' ) ( variableName ) )* ( ';' )

	# statements_

	( letStatement_ | ifStatement_ | whileStatement_ | doStatement_ | returnStatement_ )*

	# letStatement_

	( 'let' ) ( variableName ) ( ( '[' ) ( expression_ ) ( ']' ) )? ( '=' ) ( expression_ ) ( ';' )

	# ifStatement_

	( 'if' ) ( '(' ) ( expression_ ) ( ')' ) ( '{' ) ( statements_ ) ( '}' ) 
	                            ( ( 'else' ) ( '{' ) ( statements_ ) ( '}' ) )?

	# whileStatement_

	( 'while' ) ( '(' ) ( expression_ ) ( ')' ) ( '{' ) ( statements_ ) ( '}' )

	# doStatement_

	( 'do' ) ( subroutineCall_ ) ( ';' )

	# returnStatement_

	( 'return' ) ( expression_ )? ( ';' )

	# expression_

	( term_ ) ( ( binaryOp_ ) ( term_ ) )*

	# binaryOp_
	# -> see operator_symbols.binary[]

	# term_

	integerConstant_ | stringConstant_ | keywordConstant_ | 
	 unaryOp_ | subroutineCall_ |
	 ( ( '(' ) ( expression_) ( ')') ) |
	 ( ( variableName ) ( ( '[' ) ( expression_ ) ( ']' ) )? ) |

	# integerConstant_
	# -> 0..32767

	# stringConstant_
	# -> unicode sequencec enclosed in double (or single?) quotes.

	# keywordConstant_

	( 'true' | 'false' | 'null' | 'this' )

	# unaryOp_
	# -> see operator_symbols.unary[]

	# subroutineCall_

	( ( className | variableName ) ( '.' ) )? ( subroutineName ) ( '(' ) ( expressionList_ )? ( ')' )

	# expressionList_

	( expression_ ) ( ( ',' ) ( expression_ ) )*







'''

	Ignores spaces, newlines, and comments

	Comments:
	  -> // to end of line
	  -> /* everything inside */

'''

'''
	# Class scope variables (static, field)

	Name | Type | Segment | idx


	# Subroutine scope variables (arg, local)
	
	Name | Type | Segment | idx

'''



#########

className = ''

classVariables = {
	
	# 'name' : [ 'type', 'segment', 'index' ],
}

methodVaribles = {

	# 'name' : [ 'type', 'segment', 'index' ],
	# 'nArgs' : 0,
	# 'nVars' : 0,
}

def add_nArgs( methodVars ): 

	count = 0

	for var in methodVars:
		if methodVars[var][1] == 'argument':
			count += 1

	methodVars['nArgs'] = count

def add_nVars( method ): pass



#########

def writePush( segment, idx ): pass

def writePop( segment, idx ): pass

def writeArithmetic( op ): pass  # add, sub, or etc.

def writeLabel( label ): pass

def writeGoto( label ): pass

def writeIfGoto( label ): pass

def writeCall( name, nArgs ): pass

def writeFunction( name, nLocals ): pass

def writeReturn(): pass
