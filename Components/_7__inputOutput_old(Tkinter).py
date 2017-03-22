'''----------------------------- Imports -----------------------------'''

# Built ins
import tkinter, threading

# Hack computer
from ._x__components import *



'''------------------------------- I/O -------------------------------'''

class IO():

	''' Input and output devices.
	     Currently consists of screen and keyboard.
	'''

	def __init__( self, N, main_memory ):

		# General ---
		self.N = N
		self.main_memory = main_memory
		self.hasExited = False


		# Initialize IO devices ---
		self.screen = Screen( self.main_memory )
		self.keyboard = Keyboard( self.N, self.main_memory )
		self.mouse = Mouse( self.N, self.main_memory )


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

		self._updateTkinterImg()


	def _initTkinter( self ):

		# general
		self.root = tkinter.Tk()
		self.root.wm_title('Hack')
		self.root.iconbitmap('Components/favicon.ico')
		
		# events
		self.root.bind( '<KeyPress>', self._handleKeyPress )
		self.root.bind( '<KeyRelease>', self._handleKeyRelease )
		self.root.bind( '<Button-1>', self._handleMouseClick )
		self.root.protocol( 'WM_DELETE_WINDOW', self._quitTkinter )  # when user closes window by clicking X

		# img stuff
		self.img = tkinter.PhotoImage( width = self.screen.width, height = self.screen.height )

		label = tkinter.Label(self.root)
		label.pack()
		label.config( image = self.img )

		# loop
		self.update()

		#
		self.root.mainloop()


	def _handleKeyPress( self, ev = None ):

		if ev.keysym == 'escape':
			self._quitTkinter()

		else:
			self.keyboard.handleKeyPress( ev.keysym )


	def _handleKeyRelease( self, ev = None ):

		self.keyboard.handleKeyRelease()


	def _handleMouseClick( self, ev = None ):

		self.mouse.handleMouseClick( ev.x, ev.y )


	def _updateTkinterImg( self ):

		self.img.put( self.screen.data, to = (0, 0, self.screen.width, self.screen.height) )

		self.root.after( self.refreshRate, self.update )  # set timer


	def _quitTkinter( self, ev = None ):

		self.root.quit()
		self.hasExited = True



'''----------------------------- Screen -----------------------------'''

class Screen():

	'''
	    16 bit screen with a 512 x 256 pixels display.
	    Specifications hardcoded for simplicity.
	'''

	def __init__( self, main_memory ):
		
		# General
		self.N = 16
		self.nRegisters = 8192
		self.main_memory = main_memory

		# Dimensions
		self.width = 512
		self.height = 256		
		self.nRegistersPerRow = self.width // self.N

		# 1Bit color mode (default)
		self.fgColor = SCREEN_FOREGROUND_COLOR + ' '
		self.bgColor = SCREEN_BACKGROUND_COLOR + ' '

		# 4Bit color mode
		if COLOR_MODE_4BIT:
			self.nRegisters *= 4
			self.nRegistersPerRow *= 4
			self.colors = COLOR_PALETTE_4BIT
			for key, value in self.colors.items():
				self.colors[key] = value + ' '

		# Pixel data.
		#  Formatted for Tkinter (see http://tkinter.unpythonic.net/wiki/PhotoImage)
		self.data = ''

	
	def update( self ):

		# Get screen data from Hack's main memory
		#  and update pixels accordingly

		if COLOR_MODE_4BIT:
			self.update_4BitMode()
		else:
			self.update_1BitMode()


	def update_1BitMode( self ):

		self.data = ''  # clear

		for y in range( self.height ):

			row = '{'

			for x in range( self.nRegistersPerRow ):

				idx = x + y * self.nRegistersPerRow

				register = self.main_memory.read( SCREEN_MEMORY_MAP + idx )

				for i in range( self.N ):
				
					pixel = register[ i ]

					color = self.get1BitColor( pixel )

					row += color

			row += '} '

			self.data += row


	def get1BitColor( self, colorCode ):

		if colorCode == 1 : return self.fgColor

		else: return self.bgColor


	def update_4BitMode( self ):

		self.data = ''  # clear

		for y in range( self.height ):

			row = '{'

			for x in range( self.nRegistersPerRow ):

				idx = x + y * self.nRegistersPerRow

				register = self.main_memory.read( SCREEN_MEMORY_MAP + idx )

				for i in range( 0, self.N, 4 ):
				
					pixel = register[ i : i + 4 ]

					color = self.get4BitColor( pixel )

					row += color

			row += '} '

			self.data += row


	def get4BitColor( self, colorCode ):

		colorCode = ''.join( map( str, colorCode ) )  # convert tuple to string
		return self.colors[ colorCode ]               # look up corresponding color



'''----------------------------- Keyboard -----------------------------'''

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

		self.main_memory.write( 1, keyCode, 1, KBD_MEMORY_MAP )  # clk, data, write, address

		# print( self.main_memory.read( KBD_MEMORY_MAP ) )


'''
	Tkinter keysyms retrieved from, 
	  www.tcl.tk/man/tcl8.5/TkCmd/keysyms.htm
'''

lookup_keyboard = {

	# Tkinter_keySym : [ Hack_keyCode, character ],
	     'null_key' : [   0 ,         None ],
	      'newline' : [  10 ,         None ],  # \n
   'carriageReturn' : [  13 ,         None ],  # \r
	        'space' : [  32 ,          ' ' ],
	       'exclam' : [  33 ,          '!' ],
	     'quotedbl' : [  34 ,          '"' ],
	   'numbersign' : [  35 ,          '#' ],
	       'dollar' : [  36 ,          '$' ],
	      'percent' : [  37 ,          '%' ],
	    'ampersand' : [  38 ,          '&' ],
	   'quoteright' : [  39 ,          "'" ],
	    'parenLeft' : [  40 ,          '(' ],
	   'parenRight' : [  41 ,          ')' ],
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
	  'bracketLeft' : [  91 ,          '[' ],
	    'backslash' : [  92 ,         '\\' ],
	 'bracketRight' : [  93 ,          ']' ],
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
	    'braceLeft' : [ 123 ,          '{' ],
	          'bar' : [ 124 ,          '|' ],
	   'braceRight' : [ 125 ,          '}' ],
	        'tilde' : [ 126 ,          '~' ],
	          'tab' : [ 127 ,         None ],
	       'return' : [ 128 ,         None ],  # Enter
	    'backSpace' : [ 129 ,         None ],
	         'left' : [ 130 ,         None ],
	           'up' : [ 131 ,         None ],
	        'right' : [ 132 ,         None ],
	         'down' : [ 133 ,         None ],
	         'home' : [ 134 ,         None ],
	          'end' : [ 135 ,         None ],
	        'prior' : [ 136 ,         None ],  # Page up
	         'next' : [ 137 ,         None ],  # Page down
	       'insert' : [ 138 ,         None ],
	       'delete' : [ 139 ,         None ],
	       'escape' : [ 140 ,         None ],
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
	    'shiftLeft' : [ 153 ,         None ],
	   'shiftRight' : [ 154 ,         None ],
	  'controlLeft' : [ 155 ,         None ],
	 'controlRight' : [ 156 ,         None ],
	      'altLeft' : [ 157 ,         None ],
	     'altRight' : [ 158 ,         None ],
}



'''------------------------------ Mouse ------------------------------'''

class Mouse():

	''' N bit mouse '''

	def __init__( self, N, main_memory ):

		self.main_memory = main_memory

		self.N = N

		self.keySym = None


	def handleMouseClick( self, mouseX, mouseY ):

		# print( "x", mouseX, " y", mouseY )

		self.write( mouseX, mouseY )


	def write( self, mouseX, mouseY ):

		'''
		    Bypasses I/O interrupt handling by CPU as the keyboard
		     writes directly to main_memory. In the physical implementation,
		     only the CPU would have access to main_memory requiring the use
		     of interrupt handling logic.

		    See, www.cs.umd.edu/class/sum2003/cmsc311/Notes/IO/extInt.html
		'''

		mouseX = bin( mouseX )[2:].zfill( self.N )  # binary
		mouseY = bin( mouseY )[2:].zfill( self.N )  # binary

		self.main_memory.write( 1, mouseX, 1, MOUSEX_MEMORY_MAP )  # clk, data, write, address
		self.main_memory.write( 1, mouseY, 1, MOUSEY_MEMORY_MAP )  # clk, data, write, address

		# print( self.main_memory.read( MOUSEX_MEMORY_MAP ) )
		# print( self.main_memory.read( MOUSEY_MEMORY_MAP ) )