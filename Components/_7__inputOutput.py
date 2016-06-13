''''''''''''''''''''''''' imports '''''''''''''''''''''''''''

# Built ins
import tkinter, threading

# Hack computer
from ._x__components import *



''''''''''''''''''''''''' I/O '''''''''''''''''''''''''''

class IO():

	''' Input and output devices.
		 Currently consists of screen and keyboard.
	'''

	def __init__( self, N, main_memory ):

		# General ---
		self.N = N
		self.main_memory = main_memory


		# Initialize IO devices ---
		self.screen = Screen( self.main_memory )
		self.keyboard = Keyboard( self.N, self.main_memory )


		# Initialize tkinter ---
		self.refreshRate = SCREEN_REFRESH_RATE  # ms
		self.root = None
		self.img = None

		threading.Thread( 
			target = self._initTkinter,
			name = 'screen_thread'
		).start()


	def update( self ):

		self.screen.update()

		self._updateTkinterImg( self.screen.data )


	def _initTkinter( self ):

		self.root = tkinter.Tk()
		self.root.wm_title('Hack')
		self.root.iconbitmap('Components/favicon.ico')
		
		self.root.bind( '<KeyPress>', self._handleKeyPress )
		self.root.bind( '<KeyRelease>', self._handleKeyRelease )

		self.img = tkinter.PhotoImage( width = self.screen.width, height = self.screen.height )

		label = tkinter.Label(self.root)
		label.pack()
		label.config( image = self.img )

		self.update()

		self.root.mainloop()


	def _handleKeyPress( self, ev = None ):

		if ev.keysym == 'Escape':
			self._quitTkinter()

		else:
			self.keyboard.handleKeyPress( ev.keysym )


	def _handleKeyRelease( self, ev = None ):

		self.keyboard.handleKeyRelease()


	def _updateTkinterImg( self, data ):

		self.img.put( data, to = (0, 0, self.screen.width, self.screen.height) )

		self.root.after( self.refreshRate, self.update )  # set timer


	def _quitTkinter( self, ev = None ):

		self.root.quit()



''''''''''''''''''''''''' screen '''''''''''''''''''''''''''


class Screen():

	'''
		16 bit screen with a 512 x 256 pixels display.
		Specifications hardcoded for simplicity.

		Data stored using a 256 x 512 array to help with tkinter draw speed
		(In lieu of using a 1 x 8192 array which more closely resembles RAM).
	'''

	def __init__( self, main_memory ):
		
		# General
		self.N = 16
		self.nRegisters = 8192
		self.main_memory = main_memory

		# Dimensions
		self.width = 512
		self.height = 256		
		self.registersPerRow = self.width // self.N

		# Colors
		self.bgColor = SCREEN_BACKGROUND_COLOR + ' '
		self.fgColor = SCREEN_FOREGROUND_COLOR + ' '

		# Pixel array
		self.pixels = [ [0] * self.width for _ in range( self.height ) ]

		# Tkinter string
		self.data = None


	def update( self ):

		# Get screen data from Hack's main memory ---
		self.readMainMemory()


		# Format pixel array to tkinter string ---
		data = [ '{' + ''.join( map( str, row ) ) + '} ' for row in self.pixels ]
		data = ''.join( data )

		self.data = data.replace( '0', self.bgColor ).replace( '1', self.fgColor )


	def readMainMemory( self ):

		# Get screen data from Hack's main memory

		for address in range( self.nRegisters ):
			
			data = self.main_memory.read( SCREEN_MEMORY_MAP + address )

			self.write( data, address )


	def write( self, x, address ):

		# Psuedo N bit RAM interface ---
		#  Maps RAM access style to pixel array access style

		row = address // self.registersPerRow
		col_0 = address % self.registersPerRow * self.N

		for col, bit in zip( range( col_0, col_0 + self.N ), range( 0, self.N ) ):
			self.pixels[row][col] = x[bit]



''''''''''''''''''''''''' keyboard '''''''''''''''''''''''''''


class Keyboard():

	''' N bit keyboard '''

	def __init__( self, N, main_memory ):

		self.main_memory = main_memory

		self.N = N

		self.keySym = None


	def handleKeyPress( self, keySym ):

		# print( keySym )

		self.keySym = keySym

		self.write()


	def handleKeyRelease( self ):

		self.keySym = 'null_key'

		self.write()


	def write( self ):

		'''
			Bypasses I/O interrupt handling by CPU as the keyboard
			 writes directly to main_memory. In the physical implementation,
			 only the CPU would have access to main_memory requiring the use
			 of interrupt handling logic.

			See, www.cs.umd.edu/class/sum2003/cmsc311/Notes/IO/extInt.html
		'''

		keyCode = lookup_keyboard[ self.keySym ][0]   # decimal

		keyCode = bin( keyCode )[2:].zfill( self.N )  # binary

		self.main_memory.write( 1, keyCode, 1, KBD_MEMORY_MAP )  # clk, x, write, address

		# print( self.main_memory.read( KBD_MEMORY_MAP ) )


'''
	Tkinter keysyms retrieved from, 
	  www.tcl.tk/man/tcl8.5/TkCmd/keysyms.htm
'''

lookup_keyboard = {

	# Tkinter_keySym : [ Hack_keyCode, character ],
	     'null_key' : [   0 ,         None ],
	        'space' : [  32 ,          ' ' ],
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
	          'Tab' : [ 127 ,         None ],
	       'Return' : [ 128 ,         None ],  # Enter
	    'BackSpace' : [ 129 ,         None ],
	         'Left' : [ 130 ,         None ],
	           'Up' : [ 131 ,         None ],
	        'Right' : [ 132 ,         None ],
	         'Down' : [ 133 ,         None ],
	         'Home' : [ 134 ,         None ],
	          'End' : [ 135 ,         None ],
	        'Prior' : [ 136 ,         None ],  # Page up
	         'Next' : [ 137 ,         None ],  # Page down
	       'Insert' : [ 138 ,         None ],
	       'Delete' : [ 139 ,         None ],
	       'Escape' : [ 140 ,         None ],
	           'F1' : [ 141 ,         None ],
	           'F2' : [ 142 ,         None ],
	           'F3' : [ 143 ,         None ],
	           'F4' : [ 144 ,         None ],
	           'F5' : [ 145 ,         None ],
	           'F6' : [ 146 ,         None ],
	           'F7' : [ 147 ,         None ],
	           'F8' : [ 148 ,         None ],
	           'F9' : [ 149 ,         None ],
	          'F10' : [ 150 ,         None ],
	          'F11' : [ 151 ,         None ],
	          'F12' : [ 152 ,         None ],
	      'Shift_L' : [ 153 ,         None ],
	      'Shift_R' : [ 154 ,         None ],
	    'Control_L' : [ 155 ,         None ],
	    'Control_R' : [ 156 ,         None ],
	        'Alt_L' : [ 157 ,         None ],
	        'Alt_R' : [ 158 ,         None ],	      	      
}
