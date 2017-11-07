# ========================================================================================
#  
#  Description:
#     Compiles Hack HL (high level) code to Hack VM (virtual machine) code
#  
#  Attribution:
#     Code by www.jk-quantized.com
#  
#     Design is based on:
#  
#        Mihai Bazon's superb interpreter and compiler design tutorial:
#         http://lisperator.net/pltut/
#         http://lisperator.net/s/lambda/lambda-eval1.js
#  
#        Lecture notes from the Nand To Tetris course
#         www.nand2tetris.org
#  
#     Extensions to the Hack HL grammar:
#  
#        Some are my own and others are inspired by @cadet1620's posts as noted within the code.
#        http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/template/NamlServlet.jtp?macro=user_nodes&user=266121
#  
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
#  
# ========================================================================================


# === Imports ===================================================

# Built ins
import json
import os
import re

# Hack computer
import Components._0__globalConstants as GC


# === Settings ==================================================

USE_COMPATIBLE = None  # Use VM instructions that are compatible with the official TECS VMEmulator
                       # Value is set by call to 'genVMFiles'


# === Helpers ===================================================

def prettyPrint( d ):
	# stackoverflow.com/a/3314411
	print( json.dumps( d, sort_keys = True, indent = 4 ) )

largestInt = 2 ** ( GC.N_BITS - 1 ) - 1  # two's complement


# === Hack Lexicon ===============================================

Hack_lexicon = {
	
	'comparisonOps' : [ '=', '==', '>', '<', '>=', '<=', '!=' ],

	'unaryOps' : [ '~', '!', '-' ],

	'binaryOps' : [

		'+', '-', '*', '/', '%',
		'>>', '<<',
		'&', '|', '^',
	],

	'assignmentOps' : [

		'=',
		'+=', '-=', '*=', '/=', '%=',
		'>>=', '<<=',
		'&=', '|=', '^=',
	],

	'dataTypes' : [ 'int', 'char', 'boolean' ],

	'statementTypes' : [ 'let', 'do', 'if', 'else', 'while', 'return', 'for', 'break', 'continue' ],

	'functionTypes' : [ 'constructor', 'method', 'function' ],

	'variableTypes' : [ 'field', 'static', 'var' ],
	
	'other' : [ 'void', 'class', 'const', 'include' ],
	
	'keywordConstants' : [ 'true', 'false', 'null', 'this' ],

	'memoryPointers' : [ '_SCREEN','_KEYBOARD', '_MOUSEX', '_MOUSEY', '_IOBANK1', '_IOBANK2' ],

	'punctuation' : '.,;(){}[]',
}

Hack_lexicon[ 'keywords' ] = set (

	Hack_lexicon[ 'statementTypes'   ] + 
	Hack_lexicon[ 'functionTypes'    ] + 
	Hack_lexicon[ 'variableTypes'    ] + 
	Hack_lexicon[ 'other'            ] + 
	Hack_lexicon[ 'keywordConstants' ] + 
	Hack_lexicon[ 'memoryPointers'   ]
)

Hack_lexicon[ 'ops' ] = set (

	Hack_lexicon[ 'comparisonOps' ] +
	Hack_lexicon[ 'unaryOps'      ] +
	Hack_lexicon[ 'binaryOps'     ] +
	Hack_lexicon[ 'assignmentOps' ]
)



# === Input Stream ===============================================

class InputStream():

	def __init__( self, input_ ):
	
		self.pos = 0
		self.line = 1
		self.col = 0

		self.input = input_
		self.inputEnd = len( input_ )

	def next( self ):

		ch = self.input[ self.pos ]

		self.pos += 1

		if ch == '\n':

			self.line += 1
			self.col = 0

		else:

			self.col += 1

		return ch

	def peek( self ):

		return self.input[ self.pos ]

	def peekpeek( self ):

		return self.input[ self.pos + 1 ]

	# def peekpeekpeek( self ):

	# 	return self.input[ self.pos + 2 ]

	# def peekpeekpeekpeek( self ):

	# 	return self.input[ self.pos + 3 ]

	def eof( self ):

		return self.pos >= self.inputEnd

	def croak( self, msg ):

		raise Exception( '{} (at line {}, column {})'.format( msg, self.line, self.col ) )


# Test -----------------------------------------

def testInputStream():

	inputStream = InputStream( sampleCode )
	print( inputStream.next() )
	print( inputStream.next() )
	print( inputStream.next() )
	print( inputStream.next() )
	print( inputStream.next() )
	print( inputStream.next() )
	print( '--' )
	print( inputStream.peek() )
	print( inputStream.input[ inputStream.pos + 1 ] )
	print( inputStream.peekpeek() )
	print( inputStream.input[ inputStream.pos + 2 ] )
	print( inputStream.input[ inputStream.pos + 3 ] )
	print( inputStream.input[ inputStream.pos + 4 ] )
	print( '--' )
	print( inputStream.next() )
	print( inputStream.next() )
	# print( inputStream.croak('oive') )
	print( inputStream.eof() )
	inputStream.pos = len( sampleCode )
	print( inputStream.eof() )

# testInputStream()



# === Tokenizer ==================================================

'''
	{ type : 'num',  value : 5        }  # numbers
	{ type : 'str',  value : 'Hello'  }  # strings
	{ type : 'char', value : 'B'      }  # ASCII char
	{ type : 'char', value : 0xff     }  # hex
	{ type : 'char', value : 0b101    }  # bin
	{ type : 'punc', value : '('      }  # punctuation ( parens, comma, semicolon etc. )
	{ type : 'kw',   value : 'lambda' }  # keywords
	{ type : 'op',   value : '!='     }  # operators
	{ type : 'dtyp', value : 'char'   }  # data types
	{ type : 'id',   value : 'a'      }  # identifiers
'''

'''
	- skip whitespace
	- if eof,            return None
	- if '//',           skip comment and continue after encounter '\n'
	- if '/*',           skip comment and continue after encounter '*/'
	- if doublequote,    read a string
	- if singlequote,    read a char
	- if 0 lookahead,
	-    if digit,       read a number
	-    if x,           read a hex
	-    if b,           read a bin
	- if non-zero digit, read a number
	- if letter,         read an identifier or keyword
	- if punctuation,    return punctuation token
	- if oper character, return operator token
	- if none of above,  raise error
'''


class TokenStream():

	def __init__( self, input_ ):

		self.input = input_

		self.current   = None
		self.previous  = None
		self.previous2 = None
		self.previous3 = None

		self.keywords = Hack_lexicon[ 'keywords' ]

		self.datatypes = Hack_lexicon[ 'dataTypes' ]

		self.digits = '0123456789'

		self.hex = self.digits + 'abcdefABCDEF'

		self.bin = '01'

		self.idStart = '_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

		self.ops = Hack_lexicon[ 'ops' ]

		self.puncs = Hack_lexicon[ 'punctuation' ]

		self.whitespace = ' \t\n\r'


	# -----------------------------------

	def is_keyword( self, x ):

		return x in self.keywords

	def is_datatype( self, x ):

		return x in self.datatypes

	def is_digit( self, ch ):

		return ch in self.digits

	def is_hex( self, ch ):

		return ch in self.hex

	def is_bin( self, ch ):

		return ch in self.bin

	def is_idStart( self, ch ):

		return ch in self.idStart

	def is_id( self, ch ):

		return self.is_idStart( ch ) or self.is_digit( ch )  # allow digits in id as long as not start char

	def is_op( self, ch ):

		return ch in self.ops

	def is_punc( self, ch ):

		return ch in self.puncs

	def is_whitespace( self, ch ):

		return ch in self.whitespace


	# -----------------------------------

	def read_number( self ):

		def is_valid_number( ch ):

			# No support for decimals...

			return self.is_digit( ch )

		number = self.read_while( is_valid_number )

		return {

			'type'  : 'num',
			'value' : number
		}

	def read_hex( self ):

		def is_valid_hex( ch ):

			return self.is_hex( ch )

		hex_ = ''
		hex_ += self.input.next()  # 0
		hex_ += self.input.next()  # X

		hex_ += self.read_while( is_valid_hex )

		return {

			'type'  : 'hex',
			'value' : hex_
		}

	def read_bin( self ):

		def is_valid_bin( ch ):

			return self.is_bin( ch )

		bin_ = ''
		bin_ += self.input.next()  # 0
		bin_ += self.input.next()  # B

		bin_ += self.read_while( is_valid_bin )

		return {

			'type'  : 'bin',
			'value' : bin_
		}

	def read_id( self ):

		id_ = self.read_while( self.is_id )

		if self.is_keyword( id_ ):

			typ = 'kw'

		elif self.is_datatype( id_ ):

			typ = 'dtyp'

		else:

			typ = 'id'

		return {

			'type'  : typ,
			'value' : id_
		}

	def read_string( self ):

		# No support for escaped quotes '\"'

		return {

			'type'  : 'str',
			'value' : self.read_wrapped( '"' )
		}

	def read_char( self ):

		self.input.next()  # skip start quote

		ch = self.input.next()

		if self.input.peek() == "'":

			self.input.next()  # skip closing quote

		else:

			self.croak( "Error: Expected closing quote when reading char" )

		return {

			'type'  : 'char',
			'value' : ch
		}

	def skip_singlelineComment( self ):

		def yetToReachCommentEnd( ch ):

			return ch != '\n'

		self.input.next()  # skip the '/' in comment start

		self.read_while( yetToReachCommentEnd )

		self.input.next()  # skip the '\n' in comment end

	def skip_multilineComment( self ):

		def yetToReachCommentEnd( ch, next_ch ):

			return not ( ch == '*' and next_ch == '/' )

		self.input.next()  # skip the '/' in comment start
		
		self.read_whilewhile( yetToReachCommentEnd )

		self.input.next()  # skip the '*' in comment end
		self.input.next()  # skip the '/' in comment end


	# -----------------------------------

	def read_next( self ):

		self.read_while( self.is_whitespace )

		if self.input.eof():

			return None

		ch = self.input.peek()

		if ch == '/':

			# Peek if next next char signifies comment start
			next_ch = self.input.peekpeek()

			if next_ch == '/':

				# Line comment

				self.skip_singlelineComment()

				return self.read_next()
			
			elif next_ch == '*':

				# Multiline comment

				self.skip_multilineComment()

				return self.read_next()


		if ch == '"':

			return self.read_string()

		elif ch == "'":

			return self.read_char()

		elif ch == '0':

			# Peek next next char
			next_ch = self.input.peekpeek()

			if next_ch == 'x' or next_ch == 'X':

				return self.read_hex()

			elif next_ch == 'b' or next_ch == 'B':

				return self.read_bin()

			else:

				return self.read_number()

		elif self.is_digit( ch ):

			return self.read_number()

		elif self.is_idStart( ch ):

			return self.read_id()

		elif self.is_punc( ch ):

			return {

				'type'  : 'punc',
				'value' : self.input.next()
			}

		elif self.is_op( ch ):

			return {

				'type'  : 'op',
				'value' : self.read_while( self.is_op )
			}

		else:

			self.croak( "Can't handle character: " + ch )

	
	# -----------------------------------

	def read_while( self, predicate ):

		s = ''

		while not self.input.eof() and predicate( self.input.peek() ):

			s += self.input.next()

		return s

	def read_whilewhile( self, predicate ):

		s = ''

		while not self.input.eof() and predicate( self.input.peek(), self.input.peekpeek() ):

			s += self.input.next()

		return s

	def read_wrapped( self, end ):

		s = ''

		self.input.next()  # skip start char

		while not self.input.eof():

			ch  = self.input.next()

			if ch == end:

				break  # seen end char, stop gathering

			else:

				s += ch   # gather chars in between

		return s


	# -----------------------------------

	def peek( self ):

		if self.previous3:    # previously peeked4

			return self.previous3

		elif self.previous2:  # previously peeked3

			return self.previous2

		elif self.previous:   # previously peekedpeeked

			return self.previous

		elif self.current:    # previously peeked

			return self.current

		else:                 # haven't previously peeked

			self.current = self.read_next()

			return self.current

	def peekpeek( self ):

		if self.previous3:    # previously peeked4

			return self.previous3

		elif self.previous2:  # previously peeked3

			return self.previous2		

		if self.previous:     # previously peekedpeeked

			return self.current

		elif self.current:    # previously peeked

			self.previous = self.current
			self.current  = self.read_next()

			return self.current

		else:                 # haven't previously peeked

			self.previous = self.read_next()
			self.current  = self.read_next()

			return self.current

	def peek3( self ):

		if self.previous3:    # previously peeked4

			return self.previous3

		elif self.previous2:  # previously peeked3

			return self.current

		elif self.previous:   # previously peekedpeeked

			self.previous2 = self.previous
			self.previous  = self.current
			self.current   = self.read_next()

			return self.current

		elif self.current:    # previously peeked

			self.previous2 = self.current
			self.previous  = self.read_next()
			self.current   = self.read_next()

			return self.current

		else:                 # haven't previously peeked

			self.previous2 = self.read_next()
			self.previous  = self.read_next()
			self.current   = self.read_next()

			return self.current

	def peek4( self ):

		if self.previous3:    # previously peeked4

			return self.current

		elif self.previous2:  # previously peeked3

			self.previous3 = self.previous2
			self.previous2 = self.previous
			self.previous  = self.current
			self.current   = self.read_next()

			return self.current

		elif self.previous:   # previously peekedpeeked

			self.previous3 = self.previous
			self.previous2 = self.current
			self.previous  = self.read_next()
			self.current   = self.read_next()

			return self.current

		elif self.current:    # previously peeked

			self.previous3 = self.current
			self.previous2 = self.read_next()
			self.previous  = self.read_next()
			self.current   = self.read_next()

			return self.current

		else:                 # haven't previously peeked

			self.previous3 = self.read_next()
			self.previous2 = self.read_next()
			self.previous  = self.read_next()
			self.current   = self.read_next()

			return self.current

	def next( self ):

		'''
			Doesn't always call self.read_next() as might have peeked before
			in which case self.read_next() would have already been called and
			the stream advanced
		'''

		if self.previous3:

			tok = self.previous3
			self.previous3 = None

			# print( ">>", tok )
			return tok

		elif self.previous2:

			tok = self.previous2
			self.previous2 = None

			# print( ">>", tok )
			return tok

		elif self.previous:

			tok = self.previous
			self.previous = None

			# print( ">>", tok )
			return tok

		elif self.current:

			tok = self.current
			self.current = None

			# print( ">>", tok )
			return tok

		else:

			return self.read_next()
			
			# tok = self.read_next()
			# print( ">>", tok )
			# return tok

	def eof( self ):

		return self.peek() == None

	def croak( self, msg ):

		# print( "Derp Derp\n\t" + msg )

		self.input.croak( msg )


# Test -----------------------------------------

def testTokenizer():

	inputS = InputStream( sampleCode )
	tokenS = TokenStream( inputS )

	# print( inputS.peek() )
	# print( tokenS.input.peek() )

	while True:

		out = tokenS.next()

		if out:

			# print( out )
			print( '{:<6}'.format( out['type'] ), out['value'] )

		else: break

# testTokenizer()



# === Parser ==================================================

'''
	Parser will build a structure that faithfully represents
	semantics of program

	classDeclaration -> {

		type     : 'classDecleration'
		name     : STRING 
		constDec : [
			{
				var_type : STRING
				name     : STRING
				d_type   : STRING
				value    : expTerm
			}
		]
		varDec : [
			{
				var_type : STRING
				names    : [ STRING ]
				d_type   : STRING
			}
		]
		subDec : [
			{
				name     : STRING
				fx_type  : STRING
				ret_type : STRING
				params : [					
					{
						name   : STRING
						d_type : STRING
					}
				]
				constDec : [
					{
						var_type : STRING
						name     : STRING
						d_type   : STRING
						value    : expTerm
					}
				]
				varDec : [
					{
						var_type : STRING
						names    : [ STRING ]
						d_type   : STRING
					}
				]  
				statements : [
					{
						type : 'subroutineCall'  # doStatement
						name : STRING
						args : [ exp ]
					},
					{
						type         : 'assignment'  # letStatement
						assignmentOp : assignmentOp
						left         : 
						{
							type   : 'identifier'
							name   : STRING
							arrIdx : exp
						}
							|
						{							
							type : 'identifier'
							name : STRING
						}
						right : exp
					},
					{
						type : 'whileStatement'
						cond : exp
						body : [ statements ]
					},
					{
						type : 'ifStatement'
						cond : exp
						then : [ statements ]
						else : None | [ statements ]
					},
					{
						type  : 'returnStatement'
						value : 0 | exp
					},
					{
						type   : 'forStatement'
						init   : assignment
						cond   : exp
						update : assignment
						body   : [ statements ]
					},
					{
						type : 'breakStatement'
					},
					{
						type : 'continueStatement'
					}
				]
			}
		]
	}

	exp ->
		None |
		expTerm |
		[
			expTerm
			{
				type  : 'binaryOp'
				value : STRING
			}
			expTerm
			...
			{
				type  : 'binaryOp'
				value : STRING
			}
			expTerm
			...
		]

	expTerm -> 
		{
			type  : 'integerConstant'
			value : INTEGER
		}
			|
		{
			type  : 'stringConstant'
			value : STRING
		}
			|
		{
			type  : 'keywordConstant'
			value : STRING
		}
			|
		{
			type  : 'memoryPointer'
			value : STRING
		}
			|
		{
			type   : 'identifier'
			name   : STRING
			arrIdx : exp
		}
			|
		{
			type : 'identifier'
			name : STRING
		}
			|
		{
			type : 'subroutineCall'
			name : STRING
			args : [ exp ]	
		}
			|
		{
			type    : 'unaryOp'
			op      : STRING
			operand : exp
		}

'''

'''
	-- Hack HL (Jack) Grammar ----------------------------------------------------------------

	class           -> 'class' className '{' constDec* classVarDec* subroutineDec* '}'

	classVarDec     -> ( 'static' | 'field' ) type varName ( ',' varName )* ';'

	type            -> 'int' | 'char' | 'boolean' | className

	subroutineDec   -> ( 'constructor' | 'function' | 'method' ) ( 'void' | type ) subroutineName '(' parameterList ')' subroutineBody

	parameterList   -> ( type varName ( ',' type varName )* )?

	subroutineBody  -> '{' constDec* varDec* statements '}'

	varDec          -> 'var' type varName ( ',' varName )* ';'

	className       -> identifier
	subroutineName  -> identifier
	varName         -> identifier

	statements      -> statement*

	statement       -> letStatement | ifStatement | whileStatement | doStatement | returnStatement | whileStatement | continueStatement | breakStatement

	letStatement    -> 'let'? assignment ';'

	ifStatement     -> 'if' '(' expression ')' statementBlock ( 'else' statementBlock )?

	whileStatement  -> 'while' '(' expression ')' statementBlock

	doStatement     -> 'do'? subroutineCall ';'

	returnStatement -> 'return' expression? ';'

	expression      -> expressionTerm ( binaryOp expressionTerm )*

	expressionTerm  -> integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp expressionTerm

	subroutineCall  -> ( ( className | varName ) '.' )? subroutineName '(' expressionList ')'

	expressionList  -> ( expression ( ',' expression )* )?

	binaryOp        -> '+'|'-'|...
	unaryOp         -> '~'|'-'|...

	keywordConstant -> 'true' | 'false' | 'null' | 'this'

	integerConstant -> number in range 0..32767 | hexConstant | binConstant | charConstant

	stringConstant  -> sequence wrapped in double quotes

	identifier      -> sequence of letters, digits, and underscore not starting with a digit


	-- Stuff I added -------------------------------------------------------------------------

	assignment        -> varName ( '[' expression ']' )? assignmentOp expression

	assignmentOp      -> '=' | +=' | '-=' | '/=' | ...

	forStatement      -> 'for' '(' assignment ';' expression ';' assignment ')' statementBlock
	
	include           -> 'include' stringConstant

	-- Inspired by @cadet1620 ----

	continueStatement -> 'continue' ';'

	breakStatement    -> 'break' ';'
	
	charConstant      -> single Ascii character wrapped in single quotes

	hexConstant       -> ( '0x' | '0X' ) ( 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F )+

	binConstant       -> ( '0b' | '0B' ) ( 0 | 1 )+

	constDec          -> 'const' 'int' varName '=' '-'? integerConstant ';'

	statementBlock    -> statement | ( '{' statements '}' )

'''


class Parser():

	def __init__( self, input_ ):

		self.input = input_

		self.keywordConstants = Hack_lexicon[ 'keywordConstants' ]

		self.memoryPointers = Hack_lexicon[ 'memoryPointers' ]

		self.unaryOps = Hack_lexicon[ 'unaryOps' ]

		self.assignmentOps = Hack_lexicon[ 'assignmentOps' ]

		self.includes = []

	def parse( self ):

		return self.parse_toplevel()

	def croak( self, msg ):

		self.input.croak( msg )


	# -----------------------------------

	def parse_toplevel( self ):

		# -- Retrieve included files and directories
		self.retrieveIncludes()

		# -- Each file contains only one class
		return self.parse_classDeclaration()

		# -- Each file can contain multiple classes
		# output = []

		# while not self.input.eof():

		# 	output.append( self.parse_classDeclaration() )

		# return output


	# -----------------------------------

	def is_punc( self, punc = None ):

		tok = self.input.peek()

		return tok and tok[ 'type' ] == 'punc' and ( punc == None or tok[ 'value' ] == punc )

	def is_kw( self, kw = None ):

		tok = self.input.peek()

		return tok and tok[ 'type' ] == 'kw' and ( kw == None or tok[ 'value' ] == kw )

	def is_op( self, op = None ):

		tok = self.input.peek()

		return tok and tok[ 'type' ] == 'op' and ( op == None or tok[ 'value' ] == op )

	def is_d_type( self, d_type = None ):

		tok = self.input.peek()

		return tok and tok[ 'type' ] == 'dtyp' and ( d_type == None or tok[ 'value' ] == d_type )
	
	def is_id( self, id_ = None ):

		tok = self.input.peek()

		return tok and tok[ 'type' ] == 'id' and ( id_ == None or tok[ 'value' ] == id_ )

	def is_str( self, str_ = None ):

		tok = self.input.peek()

		return tok and tok[ 'type' ] == 'str' and ( str_ == None or tok[ 'value' ] == str_ )

	def skip_punc( self, punc ):

		if self.is_punc( punc ):

			self.input.next()

		else:

			self.croak( 'Error: Expecting punctuation. Instead got {}'.format( punc ) )

	def skip_kw( self, kw ):

		if self.is_kw( kw ):

			self.input.next()

		else:

			self.croak( 'Error: Expecting keyword. Instead got {}'.format( kw ) )

	def skip_op( self, op ):

		if self.is_op( op ):

			self.input.next()

		else:

			self.croak( 'Error: Expecting operator. Instead got {}'.format( op ) )

	def read_d_type( self, callerName ):

		if self.is_d_type() or self.is_id():

			return self.input.next()[ 'value' ]

		else:

			self.croak( 'Error: {} expects data type. Instead got {}'.format( callerName, self.input.peek() ) )

	def read_id( self, callerName ):

		if self.is_id():

			return self.input.next()[ 'value' ]

		else:

			self.croak( 'Error: {} expects identifier. Instead got {}'.format( callerName, self.input.peek() ) )

	
	# -----------------------------------

	def parse_classDeclaration( self ):
		'''
			'class' className '{' classVarDec* subroutineDec* '}'
		'''

		self.input.next()  # 'class'

		name = self.read_id( 'classDeclaration' )

		self.skip_punc( '{' )

		constDec = self.parse_constDeclarations()

		varDec = self.parse_classVariableDeclarations()

		subDec = self.parse_subroutineDeclarations()

		self.skip_punc( '}' )

		return {

			'type'     : 'classDeclaration',
			'name'     : name,
			'constDec' : constDec,
			'varDec'   : varDec,
			'subDec'   : subDec,
		}

	def parse_constDeclarations( self ):

		def continueCondition( tok ):

			return tok[ 'value' ] == 'const'

		return self.parse_consecutive( continueCondition, self.parse_constDeclaration )

	def parse_constDeclaration( self ):
		'''
			'const' 'int' varName '=' '-'? integerConstant ';'
		'''

		self.skip_kw( 'const' )

		if self.is_d_type( 'int' ):

			self.input.next()

		else:

			self.croak( "Error: Expecting 'int' type in constant declaration. Instead got {}".format( self.input.peek() ) )

		name = self.read_id( 'constDeclaration' )

		self.skip_op( '=' )

		if self.is_op( '-' ):

			self.input.next()  # -

			value = {

				'type'    : 'unaryOp',
				'op'      : '-',
				'operand' : self.parse_integerConstant()
			}

		else:

			value = self.parse_integerConstant()

		self.skip_punc( ';' )

		return {

			'var_type' : 'const',
			'name'     : name,
			'd_type'   : 'int',
			'value'    : value

		}

	def parse_classVariableDeclarations( self ):

		def continueCondition( tok ):

			return tok[ 'value' ] == 'static' or tok[ 'value' ] == 'field'

		return self.parse_consecutive( continueCondition, self.parse_classVariableDeclaration )
	
	def parse_classVariableDeclaration( self ):
		'''
			( 'static' | 'field' ) type varName ( ',' varName )* ';'
		'''

		if self.is_kw( 'static' ):

			var_type = 'static'

			self.input.next()

		elif self.is_kw( 'field' ):

			var_type = 'field'
			
			self.input.next()

		else:

			self.croak( "Error: Expecting either 'static' or 'field' keyword in classVariableDeclaration" )

		d_type = self.read_d_type( 'classVariableDeclaration' )

		names = self.parse_delimitedList( None, ';', ',', self.read_id, 'classVariableDeclaration' )

		return {

			'var_type' : var_type,
			'names'    : names,
			'd_type'   : d_type
		}

	def parse_subroutineDeclarations( self ):

		def continueCondition( tok ):

			return tok[ 'value' ] == 'constructor' or tok[ 'value' ] == 'function' or tok[ 'value' ] == 'method'

		return self.parse_consecutive( continueCondition, self.parse_subroutineDeclaration )
		
	def parse_subroutineDeclaration( self ):
		'''
			( 'constructor' | 'function' | 'method' ) ( 'void' | type ) subroutineName '(' parameterList ')'
			'{' varDec* statements '}'
		'''

		fx_type = self.input.next()[ 'value' ]  # constructor, function, method

		ret_type = self.input.next()[ 'value' ]   # void, other

		name = self.read_id( 'subroutineDeclaration' )

		params = self.parse_delimitedList( '(', ')', ',', self.parse_parameter )

		self.skip_punc( '{' )

		constDec = self.parse_constDeclarations()

		varDec = self.parse_variableDeclarations()

		statements = self.parse_statements()

		self.skip_punc( '}' )

		return {

			'name'       : name,
			'fx_type'    : fx_type,
			'ret_type'   : ret_type,
			'params'     : params,
			'constDec'   : constDec,
			'varDec'     : varDec,
			'statements' : statements
		}

	def parse_parameter( self ):
		'''
			type varName
		'''

		d_type = self.read_d_type( 'parameter' )

		name = self.read_id( 'parameter' )

		return {

			'name'   : name,
			'd_type' : d_type,
		}

	def parse_variableDeclarations( self ):

		def continueCondition( tok ):

			return tok[ 'value' ] == 'var'

		return self.parse_consecutive( continueCondition, self.parse_variableDeclaration )
	
	def parse_variableDeclaration( self ):
		'''
			'var' type varName ( ',' varName )* ';'
		'''

		self.skip_kw( 'var' )

		d_type = self.read_d_type( 'variableDeclaration' )

		names = self.parse_delimitedList( None, ';', ',', self.read_id, 'variableDeclaration' )

		return {

			# 'type'     : 'variableDeclaration',
			'var_type' : 'var',
			'names'    : names,
			'd_type'   : d_type
		}

	def parse_statements( self ):

		def continueCondition( tok ):

			return (
				tok[ 'value' ] == 'let'   or tok[ 'value' ] == 'if'       or 
				tok[ 'value' ] == 'while' or tok[ 'value' ] == 'do'       or
				tok[ 'value' ] == 'for'   or tok[ 'value' ] == 'return'   or
				tok[ 'value' ] == 'break' or tok[ 'value' ] == 'continue' or
				tok[ 'type'  ] == 'id'
			)

		return self.parse_consecutive( continueCondition, self.parse_statement )

	def parse_statement( self ):

		if self.is_kw( 'do' ):

			return self.parse_doStatement()

		elif self.is_kw( 'let' ):

			return self.parse_letStatement()

		elif self.is_kw( 'while' ):

			return self.parse_whileStatement()

		elif self.is_kw( 'if' ):

			return self.parse_ifStatement()

		elif self.is_kw( 'for' ):

			return self.parse_forStatement()

		elif self.is_kw( 'return' ):

			return self.parse_returnStatement()		
		
		elif self.is_kw( 'break' ):

			return self.parse_breakStatement()

		elif self.is_kw( 'continue' ):

			return self.parse_continueStatement()

		elif self.is_id():
			'''
				assignment | subroutineCall ';'
			'''

			''' Assumptions
				 - only assignment and calls can begin with ids
				 - cannot assign class properties (static/fields) outside said class
				    ex. 'let p.x = 5' is invalid
				 - cannot store function pointers in arrays
				    ex. 'do cats[0]()' is invalid
			'''

			tok2 = self.input.peekpeek()[ 'value' ]

			if tok2 == '[' or tok2 in self.assignmentOps:

				ret = self.parse_assignment()

			elif tok2 == '(':

				ret = self.parse_subroutineCall()

			elif tok2 == '.':

				tok4 = self.input.peek4()[ 'value' ]

				if tok4 == '(':

					ret = self.parse_subroutineCall()

				else:

					raise Exception( 'Should never get here' )

			else:

				print( tok2 )

				raise Exception( 'Should never get here' )

			self.input.next()  # ;

			return ret
	
	def parse_doStatement( self ):
		'''
			'do' subroutineCall ';'
		'''

		self.input.next()  # do
		
		ret = self.parse_subroutineCall()
		
		self.skip_punc( ';' )

		return ret

	def parse_subroutineCall( self ):
		'''
			( ( className | varName ) '.' )? subroutineName '(' expressionList ')'
		'''

		name = self.read_id( 'subroutineCall' )

		if self.input.peek()[ 'value' ] == '.':

			self.input.next()  # .

			name += '.' + self.read_id( 'subroutineCall dot' )

		args = self.parse_delimitedList( '(', ')', ',', self.parse_expression )

		return {

			'type' : 'subroutineCall',
			'name' : name,
			'args' : args
		}

	def parse_assignment( self, returnType = None ):
		'''
			varName ( '[' expression ']' )? assignmentOp expression
		'''

		# -- Left
		left = self.read_id( 'assignment' )

		arrIdx = None

		if self.input.peek()[ 'value' ] == '[':

			arrIdx = self.parse_wrapped( '[', ']', self.parse_expression )

		# -- Op
		tok = self.input.peek()

		if tok[ 'type' ] == 'op' and tok[ 'value' ] in self.assignmentOps:

			op = self.input.next()[ 'value' ]

		else:

			self.croak( 'Error: Expecting an assignment operator. Instead got {}'.format( tok ) )

		# -- Right
		right = self.parse_expression()

		# -- Return
		ret = {

			'type'         : 'assignment',
			'assignmentOp' : op,
			'right'        : right,
			'left'         : {

				'type' : 'identifier',
				'name' : left
			},
		}


		if arrIdx :

			ret[ 'left' ][ 'arrIdx' ] = arrIdx

		return ret

	def parse_letStatement( self ):
		'''
			'let' assignment ';'
		'''

		self.input.next()  # let

		ret = self.parse_assignment()

		self.skip_punc( ';' )

		return ret

	def parse_statementBlock( self ):
		'''
			statement | ( '{' statements '}' )
		'''

		if self.is_punc( '{' ):

			return self.parse_wrapped( '{', '}', self.parse_statements )

		else:

			return self.parse_statement()

	def parse_whileStatement( self ):
		'''
			'while' '(' expression ')' statementBlock
		'''

		self.input.next()  # while

		cond = self.parse_wrapped( '(', ')', self.parse_expression )

		body = self.parse_statementBlock()

		return {

			'type' : 'whileStatement',
			'cond' : cond,
			'body' : body
		}

	def parse_ifStatement( self ):
		'''
			'if' '(' expression ')' statementBlock ( 'else' statementBlock )?
		'''

		self.input.next()  # if

		cond = self.parse_wrapped( '(', ')', self.parse_expression )

		then = self.parse_statementBlock()

		els  = None

		if self.is_kw( 'else' ):

			self.input.next()  # else

			els = self.parse_statementBlock()

		return {

			'type' : 'ifStatement',
			'cond' : cond,
			'then' : then,
			'else' : els
		}

	def parse_forStatement( self ):

		'''
			forStatement -> 'for' '(' assignment ';' expression ';' assignment ')' statementBlock
		'''

		self.input.next()  # for

		self.skip_punc( '(' )

		# -- Init --

		init = self.parse_assignment()

		self.skip_punc( ';' )
		
		# -- Cond --

		cond = self.parse_expression()

		self.skip_punc( ';' )

		# -- Update --

		update = self.parse_assignment()

		self.skip_punc( ')' )

		# -- Body --

		body = self.parse_statementBlock()
		
		return {

			'type'   : 'forStatement',
			'init'   : init,
			'cond'   : cond,
			'update' : update,
			'body'   : body,
		}

	def parse_returnStatement( self ):
		'''
			'return' expression? ';'
		'''

		self.input.next()  # return

		val = 0

		if not self.is_punc( ';' ):

			val = self.parse_expression()

		self.skip_punc( ';' )

		return {

			'type'  : 'returnStatement',
			'value' : val
		}

	def parse_breakStatement( self ):
		'''
			'break' ';'
		'''

		self.input.next()  # break

		self.skip_punc( ';' )

		return {

			'type' : 'breakStatement'
		}

	def parse_continueStatement( self ):
		'''
			'continue' ';'
		'''

		self.input.next()  # continue

		self.skip_punc( ';' )

		return {

			'type' : 'continueStatement'
		}

	def parse_expression( self ):
		'''
			expressionTerm ( binaryOp expressionTerm )*
		'''

		exps = []
		
		left = self.parse_expressionTerm()

		if not left:

			return None

		exps.append( left )

		while self.is_op():

			tok = self.input.peek()

			if ( tok[ 'value' ] in Hack_lexicon[ 'comparisonOps' ] or
			     tok[ 'value' ] in Hack_lexicon[ 'binaryOps' ] 
			):

				op = {

					'type'  : 'binaryOp',
					'value' : self.input.next()[ 'value' ]
				}
				
				right = self.parse_expressionTerm()

				exps.append( op )
				exps.append( right )

			else:

				self.croak( "Error: Unexpected op: " + tok[ 'value' ] )


		if len( exps ) == 1:

			return exps[0]

		else:

			return exps  # sequence of 1+ binary ops

	def parse_expressionTerm( self ):
		'''
			integerConstant | stringConstant | keywordConstant | varName | 
			varName '[' expression ']' | subroutineCall | '(' expression ')' | 
			unaryOp expressionTerm
		'''

		tok = self.input.peek()

		# print( "--", tok )

		if ( tok[ 'type' ] == 'num' or tok[ 'type' ] == 'hex' or
		     tok[ 'type' ] == 'bin' or tok[ 'type' ] == 'char' ):

			return self.parse_integerConstant()

		elif tok[ 'type' ] == 'str':

			self.input.next()

			return {

				'type'  : 'stringConstant',
				'value' : tok[ 'value' ]
			}

		elif tok[ 'type' ] == 'kw' and tok[ 'value' ] in self.keywordConstants:

			self.input.next()

			return {

				'type'  : 'keywordConstant',
				'value' : tok[ 'value' ]
			}

		elif tok[ 'type' ] == 'kw' and tok[ 'value' ] in self.memoryPointers:

			self.input.next()

			return {

				'type'  : 'memoryPointer',
				'value' : tok[ 'value' ]
			}

		elif tok[ 'type' ] == 'id':

			tok2 = self.input.peekpeek()[ 'value' ]

			# varName '[' expression ']'
			if tok2 == '[':

				self.input.next() # id

				self.input.next() # '['

				arrIdx = self.parse_expression()

				self.skip_punc( ']' )

				return {

					'type'   : 'identifier',
					'name'   : tok[ 'value' ],
					'arrIdx' : arrIdx
				}

			# subroutineCall
			elif tok2 == '(':

				ret = { 'type' : 'subroutineCall' }
				ret.update( self.parse_subroutineCall() )
				return ret

			#
			elif tok2 == '.':

				tok4 = self.input.peek4()[ 'value' ]

				# className.varName '[' expression ']'
				if tok4 == '[':

					# TODO, static access support
					raise Exception( 'External static access not yet supported' )

				# subroutineCall
				elif tok4 == '(':

					ret = { 'type' : 'subroutineCall' }
					ret.update( self.parse_subroutineCall() )
					return ret

				# varName
				else:

					# TODO, static access support
					raise Exception( 'External static access not yet supported' )

			# varName
			else:

				self.input.next()

				return {

					'type' : 'identifier',
					'name' : tok[ 'value' ]
				}
		
		# unaryOp expressionTerm
		elif tok[ 'type' ] == 'op' and tok[ 'value' ] in self.unaryOps:

			self.input.next()

			return {

				'type'    : 'unaryOp',
				'op'      : tok[ 'value' ],
				'operand' : self.parse_expressionTerm()
			}

		# '(' expression ')'
		elif tok[ 'value' ] == '(':

			return self.parse_wrapped( '(', ')', self.parse_expression )

		else:

			self.croak( 'Error: Unexpected token: {}'.format( tok ) )

	def parse_integerConstant( self ):

		tok = self.input.peek()

		if tok[ 'type' ] == 'num':

			self.input.next()

			val = int( tok[ 'value' ] )

			if val > largestInt:

				raise Exception( 'Illegal 16-bit value' )

			return {

				'type'  : 'integerConstant',
				'value' : val
			}

		elif tok[ 'type' ] == 'hex':

			self.input.next()

			val = int( tok[ 'value' ], 16 )  # str2int

			if val > largestInt:

				raise Exception( 'Illegal 16-bit value' )

			return {

				'type'  : 'integerConstant',
				'value' : val
			}

		elif tok[ 'type' ] == 'bin':

			self.input.next()

			val = int( tok[ 'value' ], 2 )  # str2int

			if val > largestInt:

				raise Exception( 'Illegal 16-bit value' )

			return {

				'type'  : 'integerConstant',
				'value' : val
			}

		elif tok[ 'type' ] == 'char':

			self.input.next()

			return {

				'type'  : 'integerConstant',
				'value' : ord( tok[ 'value' ] )  # Ascii code
			}

		else:

			self.croak( 'Error: Expecting an integerConstant. Instead got {}'.format( tok ) )


	# -----------------------------------

	def parse_wrapped( self, start, stop, parser, *args ):

		self.skip_punc( start )

		item = parser( *args )

		self.skip_punc( stop )

		return item

	def parse_delimitedList( self, start, stop, seperator, parser, *args ):

		if start: # optional start

			self.skip_punc( start )

		if self.is_punc( stop ): # empty list

			self.skip_punc( stop )

			return None
		
		items = [ parser( *args ) ]

		while self.input.peek()[ 'value' ] == seperator:

			self.input.next()  # seperator

			items.append( parser( *args ) )

		self.skip_punc( stop )

		return items

	def parse_consecutive( self, continueCondition, parser, *args ):

		items = []

		while continueCondition( self.input.peek() ):

			item = parser( *args )
			
			items.append( item )

		return items

	def retrieveIncludes( self ):

		def continueCondition( tok ):

			return tok[ 'value' ] == 'include'

		while continueCondition( self.input.peek() ):

			self.skip_kw( 'include' )

			if self.is_str():
			
				self.includes.append( self.input.next()[ 'value' ] )

			else:

				self.croak( 'Error: Expecting file or directory path. Instead got {}'.format( self.input.peek() ) )



# Test -----------------------------------------

def testParser():

	inputS = InputStream( sampleCode )
	tokenS = TokenStream( inputS )

	parser = Parser( tokenS )
	prettyPrint( parser.parse() )

# testParser()



# === Compiler ==================================================

class Compiler():

	def __init__( self ):

		self.compiler = CompileTo_HackVM()

	def compile( self, input_ ):

		inputStream = InputStream( input_ )
		tokenStream = TokenStream( inputStream )
		parser      = Parser( tokenStream )

		tree = parser.parse()
		# prettyPrint( tree )

		# return self.compiler.compile( tree )
		
		includes = parser.includes
		translation = self.compiler.compile( tree )
		return( translation, includes )


# === Compiler - Hack VM ========================================

class VariableTable():

	def __init__( self, type_ ):

		self.type_ = type_

		self.setup()

	def setup( self ):

		if self.type_ == 'class':

			self.segments = {

				'const'  : [],
				'static' : [],
				'this'   : []
			}

		elif self.type_ == 'subroutine':

			self.segments = {

				'const'    : [],
				'argument' : [],
				'local'    : []
			}

	def add( self, segment, varName, dataType, value = None ):

		self.segments[ segment ].append({

			'name'   : varName,
			'd_type' : dataType,
			'value'  : value
		})

	def lookup( self, varName, checkConstants ):

		for segName in self.segments:

			if not checkConstants and segName == 'const':

				continue  # skip segment

			seg = self.segments[ segName ]

			for idx in range( len( seg ) ):

				if seg[ idx ][ 'name' ] == varName:

					return ({

						'segName'  : segName,
						'segIdx'   : idx,
						'dataType' : seg[ idx ][ 'd_type' ],
						'value'    : seg[ idx ][ 'value' ]
					})

		return None

	def clear( self ):

		# self.segmenst = {}  # clear

		self.setup()


#----------------------------------------

class CompileTo_HackVM():

	def __init__( self ):

		self.segmentMap = {

			'static' : 'static',
			'field'  : 'this',
			'var'    : 'local',
		}

		self.curClassName = None
		self.curFunctionName = None		
		self.classVarTable = VariableTable( 'class' )
		self.subroutineVarTable = VariableTable( 'subroutine' )

		self.whileStmtCount = 0
		self.ifStmtCount = 0
		self.forStmtCount = 0
		self.whileStmtCountStack = []
		self.ifStmtCountStack = []
		self.forStmtCountStack = []
		self.currentContext = []		

	def compile( self, tree ):

		return self.compile_toplevel( tree )

	def croak( self, msg ):

		raise Exception( msg )


	# -----------------------------------

	def compile_toplevel( self, tree ):

		# -- Each file contains only one class
		return self.compile_classDeclaration( tree )

		# -- Each file can contain multiple classes
		''' 
		    Atm won't work due to way we handle statics.
		    'push/pop static index' vm command does not have enough info
		    for vm2asm compiler to determine class which command belongs to
		    when it's generating '@className.index' commands

		    TODO - Resolve if wish to support multiple classes in a file
		'''
		# output = ''

		# for t in tree:

		# 	self.setup()

		# 	output += self.compile_classDeclaration( t )

		# return output


	# -----------------------------------

	def pushConstant_( self, n ):

		return 'push constant {}\n'.format( n )

	def push_( self, seg_name, val ):

		return 'push {} {}\n'.format( seg_name, val )

	def pop_( self, seg_name, val ):

		return 'pop {} {}\n'.format( seg_name, val )

	def call_( self, fx_name, nArgs ):

		return 'call {} {}\n'.format( fx_name, nArgs )

	def label_( self, label_name ):

		return 'label {}\n'.format( label_name )

	def goto_( self, label_name ):

		return 'goto {}\n'.format( label_name )

	def ifgoto_( self, label_name ):

		return 'if-goto {}\n'.format( label_name )

	def return_ ( self ) : return 'return\n'

	def eq_     ( self ) : return 'eq\n'
	def gt_     ( self ) : return 'gt\n'
	def lt_     ( self ) : return 'lt\n'
	def gte_    ( self ) : return 'gte\n'
	def lte_    ( self ) : return 'lte\n'
	def ne_     ( self ) : return 'ne\n' 

	def and_    ( self ) : return 'and\n'
	def or_     ( self ) : return 'or\n'
	def not_    ( self ) : return 'not\n'
	def xor_    ( self ) : return 'xor\n'

	def add_    ( self ) : return 'add\n'
	def sub_    ( self ) : return 'sub\n'
	def neg_    ( self ) : return 'neg\n'
	def shiftR_ ( self ) : return 'shiftR\n'
	def shiftL_ ( self ) : return 'shiftL\n'

	def mult_   ( self ) : return 'mult\n' # temp, hardware
	def div_    ( self ) : return 'div\n'  # temp, hardware


	# -----------------------------------

	def addToVarTable( self, table, variableDeclarations ):

		if variableDeclarations:

			for vDec in variableDeclarations:

				dataType  = vDec[ 'd_type' ]

				varType = vDec.get( 'var_type' )

				if varType:

					# const
					if varType == 'const':

						table.add( 'const', vDec[ 'name' ], dataType, vDec[ 'value' ] )

					# static | field | var
					else:

						segment = self.segmentMap[ varType ]

						for name in vDec[ 'names' ]:

							table.add( segment, name, dataType )

				else:

					# Assume argument
					table.add( 'argument', vDec[ 'name' ], dataType )

	def lookupVar( self, varName, checkConstants = False ):

		# Check subroutine table
		found = self.subroutineVarTable.lookup( varName, checkConstants )
		if found: return found

		# Check class table
		found = self.classVarTable.lookup( varName, checkConstants )
		if found: return found

		return None


	# -----------------------------------

	def setupForClassDeclaration( self ):
		
		self.classVarTable.clear()

	def compile_classDeclaration( self, exp ):

		self.setupForClassDeclaration()

		self.curClassName = exp[ 'name' ]

		# -- Add variables to table
		self.addToVarTable( self.classVarTable, exp[ 'constDec' ] )
		self.addToVarTable( self.classVarTable, exp[ 'varDec' ] )

		# -- Subroutines
		s = ''
		for subDec in exp[ 'subDec' ]:

			s += self.compile_subroutineDeclaration( subDec )

		return s

	def setupForSubroutineDeclaration( self ):

		self.subroutineVarTable.clear()

		self.whileStmtCount = 0
		self.ifStmtCount = 0
		self.forStmtCount = 0
		self.whileStmtCountStack = []
		self.ifStmtCountStack = []
		self.forStmtCountStack = []
		self.currentContext = []

	def compile_subroutineDeclaration( self, exp ):

		self.setupForSubroutineDeclaration()

		s = ''
		
		fx_type = exp[ 'fx_type' ]

		# -- Add variables to table
		if fx_type == 'method':

			# Add placeholder for 'self' arg
			self.subroutineVarTable.add( 
				'argument', 
				'*',  # used as won't collide with a potential Hack HL variable name
				'placeholder'
			)

		self.addToVarTable( self.subroutineVarTable, exp[ 'params' ] )
		
		self.addToVarTable( self.subroutineVarTable, exp[ 'constDec' ] )
		self.addToVarTable( self.subroutineVarTable, exp[ 'varDec' ] )

		nArgs   = len( self.subroutineVarTable.segments[ 'argument' ] )
		nLocals = len( self.subroutineVarTable.segments[ 'local' ] )

		# -- Name
		fxName = '{}.{}'.format( self.curClassName, exp[ 'name' ] )
		s = 'function {} {}\n'.format( fxName, nLocals )

		# -- Header
		if fx_type == 'method':

			# Position THIS pointer
			s += self.push_( 'argument', 0 )
			s += self.pop_( 'pointer', 0 )

		elif fx_type == 'constructor':

			# Allocate field variables
			nFields = len( self.classVarTable.segments[ 'this' ] )
			s += self.pushConstant_( nFields )
			s += self.call_( 'DataMemory.alloc', 1 )
			# s += self.call_( 'Memory.alloc', 1 )
			s += self.pop_( 'pointer', 0 )

		# -- Statements
		s += self.compile_statements( exp[ 'statements' ] )

		# -- Check if return statement present
		if s[ -7 : ] != 'return\n':

			# Allow users to omit return statemens in void subroutines
			if exp[ 'ret_type' ] == 'void':

				# return 0
				s += self.compile_returnStatement({

					'type'  : 'returnStatement',
					'value' : 0
				})

			else:

				self.croak( 'Error: Expecting a return statement in the function ' + exp[ 'name' ] )

		return s

	def compile_statements( self, statements ):

		s = ''

		if statements:

			for statement in statements:

				s += self.compile_statement( statement )

		return s

	def compile_statement( self, exp ):

		if   exp[ 'type' ] == 'subroutineCall'    : return self.compile_doStatement( exp )
		elif exp[ 'type' ] == 'assignment'        : return self.compile_letStatement( exp )
		elif exp[ 'type' ] == 'whileStatement'    : return self.compile_whileStatement( exp )
		elif exp[ 'type' ] == 'ifStatement'       : return self.compile_ifStatement( exp )
		elif exp[ 'type' ] == 'forStatement'      : return self.compile_forStatement( exp )
		elif exp[ 'type' ] == 'returnStatement'   : return self.compile_returnStatement( exp )
		elif exp[ 'type' ] == 'breakStatement'    : return self.compile_breakStatement( exp )
		elif exp[ 'type' ] == 'continueStatement' : return self.compile_continueStatement( exp )

		else:
			self.croak( "Error: Don't know how to compile the statement " + exp[ 'type' ] )

	def compile_doStatement( self, exp ):

		s = self.compile_subroutineCall( exp )
		s += self.pop_( 'temp', 0 )

		return s

	def compile_subroutineCall( self, exp ):

		s = ''
		nArgs = 0

		# -- Push instance's base address when calling methods
		#  'classInstanceName.methodName()' calls method of class the instance belongs to 
		#  'className.functionName()' calls function or constructor of class 'className'
		#  'methodName()' calls method in current class
		name = exp[ 'name' ]

		if '.' in name:

			cName, subName = name.split( '.' )

			instance = self.lookupVar( cName )

			# 'classInstanceName.methodName()'
			if instance:

				# Push base address of instance (stored in this/local/static n)
				s += self.push_( instance[ 'segName' ], instance[ 'segIdx' ] )
				nArgs += 1

				name = '{}.{}'.format( instance[ 'dataType' ], subName )  # dataType is className of instance

			# 'className.functionName()'
			else: pass

		# 'methodName()'
		else:

			# Assume called by method of the current class,
			#  so push base address of self (stored in THIS pointer)
			s += self.push_( 'pointer', 0 )
			nArgs += 1

			name = '{}.{}'.format( self.curClassName, name )

			# TODO, anyway to differentiate between function and method
			#  of current class... so that instead of assuming, push
			#  pointer only when method... and thus can also call functions
			#  without including className
		
		# -- Push passed in args onto stack
		args = exp[ 'args' ]

		if args:

			nArgs += len( args )
			
			for expr in args:

				s += self.compile_expression( expr )

		# -- Call statement
		s += self.call_( name, nArgs )

		return s

	def compile_letStatement( self, exp ):

		s = ''

		# -- Right
		right = self.compile_expression( exp[ 'right' ] )

		# -- Pop to left
		op = exp[ 'assignmentOp' ]

		varName = exp[ 'left' ][ 'name' ]

		left = self.lookupVar( varName )

		if not left:

			raise Exception( 'Error: Undefined variable - ' + varName )

		arrIdx = exp[ 'left' ].get( 'arrIdx' )

		if arrIdx:

			# Calc address
			s += self.compile_expression( arrIdx )
			s += self.push_( left[ 'segName' ], left[ 'segIdx' ] )
			s += self.add_()

			# Calc value
			if op == '=':

				s += right

			else:  # +=, -=, *= etc.

				s += self.push_( left[ 'segName' ], left[ 'segIdx' ] )
				s += right
				s += self.compile_binaryOp( op[ : -1 ] )

			s += self.pop_( 'temp', 0 )

			# Set address
			s += self.pop_( 'pointer', 1 )

			# Set RAM[address] to value
			s += self.push_( 'temp', 0 )
			s += self.pop_( 'that', 0 )

		else:

			# Calc value
			if op == '=':

				s += right

			else:  # compound assignment such as +=, -=, &=

				s += self.push_( left[ 'segName' ], left[ 'segIdx' ] )
				s += right
				s += self.compile_binaryOp( op[ : -1 ] )

			# Set var to value
			s += self.pop_( left[ 'segName' ], left[ 'segIdx' ] )

		return s

	def compile_statementBlock( self, exp ):

		if isinstance( exp, list ):

			return self.compile_statements( exp )

		else:

			return self.compile_statement( exp )

	def compile_whileStatement( self, exp ):

		'''
			label COND
			cond
			if-goto BODY
			goto END
			label BODY
			body
			goto COND
			label END
		'''

		# -- Track count
		self.whileStmtCount += 1		
		n = self.whileStmtCount

		# -- Push context
		self.currentContext.append( ( 'WHILE', n ) )
		
		# -- Loop

		# - Cond
		s = 'label WHILE_COND{}\n'.format( n )

		s += self.compile_expression( exp[ 'cond' ] )

		s += 'if-goto WHILE_BODY{}\n'.format( n )
		s += 'goto WHILE_END{}\n'.format( n )

		# - Body
		s += 'label WHILE_BODY{}\n'.format( n )

		self.whileStmtCountStack.append( n )  # Save parent count
		
		s += self.compile_statementBlock( exp[ 'body' ] )

		n = self.whileStmtCountStack.pop()  # Restore parent count	

		s += 'goto WHILE_COND{}\n'.format( n )

		# -- End
		s += 'label WHILE_END{}\n'.format( n )

		# -- Pop context
		self.currentContext.pop()
		
		return s

	def compile_ifStatement( self, exp ):

		self.ifStmtCount += 1
		n = self.ifStmtCount

		if exp[ 'else' ] :

			'''
				cond
				if-goto THEN
				goto ELSE
				label THEN
				thenBody
				goto END
				label ELSE
				elseBody
				label END
			'''

			# -- Cond
			s = self.compile_expression( exp[ 'cond' ] )

			s += 'if-goto IF_THEN{}\n'.format( n )
			s += 'goto IF_ELSE{}\n'.format( n )

			# -- Then
			s += 'label IF_THEN{}\n'.format( n )

			self.ifStmtCountStack.append( n )  # Save parent count

			s += self.compile_statementBlock( exp[ 'then' ] )

			n = self.ifStmtCountStack.pop()  # Restore parent count

			s += 'goto IF_END{}\n'.format( n )

			# -- Else
			s += 'label IF_ELSE{}\n'.format( n )

			self.ifStmtCountStack.append( n )  # Save parent count

			s += self.compile_statementBlock( exp[ 'else' ] )

			n = self.ifStmtCountStack.pop()  # Restore parent count

		else :

			'''
				cond
				if-goto THEN
				goto END
				label THEN
				thenBody
				label END
			'''

			# -- Cond
			s = self.compile_expression( exp[ 'cond' ] )

			s += 'if-goto IF_THEN{}\n'.format( n )
			s += 'goto IF_END{}\n'.format( n )

			# -- Then
			s += 'label IF_THEN{}\n'.format( n )

			self.ifStmtCountStack.append( n )  # Save parent count

			s += self.compile_statements( exp[ 'then' ] )

			n = self.ifStmtCountStack.pop()  # Restore parent count

		# -- End
		s += 'label IF_END{}\n'.format( n )

		return s

	def compile_forStatement( self, exp ):

		'''
			label COND
			cond
			if-goto BODY
			goto END
			label BODY
			body
			goto COND
			label END
		'''

		# -- Track count
		self.forStmtCount += 1
		n = self.forStmtCount

		# -- Push context
		self.currentContext.append( ( 'FOR', n ) )

		# -- Setup
		s = self.compile_letStatement( exp[ 'init' ] )

		# -- Loop

		# - Cond
		s += 'label FOR_COND{}\n'.format( n )

		s += self.compile_expression( exp[ 'cond' ] )

		s += 'if-goto FOR_BODY{}\n'.format( n )
		s += 'goto FOR_END{}\n'.format( n )

		# - Body
		s += 'label FOR_BODY{}\n'.format( n )

		self.forStmtCountStack.append( n )  # Save parent count

		s += self.compile_statementBlock( exp[ 'body' ] )

		n = self.forStmtCountStack.pop()  # Restore parent count

		# - Update
		s += 'label FOR_UPDATE{}\n'.format( n )

		s += self.compile_letStatement( exp[ 'update' ] )

		s += 'goto FOR_COND{}\n'.format( n )

		# -- End
		s += 'label FOR_END{}\n'.format( n )

		# -- Pop context
		self.currentContext.pop()

		return s

	def compile_returnStatement( self, exp ):

		s = ''

		value = exp[ 'value' ]

		if value == 0:

			s += self.pushConstant_( 0 )

		else:

			s += self.compile_expression( value )

		s += self.return_()

		return s

	def compile_breakStatement( self, exp ):

		s = 'goto {}_END{}\n'.format( *self.currentContext[ -1 ] )

		return s

	def compile_continueStatement( self, exp ):

		context = self.currentContext[ -1 ]

		print( context )

		if context[ 0 ] == 'FOR':

			s = 'goto {}_UPDATE{}\n'.format( *context )

		else:

			s = 'goto {}_COND{}\n'.format( *context )

		return s

	def compile_binaryOp( self, op ):

		# Logic ---
		if   op == '&': return self.and_()
		elif op == '|': return self.or_()

		elif op == '^':
			if USE_COMPATIBLE: return self.call_( 'Math.xor', 2 )
			else:              return self.xor_()


		# Arithmetic ---
		elif op == '+': return self.add_()
		elif op == '-': return self.sub_()

		elif op == '%': return self.call_( 'Math.mod', 2 )

		elif op == '*':
			if USE_COMPATIBLE: return self.call_( 'Math.multiply', 2 )
			else:              return self.mult_()

		elif op == '/':
			if USE_COMPATIBLE: return self.call_( 'Math.divide', 2 )
			else:              return self.div_()

		elif op == '>>': 
			if USE_COMPATIBLE: return self.call_( 'Math.lsr', 2 )
			else:              return self.shiftR_()

		elif op == '<<': 
			if USE_COMPATIBLE: return self.call_( 'Math.lsl', 2 )
			else:              return self.shiftL_()


		# Comparison ---
		elif op == '=' or op == '==': return self.eq_()
		elif op == '>': return self.gt_()
		elif op == '<': return self.lt_()

		elif op == '>=':
			if USE_COMPATIBLE: return self.call_( 'Math.gte', 2 )
			else:              return self.gte_()

		elif op == '<=':
			if USE_COMPATIBLE: return self.call_( 'Math.lte', 2 )
			else:              return self.lte_()

		elif op == '!=':
			if USE_COMPATIBLE: return self.call_( 'Math.ne', 2 )
			else:              return self.ne_()


		# ---
		else:
			self.croak( "Error: Don't know how to compile the binaryOp " + op )

	def compile_expression( self, exp ):

		s = ''

		if exp == None:

			return ''

		elif isinstance( exp, dict ):

			return self.compile_expressionTerm( exp )

		else:

			s += self.compile_expression( exp[0] )

			for i in range( 1, len( exp ), 2 ):

				s += self.compile_expression( exp[ i + 1 ] )
				s += self.compile_binaryOp( exp[ i ][ 'value' ] )

			return s

	def compile_expressionTerm( self, exp ):

		if exp[ 'type' ] == 'integerConstant':

			return self.pushConstant_( exp[ 'value' ] )

		elif exp[ 'type' ] == 'stringConstant':

			msg = exp[ 'value' ]

			# Create String instance
			s = self.pushConstant_( len( msg ) )
			s += self.call_( 'String.new', 1 )  # returns self

			# Fill it (verbatim)
			# for c in msg:
			# 	s += self.pushConstant_( ord( c ) )  # Ascii code
			# 	s += self.call_( 'String.appendChar', 2 )  # returns self

			# Fill it (handling special characters)
			i = 0
			while i < len( msg ):

				c = msg[i]

				if c == '\\':  # escape character

					c2 = msg[ i + 1 ]

					if c2 in 'tnr':
						
						if c2 == 't': c = 9   # tab
						if c2 == 'n': c = 10  # newline
						if c2 == 'r': c = 13  # Windows carriage

						i += 2

					else:

						c = ord( c )
						i += 1

				else:

					c = ord( c )
					i += 1

				s += self.pushConstant_( c )
				s += self.call_( 'String.appendChar', 2 )  # returns self

			#
			return s

		elif exp[ 'type' ] == 'charConstant':

			return self.pushConstant_( ord( exp[ 'value' ] ) )  # Ascii code


		elif exp[ 'type' ] == 'keywordConstant':

			kw = exp[ 'value' ]

			if kw == 'true':

				s = self.pushConstant_( 0 )
				s += self.not_()
				return s

			elif kw == 'false' or kw == 'null':

				return self.pushConstant_( 0 )

			elif kw == 'this':

				return self.push_( 'pointer', 0 )

		elif exp[ 'type' ] == 'memoryPointer':

			return self.pushConstant_( Hack_pointerMap[ exp[ 'value' ] ] )
		
		elif exp[ 'type' ] == 'identifier':

			name = exp[ 'name' ]

			loc = self.lookupVar( name, True )

			if not loc:

				raise Exception( 'Error: Undefined variable - ' + name )

			arrIdx = exp.get( 'arrIdx' )

			if arrIdx:

				# Retrieve value and push to stack
				s  = self.push_( loc[ 'segName' ], loc[ 'segIdx' ] )
				s += self.compile_expression( arrIdx )
				s += self.add_()
				s += self.pop_( 'pointer', 1 )
				s += self.push_( 'that', 0 )
				return s

			else:

				# Push value to stack
				if loc[ 'segName' ] == 'const':

					return self.compile_expressionTerm( loc[ 'value' ] )

				else:

					return self.push_( loc[ 'segName' ], loc[ 'segIdx' ] )

		elif exp[ 'type' ] == 'subroutineCall':

			return self.compile_subroutineCall( exp )

		elif exp[ 'type' ] == 'unaryOp':

			s = self.compile_expression( exp[ 'operand' ] )

			op = exp[ 'op' ]

			if op == '!' or op == '~':

				s += self.not_()

			elif op == '-':

				s += self.neg_()

			return s

		else:

			self.croak( "Error: Don't know how to compile the expressionTerm " + exp[ 'type' ] )



# === Compiler - TODO =========================================

# class CompileTo_Python(): pass
# class CompileTo_JavaScript(): pass



# -- Run -----------------------------------------

def genVMFile( inputFilePath, outputFilePath, useCompatibleVM = False ):

	global USE_COMPATIBLE

	# Setup compatibility
	USE_COMPATIBLE = useCompatibleVM

	# Init compiler
	compiler = Compiler()

	# Read
	with open( inputFilePath, 'r' ) as file:
		
		jackCode = file.read()

	# Translate
	vmCode, includes = compiler.compile( jackCode )

	# Write
	with open( outputFilePath, 'w' ) as file:

		file.write( vmCode )

	print( 'Done' )



def getJackFilesFromDir( dirPath ):

	fileNames = os.listdir( dirPath )

	filePaths = []

	for fileName in fileNames:

		if fileName[ -4 : ] == 'jack':

			filePath = dirPath + '/' + fileName

			filePaths.append( filePath )

	return filePaths


def translateFile( compiler, className, inputFilePath, outputDirPath, includes ):

	print( ' - Translating {}'.format( inputFilePath ) )

	outputFilePath = '{}/{}.vm'.format( outputDirPath, className )

	# Read
	with open( inputFilePath, 'r' ) as file:
		
		jackCode = file.read()

	vmCode, includes_ = compiler.compile( jackCode )

	# Write
	with open( outputFilePath, 'w' ) as file:

		file.write( vmCode )

	includes.extend( includes_ )


def genVMFiles( inputDirPath, useCompatibleVM = False ):

	global USE_COMPATIBLE

	# Setup compatibility
	USE_COMPATIBLE = useCompatibleVM

	# Init compiler
	compiler = Compiler()

	# Translate jack files in input directory
	classes = []
	processedFiles = []

	includes = []

	inputFilePaths = getJackFilesFromDir( inputDirPath )

	for inputFilePath in inputFilePaths:

		className = re.search( '\w+(?=\.jack)', inputFilePath ).group( 0 )

		if className in classes:

			raise Exception( 'Error: More than one class is named {}\n\t{}\n\t{}\n'.format(

				className,
				'\n\t'.join( processedFiles ),
				path
			) )

		else:

			classes.append( className )

			translateFile( compiler, className, inputFilePath, inputDirPath, includes )

	processedFiles.extend( inputFilePaths )


	# Translate 'included' jack files. Pass on 'included' vm files
	vmIncludes = []

	while len( includes ) > 0:

		path = includes.pop()

		className = re.search( '\w+(?=\.jack)|\w+(?=\.vm)', path ).group( 0 )

		if className in classes:

			# raise Exception( 'Error: More than one class is named {}\n\t{}\n\t{}\n'.format(

			# 	className,
			# 	'\n\t'.join( processedFiles ),
			# 	path
			# ) )

			print( ' Note: More than one class is named {}. As such, ignored \n\t{}'.format(

				className, path
			) )

		else:

			classes.append( className )

			# Generated VM files are appended to the input directory instead of 
			#  replacing the ones in the source directory
			if path[ - 4 : ] == 'jack':

				translateFile( compiler, className, path, inputDirPath, includes )

			# Paths of included VM files passed on as is
			elif path[ - 2 : ] == 'vm':

				vmIncludes.append( path )
			
			processedFiles.append( path )


	# Return list of included VM files
	return vmIncludes

	# print( 'Done' )


# inputFile = ''
# outputFile = ''
# genVMFile( inputFile, outputFile )

# readPath = ''
# genVMFiles( readPath )
