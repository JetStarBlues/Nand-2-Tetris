''''''''''''''''''''''''' imports '''''''''''''''''''''''''''

# Built ins
import re

# Hack computer
from Components._0__globalConstants import *


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''


### --- Lookup tables ------------------------------

lookup_globalLabels = {

	'SP'     : '@SP',
	'LCL'    : '@LCL',
	'ARG'    : '@ARG',
	'THIS'   : '@THIS',
	'THAT'   : '@THAT',
	'TEMP'   : '@TEMP',
	'GP'     : '@GP',
	'STATIC' : '@STATIC',
	'STACK'  : '@STACK',
	'HEAP'   : '@HEAP',
}

'''
add
sub
neg
eq
gt
lt
and
or
not

pop
push

local
static
temp
this
argument
that
constant

goto
if-goto
function
call
return

'''


### --- Extraction ---------------------------------


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



### --- Translation ---------------------------------

