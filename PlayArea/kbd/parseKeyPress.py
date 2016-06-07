''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''


''''''''''''''''''''''''' helpers '''''''''''''''''''''''''

def toString(array):
	return ''.join( map(str, array) )

def toDecimal(bitSeq):
	return int(bitSeq, 2)

def toBinary(N, x):
	return bin(x)[2:].zfill(N)


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

has_quit = False

def getInput():
	user_input = input()
	parseCmd( user_input )


def parseCmd( cmd ):
	
	cmd = cmd.split() # assume args seperated by spaces

	if cmd[0] == 'quit': 
		quit()

	elif cmd[0] == 'add':
		add( cmd[1], cmd[2] )

	elif cmd[0] == 'hello':
		hello()

	else:
		print('n/a')

	#
	if not has_quit: getInput()


def quit():
	global has_quit
	has_quit = True

def hello():
	print("hi there")

def add(a, b):
	sum_ = float(a) + float(b)
	print( sum_ )


##
# getInput()


# http://www.tcl.tk/man/tcl8.5/TkCmd/keysyms.htm

lookup_kbd = {

	# [ key, tkinter_keyCode, Hack_keyCode, python_keyCode]
	
	     'space' ,         'space' ,   32 ,
	         '!' ,        'exclam' ,   33 ,
	         '"' ,      'quotedbl' ,   34 ,
	         '#' ,    'numbersign' ,   35 ,
	         '$' ,        'dollar' ,   36 ,
	         '%' ,       'percent' ,   37 ,
	         '&' ,     'ampersand' ,   38 ,
	         "'" ,    'quoteright' ,   39 ,
	         '(' ,     'parenleft' ,   40 ,
	         ')' ,    'parenright' ,   41 ,
	         '*' ,      'asterisk' ,   42 ,
	         '+' ,          'plus' ,   43 ,
	         ',' ,         'comma' ,   44 ,
	         '-' ,         'minus' ,   45 ,
	         '.' ,        'period' ,   46 ,
	         '/' ,         'slash' ,   47 ,
	         '0' ,             '0' ,   48 ,
	         '1' ,             '1' ,   49 ,
	         '2' ,             '2' ,   50 ,
	         '3' ,             '3' ,   51 ,
	         '4' ,             '4' ,   52 ,
	         '5' ,             '5' ,   53 ,
	         '6' ,             '6' ,   54 ,
	         '7' ,             '7' ,   55 ,
	         '8' ,             '8' ,   56 ,
	         '9' ,             '9' ,   57 ,
	         ':' ,         'colon' ,   58 ,
	         ';' ,     'semicolon' ,   59 ,
	         '<' ,          'less' ,   60 ,
	         '=' ,         'equal' ,   61 ,
	         '>' ,       'greater' ,   62 ,
	         '?' ,      'question' ,   63 ,
	         '@' ,            'at' ,   64 ,
	         'A' ,             'A' ,   65 ,
	         'B' ,             'B' ,   66 ,
	         'C' ,             'C' ,   67 ,
	         'D' ,             'D' ,   68 ,
	         'E' ,             'E' ,   69 ,
	         'F' ,             'F' ,   70 ,
	         'G' ,             'G' ,   71 ,
	         'H' ,             'H' ,   72 ,
	         'I' ,             'I' ,   73 ,
	         'J' ,             'J' ,   74 ,
	         'K' ,             'K' ,   75 ,
	         'L' ,             'L' ,   76 ,
	         'M' ,             'M' ,   77 ,
	         'N' ,             'N' ,   78 ,
	         'O' ,             'O' ,   79 ,
	         'P' ,             'P' ,   80 ,
	         'Q' ,             'Q' ,   81 ,
	         'R' ,             'R' ,   82 ,
	         'S' ,             'S' ,   83 ,
	         'T' ,             'T' ,   84 ,
	         'U' ,             'U' ,   85 ,
	         'V' ,             'V' ,   86 ,
	         'W' ,             'W' ,   87 ,
	         'X' ,             'X' ,   88 ,
	         'Y' ,             'Y' ,   89 ,
	         'Z' ,             'Z' ,   90 ,
	         '[' ,   'bracketleft' ,   91 ,
	         '/' ,     'backslash' ,   92 ,
	         ']' ,  'bracketright' ,   93 ,
	         '^' ,   'asciicircum' ,   94 ,
	         '_' ,    'underscore' ,   95 ,
	         '`' ,     'quoteleft' ,   96 ,
	         'a' ,             'a' ,   97 ,
	         'b' ,             'b' ,   98 ,
	         'c' ,             'c' ,   99 ,
	         'd' ,             'd' ,  100 ,
	         'e' ,             'e' ,  101 ,
	         'f' ,             'f' ,  102 ,
	         'g' ,             'g' ,  103 ,
	         'h' ,             'h' ,  104 ,
	         'i' ,             'i' ,  105 ,
	         'j' ,             'j' ,  106 ,
	         'k' ,             'k' ,  107 ,
	         'l' ,             'l' ,  108 ,
	         'm' ,             'm' ,  109 ,
	         'n' ,             'n' ,  110 ,
	         'o' ,             'o' ,  111 ,
	         'p' ,             'p' ,  112 ,
	         'q' ,             'q' ,  113 ,
	         'r' ,             'r' ,  114 ,
	         's' ,             's' ,  115 ,
	         't' ,             't' ,  116 ,
	         'u' ,             'u' ,  117 ,
	         'v' ,             'v' ,  118 ,
	         'w' ,             'w' ,  119 ,
	         'x' ,             'x' ,  120 ,
	         'y' ,             'y' ,  121 ,
	         'z' ,             'z' ,  122 ,
	         '{' ,     'braceleft' ,  123 ,
	         '|' ,           'bar' ,  124 ,
	         '}' ,    'braceright' ,  125 ,
	         '~' ,    'asciitilde' ,  126 ,
	       'tab' ,           'Tab' ,  127 ,
	   'newline' ,        'Return' ,  128 ,
	 'backspace' ,     'BackSpace' ,  129 ,
	 'leftArrow' ,          'Left' ,  130 ,
	   'upArrow' ,            'Up' ,  131 ,
	'rightArrow' ,         'Right' ,  132 ,
	 'downArrow' ,          'Down' ,  133 ,
	      'home' ,          'Home' ,  134 ,
	       'end' ,           'End' ,  135 ,
	    'pageUp' ,         'Prior' ,  136 ,
	  'pageDown' ,          'Next' ,  137 ,
	       'ins' ,        'Insert' ,  138 ,
	       'dlt' ,        'Delete' ,  139 ,
	       'esc' ,        'Escape' ,  140 ,
	        'f1' ,            'F1' ,  141 ,
	        'f2' ,            'F2' ,  142 ,
	        'f3' ,            'F3' ,  143 ,
	        'f4' ,            'F4' ,  144 ,
	        'f5' ,            'F5' ,  145 ,
	        'f6' ,            'F6' ,  146 ,
	        'f7' ,            'F7' ,  147 ,
	        'f8' ,            'F8' ,  148 ,
	        'f9' ,            'F9' ,  149 ,
	       'f10' ,           'F10' ,  150 ,
	       'f11' ,           'F11' ,  151 ,
	       'f12' ,           'F12' ,  152 ,
}
