# == Imports =================================================

# Built ins
import re


# == Helpers =================================================



# == Main ====================================================


D = *P   // D = RAM[ address pointed to by q ]
	
	@p
	A = M
	D = M

p--     // address pointed to by q -= 1

	@p
	M = M - 1

p -= a
	
	@A
	D = M
	@p
	M = M - D

*q = 9  // RAM[ address pointed to by q ] = 9

	@9
	D = A
	@q
	A = M
	M = D




segmentPointer = {
	
	'argument' : '@ARG',
	'local'    : '@LCL',
	'this'     : '@THIS',
	'that'     : '@THAT',
	'temp'     : '@TEMP',
	'static'   : '@STATIC',
}

# action, seg, offset = cmd.split( ' ' )

def a2s( a ):

	# Return newline delimited string
	return '\n'.join( a ) + '\n'

def atConstant( x ):

	return '@' + str( x )

def atStatic( index ):

	return '@{}.{}'.format( curClassName, index )


def compile_push( seg, index ):

	s = []

	# Get value from segment
	if seg == 'constant':

		s.append( atConstant( index ) )
		s.append( 'D = A' )
	
	elif seg == 'pointer':

		if index == 0: s.append( '@THIS' )
		else:          s.append( '@THAT' )

		s.append( 'D = M' )

	elif seg == 'static':

		s.append( atStatic( index ) )
		s.append( 'D = M' )

	else:  # arg, local, this, that, temp

		s.append( atConstant( index ) )
		s.append( 'D = A' )
		s.append( segmentPointer[ seg ] )
		s.append( 'A = M + D' )
		s.append( 'D = M' )

	# Push it to stack
	s.append( '@SP' )
	s.append( 'A = M' )  # set A reg to address held by SP
	s.append( 'M = D' )  # set value at said address

	# Increment address held by SP
	s.append( '@SP' )
	s.append( 'M = M + 1' )

	return a2s( s )


def compile_pop( seg, index ):

	s = []

	if seg == 'pointer' or seg == 'static':

		# Decrement address held by SP
		s.append( '@SP' )
		s.append( 'AM = M - 1' )  # set A reg and memory value simultaneously

		# Get value from stack
		s.append( 'D = M' )

		# Get target address
		if seg == 'pointer':

			if index == 0: s.append( '@THIS' )
			else:          s.append( '@THAT' )

		else:

			s.append( atStatic( index ) )

		# Pop value to target address
		s.append( 'M = D' )

	else:  # arg, local, this, that, temp

		# Get target address
		s.append( atConstant( index ) )
		s.append( 'D = A' )
		s.append( segmentPointer[ seg ] )
		s.append( 'D = M + D' )

		# Save address to TEMP
		s.append( '@TEMP' )
		s.append( 'M = D' )

		# Decrement address held by SP
		s.append( '@SP' )
		s.append( 'AM = M - 1' )  # set A reg and memory value simultaneously

		# Get value from stack
		s.append( 'D = M' )

		# Pop value to target address
		s.append( '@TEMP' )
		s.append( 'A = M' )
		s.append( 'M = D' )

	return a2s( s )


def compile_arithmetic( cmd ):

	# For +/- 1 ... write direct VM code if doable ex. M = M + 1

	'''
		12            12             12
		7    sub ->   4    neg ->    -4
		3             SP             SP
		SP
	'''

	if cmd == 'eq' : pass
	elif cmd == 'gt' : pass
	elif cmd == 'lt' : pass
	elif cmd == 'gte' : pass
	elif cmd == 'lte' : pass
	elif cmd == 'ne' : pass

	elif cmd == 'and' : pass
	elif cmd == 'or' : pass
	elif cmd == 'not' :

		s = []

		s.append( '@SP' )
		s.append( 'A = M - 1' )
		s.append( 'M = ! M' )

		return a2s( s )


	elif cmd == 'xor' : pass

		'@SP'
		'M = M - 1'  # prev addr
		
		'@SP'
		'A = M - 1'  # prevprev addr
		'D = M'      # prevprev val

		'@SP'
		'A = M'      # prev addr
		'M = D ^ M'  # prevprev val op prev val
###
		'@SP'
		'AM = M - 1'  # prev addr
		'D = M'       # prev val
		
		'@SP'
		'A = M - 1'  # prevprev addr
		'D = M '     # prevprev val

		'@SP'
		'A = M'      # prev addr
		'M = D ^ M'  # prevprev val op prev val


	elif cmd == 'add' : pass
	elif cmd == 'sub' : pass

	elif cmd == 'neg' :

		s = []

		s.append( '@SP' )
		s.append( 'A = M - 1' )
		s.append( 'M = - M' )

		return a2s( s )

	elif cmd == 'shiftR' : pass
	elif cmd == 'shiftL' : pass

def compile_label(): pass
def compile_goto(): pass
def compile_ifgoto():

	# Jump only when cond != 0 i.e. when true
	s += 'cond ; JNE'

	pass
def compile_function(): pass
def compile_call(): pass
def compile_return():

	# Save current LCL

	# Get return address

	pass



# -- Lookup tables ---------------------------------

lookup_globalAddresses = {

	'@SCREEN' : '@' + str( SCREEN_MEMORY_MAP ),
	'@KBD'    : '@' + str( KBD_MEMORY_MAP ),

	'@R0'     : '@0',   # SP
	'@R1'     : '@1',   # ARG
	'@R2'     : '@2',   # LCL
	'@R3'     : '@3',   # THIS
	'@R4'     : '@4',   # THAT
	'@R5'     : '@5',   # TEMP
	'@R6'     : '@6',   # TEMP
	'@R7'     : '@7',   # TEMP
	'@R8'     : '@8',   # TEMP
	'@R9'     : '@9',   # TEMP
	'@R10'    : '@10',  # TEMP
	'@R11'    : '@11',  # TEMP
	'@R12'    : '@12',  # TEMP
	'@R13'    : '@13',  # GP
	'@R14'    : '@14',  # GP
	'@R15'    : '@15',  # GP

	'@SP'     : '@0',
	'@LCL'    : '@1',
	'@ARG'    : '@2',
	'@THIS'   : '@3',
	'@THAT'   : '@4',
	'@TEMP'   : '@5',
	'@GP'     : '@13',
	'@STATIC' : '@16',
	# '@STACK'  : '@256',
	# '@HEAP'   : '@2048',
}



# -- Extraction -------------------------------------


# select everything that is not a comment
cmdPattern = '''
	^   		# from beginning of string
	[^\/]   	# that does not start with a comment
	.*?  		# select all characters until,
	(?=\/\/|$)  # reach start of a comment or the string's end
'''
cmdPattern = re.compile( cmdPattern, re.X )


def extractCmd( line ):
	
	''' Extract symbolic command from line of source code '''

	line = line.replace(' ', '')   # remove whitespaces
	line = line.replace('\t', '')  # remove tabs
	line = line.upper()            # upper case everything

	found = re.search( cmdPattern, line ) 	# select everything that is not a comment

	if found != None:
		return found.group(0)
	else:
		return None


def extractCmds( inputFile ):

	''' Extract symbolic commands from source code '''

	commands = []

	with open( inputFile, encoding='utf-8' ) as input_file:
		
		for a_line in input_file:

			a_line = a_line.rstrip()   # remove trailing whitespace and carriage return

			cmd_symbolic = extractCmd( a_line )

			if cmd_symbolic:
				commands.append( cmd_symbolic )

	return commands



# -- Translation -------------------------------------


def handle_Labels( cmdList ):

	''' Replace labels with integer addresses '''

	trimmedCmdList = []

	knownAddresses_ROM = {}

	for i in range( len( cmdList ) ):

		if cmdList[i][0] == '(':

			label = cmdList[i][1:-1]    # get the label

			ROM_addr = i - len( knownAddresses_ROM)    # and the corresponding ROM address

			knownAddresses_ROM[ '@' + label ] = '@' + str( ROM_addr )   # add it to dict of knownAddresses_ROM

		else:

			trimmedCmdList.append( cmdList[i] )   # not a label so include it


	return( trimmedCmdList, knownAddresses_ROM )


def handle_Variables( cmdList, knownAddresses_ROM ):

	''' Replace variable names with integer addresses '''

	freeAddress = 16  # 16..255 (static)

	knownAddresses_RAM = {}
	knownAddresses_RAM.update( lookup_globalAddresses )  # fill with global addresses
	

	for i in range( len( cmdList ) ):

		if cmdList[i][0] == '@':

			# Is the address an integer? ---

			try:
				int( cmdList[i][1:] )
			

			except ValueError:

				# No? Must be a variable.			
			
				# Check known variables ---

				try:
					cmdList[i] = knownAddresses_ROM[ cmdList[i] ]

				except KeyError:

					try:
						cmdList[i] = knownAddresses_RAM[ cmdList[i] ]


					# Otherwise, create a new address ---	
					
					except KeyError:					
					

						newAddr = '@' + str( freeAddress )          # create new address

						knownAddresses_RAM[ cmdList[i] ] = newAddr  # add it to dict of knownAddresses_RAM

						cmdList[i] = newAddr                        # and set it

						freeAddress += 1 	# register is no longer unallocated


	return cmdList


def translate_Instructions( cmdList ):

	''' Translate symbolic instructions to binary '''

	for i in range( len( cmdList ) ):

		#
		cmd_s = cmdList[i]
		cmd_b = None


		# A instruction
		if cmd_s[0] == '@':

			opcode = '0'
			addr = int( cmd_s[1:] )
			addr = _toBinary( N_BITS - 1, addr )
			cmd_b = opcode + addr


		# C instruction
		else:
			
			opcode = '1'
			nUnusedBits = ( N_BITS - 16 )  # 16 bits used to encode opcode(1), dest(3), comp( 2 + 1 + 6 ), jmp(3)
			header = opcode + '1' * nUnusedBits
			
			dest, comp, jmp = [None] * 3

			if '=' in cmd_s and ';' in cmd_s:
				dest, comp, jmp = re.split( '=|;', cmd_s )

			elif '=' in cmd_s:
				dest, comp = re.split( '=', cmd_s )

			elif ';' in cmd_s:
				comp, jmp = re.split( ';', cmd_s )

			# print(dest, comp, jmp)

			dest = lookup_dest[dest] if dest else lookup_dest['NULL']
			jmp = lookup_jmp[jmp] if jmp else lookup_jmp['NULL']
			comp = lookup_comp[comp]

			cmd_b = header + comp + dest + jmp


		#
		cmdList[i] = cmd_b


	return cmdList


def translateCmds( cmdList ):

	''' Translate symbolic commands to binary '''

	cmdList = handle_Labels( cmdList )
	cmdList = handle_Variables( cmdList[0], cmdList[1] )
	binCmdList = translate_Instructions( cmdList )

	return binCmdList



# -- Output --------------------------------------


def writeToOutputFile( binCmdList, outputFile ):

	''' generate an output file containing the binary commands '''

	with open( outputFile, mode='w', encoding='utf-8' ) as output_file:

			firstLine = True # workaround to avoid extra blank line at end of output file, http://stackoverflow.com/a/18139440
			
			for cmd_binary in binCmdList:
					
				if firstLine: firstLine = False
				else: output_file.write( '\n' )

				output_file.write( cmd_binary )



# -- Run ------------------------------------------


def asm_to_bin( inputFile, outputFile ):

	''' Translate the symbolic code in inputFile to binary code,
	     and generate an outputFile containing the translated code '''

	cmds_symbolic = extractCmds( inputFile )
	cmds_binary = translateCmds( cmds_symbolic )
	writeToOutputFile( cmds_binary, outputFile )
