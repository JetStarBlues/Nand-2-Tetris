# ========================================================================================
#
#  Description:
#
#     Compiles Hack VM (virtual machine) code to Hack ASM (assembly) code
#
#  Attribution:
#
#     Code by www.jk-quantized.com
#
#     Design is based on:
#
#        Lecture notes from the Nand To Tetris course
#         www.nand2tetris.org
#
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
#
# ========================================================================================

'''
	--- Notes ---

	> Segment use

		If 'one-time' safe to use again as value was used up immediately

		. Temp 0 - (in hl2vm) one-time
		            . by 'array assignment' to save return value
		            . to discard return value from standalone 'call'
		. Temp 1 - (in hl2vm) one-time
		            . by 'comparisonOp2' to save 'x' value
		. Temp 2 - (in hl2vm) one-time
		            . by 'comparisonOp2' to save 'y' value
		. Temp 3 - (in hl2vm) one-time
		            . by 'comparisonOp2' to save return address
		. Temp 4 -
		. Temp 5 -
		. Temp 6 -
		. Temp 7 -
		. GP   0 - (in vm2asm) one-time by,
		            . 'return'   to save return address
		            . 'pop'      to save target address
		            . 'shift op' to workaround limited instruction set
		. GP   1 - (in vm2asm) by 'generic call' to save address
		. GP   2 - (in vm2asm) by 'generic call' to save nArgs

'''

'''
	TODO
	- test comparison ops!

	- optimize for 0, 1, -1, 'x+1', 'x-1',
		push constant 0/1
		(neg/add/sub)
		pop static/local/arg idx
'''


# == Imports =======================================================

# Built ins
import re
import os

# Hack computer
import Components._0__globalConstants as GC



# == Main ==========================================================

# -- Lookup tables ---------------------------------

segmentPointer = {
	
	'argument' : '@ARG',
	'local'    : '@LCL',
	'this'     : '@THIS',
	'that'     : '@THAT',
}

unaryOps = {
	
	'not' : '!',
	'neg' : '-',
}
binaryOps = {
	
	'and' : '&',
	'or'  : '|',
	'add' : '+',
	'sub' : '-',
	'xor' : '^',
	'lsr' : '>>',
	'lsl' : '<<',
}
comparisonOps = {

	'eq'  : 'JEQ',
	'gt'  : 'JGT',
	'lt'  : 'JLT',
	'gte' : 'JGE',
	'lte' : 'JLE',
	'ne'  : 'JNE',
}
# operations = unaryOps + binaryOps + comparisonOps
operations = dict( unaryOps )
operations.update( binaryOps )
operations.update( comparisonOps )



# -- Extraction -------------------------------------

# Select everything that is not a comment
cmdPattern = '''
	^                # from beginning of string
	.*?              # select all characters until
	(?=\/\/|[\r\n])  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )

def extractCmd( line ):

	found = re.search( cmdPattern, line )  # select everything that is not a comment

	if found:

		cmd = found.group( 0 )
		cmd = cmd.strip()  # remove leading and trailing whitespace
		return cmd.split( ' ' )  # split on spaces

	else:

		return None



# -- Translation -------------------------------------

class Feed():

	def __init__( self, cmdList ):

		self.pos = 0

		self.cmdList = cmdList

		self.end = len( cmdList )

	def next( self ):

		if self.eof( self.pos ):

			return None
		
		else:

			cmd = self.cmdList[ self.pos ]

			self.pos += 1

			return cmd

	def peek( self ):

		if self.eof( self.pos ):

			return None

		return self.cmdList[ self.pos ]

	def peekpeek( self ):

		if self.eof( self.pos + 1 ):

			return None

		return self.cmdList[ self.pos + 1 ]

	def eof( self, pos ):

		return pos >= self.end



class Compiler():

	def __init__( self ):

		# Set SP
		self.SP = GC.STACK_START

		# Track scope
		self.curClassName = None
		self.curFunctionName = None

		# Use generic functions
		self.useGenerics = True

		# Include comments in generated asm file
		self.debug = False

		# Optimize generated assembly
		self.optimize = False

		# Skip cmd
		self.skip = False
		self.skip2 = False


	def setup( self ):

		self.compCount = 0              # track jump positions of comparison operations
		self.returnPosCount = 0         # track return positions of calls
		self.returnGenericPosCount = 0  # track return positions of generic ASM calls


	def compile( self, cmds, debug = False ):

		self.debug = debug

		self.setup()

		out = []

		out.append( self.compile_bootstrap() )

		for className in cmds:

			if self.debug:

				out.append( '\n// === {} ===\n'.format( className ) )

			out.append( self.compile_topLevel( className, cmds[ className ] ) )

		return self.a2s( out )


	def compile_topLevel( self, className, cmdList ):

		self.curClassName = className

		self.input = Feed( cmdList )

		return self.compile_statements()



	# --------------------------------------

	def a2s( self, a ):

		# Return newline delimited string
		return '\n'.join( a )

	def at( self, x ):

		return '@' + str( x )

	def atTemp( self, index ):

		return '@TEMP{}'.format( index )

	def atGP( self, index ):

		return '@GP{}'.format( index )

	def atStatic( self, index, className = None ):

		className_ = className if className else self.curClassName

		return '@{}.{}'.format( className, index )  # support external access

	def label( self, loc ):

		return '({})'.format( loc )

	def pushDToStack( self ):

		s = []

		# Push it to stack
		s.append( '@SP' )
		s.append( 'A = M' )  # set A reg to address held by SP
		s.append( 'M = D' )  # set value at said address

		# Increment address held by SP
		s.append( '@SP' )
		s.append( 'M = M + 1' )

		return self.a2s( s ) 

	def popStackToD( self ):

		s = []

		# Decrement address held by SP, and get the value
		s.append( '@SP' )

		# s.append( 'AM = M - 1' )
		s.append( 'D = M - 1' )
		s.append( 'M = D' )
		s.append( 'A = D' )

		s.append( 'D = M' )

		return self.a2s( s )



	# --------------------------------------

	def compile_statements( self, exitCondition = None ):

		s = []

		while True:

			cmd = self.input.next()

			if cmd:

				if self.skip2:

					self.skip = True

					self.skip2 = False

					continue  # go to next iteration

				if self.skip:

					self.skip = False

					continue  # go to next iteration

				if self.debug:

					s.append( '// {}'.format( ' '.join( cmd ) ) )

				s.append( self.compile_statement( cmd ) )

			else:

				break

		return self.a2s( s )


	def compile_statement( self, cmd ):

		cmdType = cmd[ 0 ]

		if cmdType == 'push':

			if len( cmd ) == 4:

				return self.compile_push( cmd[ 1 ], int( cmd[ 2 ] ), cmd[ 3 ] )

			else:

				return self.compile_push( cmd[ 1 ], int( cmd[ 2 ] ) )

		elif cmdType == 'pop':

			if len( cmd ) == 4:

				return self.compile_pop( cmd[ 1 ], int( cmd[ 2 ] ), cmd[ 3 ] )

			else:

				return self.compile_pop( cmd[ 1 ], int( cmd[ 2 ] ) )

		elif cmdType in operations:

			return self.compile_operation( cmdType )

		elif cmdType == 'label':

			return self.compile_label( cmd[ 1 ] )

		elif cmdType == 'goto':

			return self.compile_goto( cmd[ 1 ] )

		elif cmdType == 'if-goto':

			return self.compile_ifgoto( cmd[ 1 ] )

		elif cmdType == 'call':

			return self.compile_call( cmd[ 1 ], int( cmd[ 2 ] ) )

		elif cmdType == 'function':

			return self.compile_function( cmd[ 1 ], int( cmd[ 2 ] ) )

		elif cmdType == 'return':

			return self.compile_return()

		else:

			raise Exception( "Don't know how to compile the command - {}".format( cmd ) )


	def compile_push_( self, seg, index, className = None ):

		s = []

		# Get value from segment
		if seg == 'constant':

			s.append( self.at( index ) )
			s.append( 'D = A' )

		elif seg == 'pointer':

			if index == 0: s.append( '@THIS' )
			else:          s.append( '@THAT' )

			s.append( 'D = M' )

		elif seg == 'static':

			s.append( self.atStatic( index, className ) )
			s.append( 'D = M' )

		elif seg == 'temp':

			s.append( self.atTemp( index ) )
			s.append( 'D = M' )

		else:  # arg, local, this, that

			if index == 0:

				s.append( segmentPointer[ seg ] )
				s.append( 'A = M' )

			else:

				s.append( self.at( index ) )
				s.append( 'D = A' )
				s.append( segmentPointer[ seg ] )
				s.append( 'A = M + D' )
			
			s.append( 'D = M' )

		return self.a2s( s )


	def compile_push( self, seg, index, className = None ):

		s = []

		# Get value from segment
		s.append( self.compile_push_( seg, index, className ) )

		# Push it to stack
		s.append( self.pushDToStack() )

		return self.a2s( s )


	def compile_pop( self, seg, index, className = None ):

		s = []

		if seg == 'pointer' or seg == 'static' or seg == 'temp':

			# Get value from stack
			s.append( self.popStackToD() )

			# Get target address
			if seg == 'pointer':

				if index == 0: s.append( '@THIS' )
				else:          s.append( '@THAT' )

			elif seg == 'static':

				s.append( self.atStatic( index, className ) )

			elif seg == 'temp':

				s.append( self.atTemp( index ) )

			# Pop value to target address
			s.append( 'M = D' )

		else:  # arg, local, this, that

			# Get target address
			if index == 0:

				s.append( segmentPointer[ seg ] )
				s.append( 'D = M' )

			else:

				s.append( self.at( index ) )
				s.append( 'D = A' )
				s.append( segmentPointer[ seg ] )
				s.append( 'D = M + D' )

			# Save address to temporary location
			s.append( self.atGP( 0 ) )
			s.append( 'M = D' )

			# Get value from stack
			s.append( self.popStackToD() )

			# Pop value to target address
			s.append( self.atGP( 0 ) )
			s.append( 'A = M' )
			s.append( 'M = D' )

		return self.a2s( s )


	def compile_operation( self, op ):

		'''
			12            12             12
			7    sub ->   4    neg ->    -4
			3             SP             SP
			SP
		'''

		s = []

		if op in unaryOps:

			s.append( '@SP' )
			s.append( 'A = M - 1' )
			s.append( 'M = {} M'.format( unaryOps[ op ] ) )

		elif op in binaryOps:

			if op == 'lsl' or op == 'lsr':

				# Workaround for available shift instructions ( D << M or D >> M )

				# Get prev value
				s.append( self.popStackToD() )  # D = prev_val
				s.append( self.atGP( 0 ) )
				s.append( 'M = D' )             # Temp[1] = prev_val

				# Get prevprev value
				s.append( '@SP' )
				s.append( 'A = M - 1' )  # aReg = prevprev_addr
				s.append( 'D = M' )      #    D = prevprev_val

				# Apply op
				s.append( self.atGP( 0 ) )
				s.append( 'D = D {} M'.format( binaryOps[ op ] ) )  # D = prevprev_val op prev_val
				s.append( '@SP' )
				s.append( 'A = M - 1' )  #  aReg = prevprev_addr
				s.append( 'M = D' )      # stack = D

			else:

				# Get prev value
				s.append( self.popStackToD() )  # D = prev_val

				# Get prevprev value 
				s.append( 'A = A - 1' )  # aReg = prevprev_addr

				# Apply op
				s.append( 'M = M {} D'.format( binaryOps[ op ] ) )  # stack = prevprev_val op prev_val

		elif op in comparisonOps:
			
			s.append( self.compile_comparisonOp( op ) )

		return self.a2s( s )


	def compile_comparisonOp_( self, op ):

		s = []

		cTrue = 'comp_true{}'.format( self.compCount )
		cEnd  = 'comp_end{}'.format( self.compCount )
		self.compCount += 1

		# Compare
		s.append( 'D = M - D' )  # D = prevprev_val - prev_val
		s.append( self.at( cTrue ) )
		s.append( 'D ; {}'.format( comparisonOps[ op ] ) )
		
		# False
		s.append( 'D = 0' )
		s.append( self.at( cEnd ) )
		s.append( '0 ; JMP' )
		
		# True
		s.append( self.label( cTrue ) )
		s.append( 'D = - 1' )
		
		# End/continue
		s.append( self.label( cEnd ) )

		return self.a2s( s )


	def compile_comparisonOp( self, op ):

		s = []

		# Get prev value
		s.append( self.popStackToD() )  # D = prev_val

		# Get prevprev value
		s.append( 'A = A - 1' )  # aReg = prevprev_addr

		# Compare
		if self.useGenerics:

			if op == 'eq' or op == 'ne':
				
				s.append( self.compile_comparisonOp_( op ) )  # simple

			else:

				s.append( self.compile_comparisonOp2_( op ) )  # not so simple, but correct

		else:
		
			s.append( self.compile_comparisonOp_( op ) )  # simple

		# Update stack
		s.append( '@SP' )
		s.append( 'A = M - 1' )
		s.append( 'M = D' )

		return self.a2s( s )


	def compile_comparisonOp2_( self, op ):

		s = []

		returnPos = 'comp_returnPosition{}'.format( self.compCount )
		self.compCount += 1

		# Save x and y values
		s.append( 'B = M' )
		s.append( self.atTemp( 1 ) )
		s.append( 'M = B' )          # x
		s.append( self.atTemp( 2 ) )
		s.append( 'M = D' )          # y

		# Save return position
		s.append( self.at( returnPos ) )
		s.append( 'D = A' )
		s.append( self.atTemp( 3 ) )
		s.append( 'M = D' )           # returnPos

		# Goto respective generic comparison function
		#  Sets D to result of comparison
		if op == 'lt':

			s.append( self.at( '$_genericComparisonOpLt' ) )
			s.append( '0 ; JMP' )

		elif op == 'lte':

			s.append( self.at( '$_genericComparisonOpLte' ) )
			s.append( '0 ; JMP' )

		elif op == 'gt':

			s.append( self.at( '$_genericComparisonOpLte' ) )
			s.append( '0 ; JMP' )

		elif op == 'gte':

			s.append( self.at( '$_genericComparisonOpLt' ) )
			s.append( '0 ; JMP' )

		# Create label for return position
		s.append( self.label( returnPos ) )

		if op == 'gt' or op == 'gte':

			s.append( 'D = ! D' )

		#
		return self.a2s( s )


	def compile_comparisonOp2_bootstrap( self ):

		''' Code is based on @Cadet1620's answer on this forum discussion:
		      http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/Greater-or-less-than-when-comparing-numbers-with-different-signs-td4031520.html
		'''

		'''
			Python equivalent of what subsequent assembly code aims to do

			def lt ( x, y ):

				if isNeg( x ):

					if not isNeg( y ):

						return True

					# isNeg( x ) and isNeg( y ) - aka same signs

				else:

					if isNeg( y ):

						return False

					# not isNeg( x ) and not isNeg( y ) - aka same signs

				# same signs
				if isNeg( d ):

					return True

				else:

					return False


			def lte ( x, y ):

				d = x - y

				if isNeg( x ):

					if not isNeg( y ):

						return True

					# isNeg( x ) and isNeg( y ) - aka same signs

				else:

					if isNeg( y ):

						return False

					# not isNeg( x ) and not isNeg( y ) - aka same signs

				# same signs
				if isNeg( d ):

					return True

				else:

					if isZero( d ):

						return True

					else:

						return False


			def gt ( x, y ):

				return not lte(x, y )

			def gte ( x, y ):

				return not lt( x, y )
		'''

		s = []

		# ___ Lt _______________________________________________________________

		# Create label
		s.append( self.label( '$_genericComparisonOpLt' ) )

		s.append(    self.at( 'xIsNotNeg___lt' ) )
		s.append(    'D ; JGE' )

		s.append( self.label( 'xIsNeg___lt' ) )
		s.append(    self.atTemp( 2 ) )
		s.append(    'D = M' )                                     # y

		s.append(    self.at( 'xIsNeg_and_yIsNeg___lt' ) )
		s.append(    'D ; JLT' )

		s.append( self.label( 'xIsNeg_and_yIsNotNeg___lt' ) )      # <--- return
		s.append(    'D = - 1' )                                   # true
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'xIsNotNeg___lt' ) )
		s.append(    self.atTemp( 2 ) )
		s.append(    'D = M' )                                     # y

		s.append(    self.at( 'xIsNotNeg_and_yIsNotNeg___lt' ) )
		s.append(    'D ; JGE' )

		s.append( self.label( 'xIsNotNeg_and_yisNeg___lt' ) )      # <--- return
		s.append(    'D = 0' )                                     # false
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'xIsNeg_and_yIsNeg___lt' ) )
		s.append( self.label( 'xIsNotNeg_and_yIsNotNeg___lt' ) )
		# D = Y
		s.append(    self.atTemp( 1 ) )
		s.append(    'D = M - D' )                                 # x - y

		s.append(    self.at( 'dIsNotNeg___lt' ) )
		s.append(    'D ; JGE' )

		s.append( self.label( 'dIsNeg___lt' ) )                    # <--- return
		s.append(    'D = - 1' )                                   # true
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'dIsNotNeg___lt' ) )                 # <--- return
		s.append(    'D = 0' )                                     # false
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )


		# ___ Lte ______________________________________________________________

		# Create label
		s.append( self.label( '$_genericComparisonOpLte' ) )

		s.append(    self.at( 'xIsNotNeg___lte' ) )
		s.append(    'D ; JGE' )

		s.append( self.label( 'xIsNeg___lte' ) )
		s.append(    self.atTemp( 2 ) )
		s.append(    'D = M' )                                      # y

		s.append(    self.at( 'xIsNeg_and_yIsNeg___lte' ) )
		s.append(    'D ; JLT' )

		s.append( self.label( 'xIsNeg_and_yIsNotNeg___lte' ) )      # <--- return
		s.append(    'D = - 1' )                                    # true
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'xIsNotNeg___lte' ) )
		s.append(    self.atTemp( 2 ) )
		s.append(    'D = M' )                                      # y

		s.append(    self.at( 'xIsNotNeg_and_yIsNotNeg___lte' ) )
		s.append(    'D ; JGE' )

		s.append( self.label( 'xIsNotNeg_and_yisNeg___lte' ) )      # <--- return
		s.append(    'D = 0' )                                      # false
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'xIsNeg_and_yIsNeg___lte' ) )
		s.append( self.label( 'xIsNotNeg_and_yIsNotNeg___lte' ) )
		# D = Y
		s.append(    self.atTemp( 1 ) )
		s.append(    'D = M - D' )                                  # x - y

		s.append(    self.at( 'dIsNotNeg___lte' ) )
		s.append(    'D ; JGE' )

		s.append( self.label( 'dIsNeg___lte' ) )                    # <--- return
		s.append(    'D = - 1' )                                    # true
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'dIsNotNeg___lte' ) )
		s.append(    self.at( 'dIsNotNeg_and_dIsNotZero___lte' ) )
		s.append(    'D ; JNE' )

		s.append( self.label( 'dIsNotNeg_and_dIsZero___lte' ) )     # <--- return
		s.append(    'D = - 1' )                                    # true
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )

		s.append( self.label( 'dIsNotNeg_and_dIsNotZero___lte' ) )  # <--- return
		s.append(    'D = 0' )                                      # false
		s.append(    self.at( 'genericComparisonOp_return' ) )
		s.append(    '0 ; JMP' )


		# ___ Return ___________________________________________________________

		# Jump to saved return position
		s.append( self.label( 'genericComparisonOp_return' ) )
		s.append( self.atTemp( 3 ) )
		s.append( 'A = M' )
		s.append( '0 ; JMP' )


		return self.a2s( s )


	def compile_label( self, loc ):

		return self.label( '{}.{}'.format( self.curFunctionName, loc ) )


	def compile_goto( self, loc ):

		s = []

		s.append( self.at( '{}.{}'.format( self.curFunctionName, loc ) ) )
		s.append( '0 ; JMP' )

		return self.a2s( s )


	def compile_ifgoto_( self, loc ):

		s = []

		# Jump only when cond != 0 i.e. when true
		s.append( self.at( '{}.{}'.format( self.curFunctionName, loc ) ) )
		s.append( 'D ; JNE' )

		return self.a2s( s )


	def compile_ifgoto( self, loc ):

		s = []

		# Condition
		s.append( self.popStackToD() )

		# Conditional jump
		s.append( self.compile_ifgoto_( loc ) )

		return self.a2s( s )


	def compile_call( self, fxName, nArgs ):

		if self.useGenerics:

			return self.compile_call_generic( fxName, nArgs )

		else:

			return self.compile_call_inline( fxName, nArgs )


	def compile_call_inline( self, fxName, nArgs ):

		s = []

		returnPos = 'returnPosition{}'.format( self.returnPosCount )
		self.returnPosCount += 1

		# Save return position
		s.append( self.at( returnPos ) )
		s.append( 'D = A' )
		s.append( self.pushDToStack() )	

		# Save segment pointers
		for ptr in [ 'LCL', 'ARG', 'THIS', 'THAT' ]:

			# get current val
			s.append( self.at( ptr ) )
			s.append( 'D = M' )

			# push to stack
			s.append( self.pushDToStack() )

		# Set ARG
		#  ARG = SP - ( nArgs + 5 )
		s.append( self.at( nArgs + 5 ) )
		s.append( 'D = A' )
		s.append( '@SP' )
		s.append( 'D = M - D' )
		s.append( '@ARG' )
		s.append( 'M = D' )

		# Set LCL
		s.append( '@SP' )
		s.append( 'D = M' )
		s.append( '@LCL' )
		s.append( 'M = D' )

		# Goto function
		s.append( self.at( fxName ) )
		s.append( '0 ; JMP' )

		# Create label for return position
		s.append( self.label( returnPos ) )

		return self.a2s( s )


	def compile_call_generic( self, fxName, nArgs ):

		s = []

		# Save fx position at R14
		s.append( self.at( fxName ) )
		s.append( 'D = A' )
		s.append( self.atGP( 1 ) )
		s.append( 'M = D' )

		# Save nArgs at R15
		s.append( self.at( nArgs ) )
		s.append( 'D = A' )
		s.append( self.atGP( 2 ) )
		s.append( 'M = D' )

		# Save return position
		returnPos = '$_returnFromGenericFunction{}'.format( self.returnGenericPosCount )
		self.returnGenericPosCount += 1

		s.append( self.at( returnPos ) )
		s.append( 'D = A' )

		# Goto genericCall function
		s.append( self.at( '$_genericCall' ) )
		s.append( '0 ; JMP' )

		# Create label for return position
		s.append( self.label( returnPos ) )

		return self.a2s( s )


	def compile_call_bootstrap( self ):

		s = []

		# Create label
		s.append( self.label( '$_genericCall' ) )
		
		# Save return position
		s.append( self.pushDToStack() )	

		# Save segment pointers
		for ptr in [ 'LCL', 'ARG', 'THIS', 'THAT' ]:

			# get current val
			s.append( self.at( ptr ) )
			s.append( 'D = M' )

			# push to stack
			s.append( self.pushDToStack() )

		# Set ARG
		#  ARG = SP - ( nArgs + 5 )
		s.append( self.atGP( 2 ) )  # get nArgs from R15
		s.append( 'D = M' )
		s.append( self.at( 5 ) )
		s.append( 'D = D + A' )  # nArgs + 5
		s.append( '@SP' )
		s.append( 'D = M - D' )
		s.append( '@ARG' )
		s.append( 'M = D' )

		# Set LCL
		s.append( '@SP' )
		s.append( 'D = M' )
		s.append( '@LCL' )
		s.append( 'M = D' )

		# Goto function
		s.append( self.atGP( 1 ) )  # get fx position from R14
		s.append( 'A = M' )
		s.append( '0 ; JMP' )

		return self.a2s( s )


	def compile_function( self, fxName, nLocals ):

		s = []

		self.curFunctionName = fxName

		# Create label
		s.append( self.label( fxName ) )

		# Init locals to zeros
		if nLocals == 1:
			s.append( '@SP' )
			s.append( 'A = M' )
			s.append( 'M = 0' )
			s.append( '@SP' )
			s.append( 'M = M + 1' )

		elif nLocals > 1:

			s.append( '@SP' )
			s.append( 'A = M' )
			s.append( 'M = 0' )

			for i in range( nLocals - 1 ):
				s.append( '@SP' )

				# s.append( 'AM = M + 1' )
				s.append( 'D = M + 1' )
				s.append( 'M = D' )
				s.append( 'A = D' )

				s.append( 'M = 0' )

			s.append( '@SP' )
			s.append( 'M = M + 1' )

		return self.a2s( s )


	def compile_return( self ):

		if self.useGenerics:

			return self.compile_return_generic()

		else:

			return self.compile_return_inline()


	def compile_return_inline( self ):

		s = []

		curLCL = 'curLCL_' + self.curFunctionName

		# Save current LCL
		s.append( '@LCL' )
		s.append( 'D = M' )
		s.append( self.at( curLCL ) )
		s.append( 'M = D' )

		# Save return address, @(curLCL - 5)
		s.append( self.at( 5 ) )
		s.append( 'A = D - A' )
		s.append( 'D = M' )
		s.append( self.atGP( 0 ) )
		s.append( 'M = D' )

		# Copy return value onto arg0
		s.append( '@SP' )
		s.append( 'A = M - 1' )
		s.append( 'D = M' )
		s.append( '@ARG' )
		s.append( 'A = M' )
		s.append( 'M = D' )

		# Reposition SP for caller (to just after return value)
		s.append( '@ARG' )
		s.append( 'D = M' )
		s.append( '@SP' )
		s.append( 'M = D + 1' )

		# Restore segment pointers of caller
		s.append( self.at( curLCL ) )
		s.append( 'A = M - 1' )
		s.append( 'D = M' )
		s.append( '@THAT' )
		s.append( 'M = D' )

		segs = [ None, None, 'THIS', 'ARG', 'LCL' ]
		for i in range( 2, 5 ):
			s.append( self.at( i ) )
			s.append( 'D = A' )
			s.append( self.at( curLCL ) )
			s.append( 'A = M - D' )
			s.append( 'D = M' )
			s.append( self.at( segs[i] ) )
			s.append( 'M = D' )

		# Jump to return position
		s.append( self.atGP( 0 ) )
		s.append( 'A = M' )
		s.append( '0 ; JMP' )

		return self.a2s( s )


	def compile_return_generic( self ):

		s = []

		# Goto genericReturn function
		s.append( self.at( '$_genericReturn' ) )
		s.append( '0 ; JMP' )

		return self.a2s( s )


	def compile_return_bootstrap( self ):

		s = []

		curLCL = 'curLCL'

		# Create label
		s.append( self.label( '$_genericReturn' ) )

		# Save current LCL
		s.append( '@LCL' )
		s.append( 'D = M' )
		s.append( self.at( curLCL ) )
		s.append( 'M = D' )

		# Save return address, @(curLCL - 5)
		s.append( self.at( 5 ) )
		s.append( 'A = D - A' )
		s.append( 'D = M' )
		s.append( self.atGP( 0 ) )
		s.append( 'M = D' )

		# Copy return value onto arg0
		s.append( '@SP' )
		s.append( 'A = M - 1' )
		s.append( 'D = M' )
		s.append( '@ARG' )
		s.append( 'A = M' )
		s.append( 'M = D' )

		# Reposition SP for caller (to just after return value)
		s.append( '@ARG' )
		s.append( 'D = M' )
		s.append( '@SP' )
		s.append( 'M = D + 1' )

		# Restore segment pointers of caller
		#  s.append( 'A = D - 1' )
		s.append( self.at( curLCL ) )
		s.append( 'A = M - 1' )
		s.append( 'D = M' )
		s.append( '@THAT' )
		s.append( 'M = D' )

		segs = [ None, None, 'THIS', 'ARG', 'LCL' ]
		for i in range( 2, 5 ):
			s.append( self.at( i ) )
			s.append( 'D = A' )
			s.append( self.at( curLCL ) )
			s.append( 'A = M - D' )
			s.append( 'D = M' )
			s.append( self.at( segs[i] ) )
			s.append( 'M = D' )

		# Jump to return position
		s.append( self.atGP( 0 ) )
		s.append( 'A = M' )
		s.append( '0 ; JMP' )

		return self.a2s( s )



	# Bootstrap ---------------------------------------

	def compile_bootstrap( self ):

		# Present in every asm file generated

		s = []	

		# Setup pointers
		if self.debug:

			s.append( '// --- Begin pointer setup' )
			s.append( '\n// set SP' )

		s.append( self.at( self.SP ) )
		s.append( 'D = A' )
		s.append( '@SP' )
		s.append( 'M = D' )

		if self.debug:

			s.append( '\n// set LCL' )

		s.append( '@LCL' )
		s.append( 'M = D' )

		if self.debug:

			s.append( '\n// set ARG' )

		s.append( '@ARG' )
		s.append( 'M = D' )

		if self.debug:

			s.append( '\n// set THIS' )

		s.append( self.at( 9999 ) )  # arbitrary
		s.append( 'D = A' )
		s.append( '@THIS' )
		s.append( 'M = D' )

		if self.debug:

			s.append( '\n// set THAT' )

		s.append( '@THAT' )
		s.append( 'M = D' )

		if self.debug:

			s.append( '\n// --- end pointer setup\n' )


		# Insert call to Sys.init
		if self.debug:

			s.append( '\n// --- Call Sys.init()' )

		s.append( '@Sys.init' )
		s.append( '0 ; JMP' )

		if self.debug:

			s.append( '' )


		# Insert generic functions
		#  Generate often used and generic code once.
		#  Based on @cadet1620's idea and code
		#  http://nand2tetris-questions-and-answers-forum.32033.n3.nabble.com/What-is-a-reasonable-amount-of-assembly-code-to-implement-gt-lt-eq-td4030839.html	
		if self.useGenerics:

			if self.debug:

				s.append( '\n// --- Begin generic functions' )
				s.append( '\n// genericReturn' )

			s.append( self.compile_return_bootstrap() )

			if self.debug: 

				s.append( '\n// genericCall' )

			s.append( self.compile_call_bootstrap() )

			if self.debug:

				s.append( '\n// genericComparisonOp' )

			s.append( self.compile_comparisonOp2_bootstrap() )

			if self.debug: 

				s.append( '\n// --- end generic functions\n' )


		return self.a2s( s )



	# Optimizations -----------------------------------

	# TODO maybe, tradeoff is complexity



# -- Run ------------------------------------------

def genASMFile_single( inputFilePath, outputFilePath, debug = False ):

	compiler = Compiler()  # init compiler

	fileName = inputFilePath.split( '/' )[ - 1 ]

	className = fileName[ : - 3 ]

	vmCode = { className : [] }

	# Read
	with open( inputFilePath, 'r' ) as file:

		for line in file:

			cmd = extractCmd( line )

			if cmd:

				vmCode[ className ].append( cmd )

	# Translate
	asmCode = compiler.compile( vmCode, debug )

	# Write
	with open( outputFilePath, 'w' ) as file:

		file.write( asmCode )
		file.write( '\n' )

	print( 'Done' )


def getVMFilesFromDir( dirPath ):

	fileNames = os.listdir( dirPath )

	filePaths = []

	for fileName in fileNames:

		if fileName[ -2 : ] == 'vm':

			filePath = dirPath + '/' + fileName

			filePaths.append( filePath )

	return filePaths


def genASMFile( inputDirPath, debug = False, libraryPaths = None ):

	''' Translate the vm code in a directory to assembly code,
	     and generate a single outputFile containing the translated code '''

	# Init compiler
	compiler = Compiler()

	# Get input file paths
	inputFilePaths = getVMFilesFromDir( inputDirPath )

	if libraryPaths:

		inputFilePaths.extend( libraryPaths )

	# Read
	vmCode = {}

	for inputFilePath in inputFilePaths:

		className = re.search( '\w+(?=\.vm)', inputFilePath ).group( 0 )

		if className in vmCode:

			raise Exception( 'Error: More than one class is named {}\n\t{}\n'.format(

				className,
				'\n\t'.join( inputFilePaths )
			) )

		print( ' - Translating {}'.format( inputFilePath ) )		

		vmCode[ className ] = []

		with open( inputFilePath, 'r' ) as file:
			
			for line in file:

				cmd = extractCmd( line )

				if cmd:

					vmCode[ className ].append( cmd )

	# Translate
	asmCode = compiler.compile( vmCode, debug )

	# Write
	outputFilePath = inputDirPath + '/Main.asm'

	with open( outputFilePath, 'w' ) as file:

		file.write( asmCode )
		file.write( '\n' )

	# print( 'Done' )


# inputFilePath = ''
# outputFilePath = ''
# genASMFile_single( inputFilePath, outputFilePath )

# inputDirPath = ''
# genASMFile( inputDirPath )
