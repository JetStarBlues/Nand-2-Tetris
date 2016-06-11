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

	# Tkinter_keySym : [ Hack_keyCode, key ]
	
	        'space' : [  32 ,      'space' ],
	       'exclam' : [  33 ,          '!' ],
	     'quotedbl' : [  34 ,          '"' ],
	   'numbersign' : [  35 ,          '#' ],
	       'dollar' : [  36 ,          '$' ],
	      'percent' : [  37 ,          '%' ],
	    'ampersand' : [  38 ,          '&' ],
	   'quoteright' : [  39 ,          "'" ],
	    'parenleft' : [  40 ,          '(' ],
	   'parenright' : [  41 ,          ')' ],
	     'asterisk' : [  42 ,          '*' ],
	         'plus' : [  43 ,          '+' ],
	        'comma' : [  44 ,          ',' ],
	        'minus' : [  45 ,          '-' ],
	       'period' : [  46 ,          '.' ],
	        'slash' : [  47 ,          '/' ],
	            '0' : [  48 ,          '0' ],
	            '1' : [  49 ,          '1' ],
	            '2' : [  50 ,          '2' ],
	            '3' : [  51 ,          '3' ],
	            '4' : [  52 ,          '4' ],
	            '5' : [  53 ,          '5' ],
	            '6' : [  54 ,          '6' ],
	            '7' : [  55 ,          '7' ],
	            '8' : [  56 ,          '8' ],
	            '9' : [  57 ,          '9' ],
	        'colon' : [  58 ,          ':' ],
	    'semicolon' : [  59 ,          ';' ],
	         'less' : [  60 ,          '<' ],
	        'equal' : [  61 ,          '=' ],
	      'greater' : [  62 ,          '>' ],
	     'question' : [  63 ,          '?' ],
	           'at' : [  64 ,          '@' ],
	            'A' : [  65 ,          'A' ],
	            'B' : [  66 ,          'B' ],
	            'C' : [  67 ,          'C' ],
	            'D' : [  68 ,          'D' ],
	            'E' : [  69 ,          'E' ],
	            'F' : [  70 ,          'F' ],
	            'G' : [  71 ,          'G' ],
	            'H' : [  72 ,          'H' ],
	            'I' : [  73 ,          'I' ],
	            'J' : [  74 ,          'J' ],
	            'K' : [  75 ,          'K' ],
	            'L' : [  76 ,          'L' ],
	            'M' : [  77 ,          'M' ],
	            'N' : [  78 ,          'N' ],
	            'O' : [  79 ,          'O' ],
	            'P' : [  80 ,          'P' ],
	            'Q' : [  81 ,          'Q' ],
	            'R' : [  82 ,          'R' ],
	            'S' : [  83 ,          'S' ],
	            'T' : [  84 ,          'T' ],
	            'U' : [  85 ,          'U' ],
	            'V' : [  86 ,          'V' ],
	            'W' : [  87 ,          'W' ],
	            'X' : [  88 ,          'X' ],
	            'Y' : [  89 ,          'Y' ],
	            'Z' : [  90 ,          'Z' ],
	  'bracketleft' : [  91 ,          '[' ],
	    'backslash' : [  92 ,         '\\' ],
	 'bracketright' : [  93 ,          ']' ],
	  'asciicircum' : [  94 ,          '^' ],
	   'underscore' : [  95 ,          '_' ],
	    'quoteleft' : [  96 ,          '`' ],
	            'a' : [  97 ,          'a' ],
	            'b' : [  98 ,          'b' ],
	            'c' : [  99 ,          'c' ],
	            'd' : [ 100 ,          'd' ],
	            'e' : [ 101 ,          'e' ],
	            'f' : [ 102 ,          'f' ],
	            'g' : [ 103 ,          'g' ],
	            'h' : [ 104 ,          'h' ],
	            'i' : [ 105 ,          'i' ],
	            'j' : [ 106 ,          'j' ],
	            'k' : [ 107 ,          'k' ],
	            'l' : [ 108 ,          'l' ],
	            'm' : [ 109 ,          'm' ],
	            'n' : [ 110 ,          'n' ],
	            'o' : [ 111 ,          'o' ],
	            'p' : [ 112 ,          'p' ],
	            'q' : [ 113 ,          'q' ],
	            'r' : [ 114 ,          'r' ],
	            's' : [ 115 ,          's' ],
	            't' : [ 116 ,          't' ],
	            'u' : [ 117 ,          'u' ],
	            'v' : [ 118 ,          'v' ],
	            'w' : [ 119 ,          'w' ],
	            'x' : [ 120 ,          'x' ],
	            'y' : [ 121 ,          'y' ],
	            'z' : [ 122 ,          'z' ],
	    'braceleft' : [ 123 ,          '{' ],
	          'bar' : [ 124 ,          '|' ],
	   'braceright' : [ 125 ,          '}' ],
	   'asciitilde' : [ 126 ,          '~' ],
	          'Tab' : [ 127 ,        'tab' ],
	       'Return' : [ 128 ,    'newline' ],
	    'BackSpace' : [ 129 ,  'backspace' ],
	         'Left' : [ 130 ,  'leftArrow' ],
	           'Up' : [ 131 ,    'upArrow' ],
	        'Right' : [ 132 , 'rightArrow' ],
	         'Down' : [ 133 ,  'downArrow' ],
	         'Home' : [ 134 ,       'home' ],
	          'End' : [ 135 ,        'end' ],
	        'Prior' : [ 136 ,     'pageUp' ],
	         'Next' : [ 137 ,   'pageDown' ],
	       'Insert' : [ 138 ,        'ins' ],
	       'Delete' : [ 139 ,        'dlt' ],
	       'Escape' : [ 140 ,        'esc' ],
	           'F1' : [ 141 ,         'f1' ],
	           'F2' : [ 142 ,         'f2' ],
	           'F3' : [ 143 ,         'f3' ],
	           'F4' : [ 144 ,         'f4' ],
	           'F5' : [ 145 ,         'f5' ],
	           'F6' : [ 146 ,         'f6' ],
	           'F7' : [ 147 ,         'f7' ],
	           'F8' : [ 148 ,         'f8' ],
	           'F9' : [ 149 ,         'f9' ],
	          'F10' : [ 150 ,        'f10' ],
	          'F11' : [ 151 ,        'f11' ],
	          'F12' : [ 152 ,        'f12' ],
}
