''' Read/write data from/to memory using integer representation instead of binary'''

'''----------------------------- Imports -----------------------------'''

# Built ins
import threading
import pygame, numpy
from math import ceil

# Hack computer
from ._x__components import *



'''------------------------------- I/O -------------------------------'''

class IO():

	''' Input and output devices '''

	''' Currently consists of,
	      input: keyboard, mouse
	      ouput: screen
	'''

	'''
	    Input devices bypass I/O interrupt handling by CPU as they
	     write directly to main_memory. In the physical implementation,
	     only the CPU would have access to main_memory requiring the use
	     of interrupt handling logic.

	    See, www.cs.umd.edu/class/sum2003/cmsc311/Notes/IO/extInt.html
	'''

	def __init__( self, N, main_memory ):

		# General ---
		self.N = N
		self.main_memory = main_memory
		self.hasExited = False

		# Pygame ---
		self.maxFps = SCREEN_FPS
		self.display = None
		self.clock = None

		# Screen ---
		self.width = 512
		self.height = 256
		self.screenMemStart = SCREEN_MEMORY_MAP
		self.newContent = False

		# 1Bit color mode ---
		self.fgColor = self.hex2rgb( SCREEN_FOREGROUND_COLOR )
		self.bgColor = self.hex2rgb( SCREEN_BACKGROUND_COLOR )
		self.colors = {

			'0' : self.bgColor,
			'1' : self.fgColor
		}
		self.nRegistersPerRow = self.width // self.N
		self.nPixelsPerWord = self.N
		self.screenMemEnd = self.screenMemStart + self.height * self.nRegistersPerRow;

		# 4Bit color mode ---
		if COLOR_MODE_4BIT:

			self.colors = {}

			for key, value in COLOR_PALETTE_4BIT.items():

				self.colors[ key ] = self.hex2rgb( value )

			self.fgColor = self.colors[ '0111' ]
			self.bgColor = self.colors[ '0000' ]

			self.nRegistersPerRow *= 4
			self.nPixelsPerWord = 4
			self.screenMemEnd = self.screenMemStart + self.height * self.nRegistersPerRow;

		# Pixel array ---
		# Pygame 'blit_array' expects a numpy array with [x][y] indexing (i.e. [column][row])
		self.pixelArray = numpy.full( ( self.width, self.height, 3 ), self.bgColor )   # np( nCols, nRows, z )
		self.curColor = self.fgColor

		# Initialize Pygame ---
		# threading.Thread(
		# 	target = self.initPygame,
		# 	name = 'io_thread'
		# ).start()

	def hex2rgb( self, h ):

		r = int( h[ -6 : -4 ], 16 )
		g = int( h[ -4 : -2 ], 16 )
		b = int( h[ -2 :    ], 16 )

		return( r, g, b )

	def toBinary( self, x, fill ):

		# convert representation from integer to binary
		return bin( x )[ 2 : ].zfill( fill )

	def runAsThread( self ):

		threading.Thread(

			target = self.initPygame,
			name = 'io_thread'

		).start()

	def initPygame( self ):

		pygame.init()

		pygame.display.set_caption( 'Hack Computer' )

		icon = pygame.image.load( 'Components/favicon.png' )
		pygame.display.set_icon( icon )

		pygame.display.set_mode( ( self.width, self.height ) )

		self.surface = pygame.display.get_surface()

		self.clock = pygame.time.Clock()

		# Start loop
		self.run()

	def quitPygame( self ):

		pygame.quit()

		self.hasExited = True

		print( 'Exited Pygame' )

	def run( self ):

		while not self.hasExited:

			# Poll input devices (mouse, keyboard)
			for event in pygame.event.get():

				if event.type == pygame.QUIT:  # click X

					self.quitPygame()

					return

				if event.type == pygame.KEYDOWN:

					if event.key == 27:  # Escape

						self.quitPygame()

						return

					else:

						modifier = pygame.key.get_mods()

						self.handleKeyPressed( event.key, modifier )

				if event.type == pygame.KEYUP:

					self.handleKeyReleased()

				if event.type == pygame.MOUSEBUTTONDOWN:

					self.handleMousePressed( event.button, event.pos )

				if event.type == pygame.MOUSEBUTTONUP:

					self.handleMouseReleased( event.button )

			# Update screen
			self.updateScreen()

			# Tick
			self.clock.tick( self.maxFps )


	# Screen ----------------------------------------------------

	def updateScreen( self ):

		if self.newContent:  # update only if there's a change

			# Blit pixel values
			pygame.surfarray.blit_array( self.surface, self.pixelArray )

			# Update display
			pygame.display.flip()

			self.newContent = False

	def updateScreen_partial( self, x, y, w, h ):

		# Hmmm.... also why crashes when close?

		# Blit pixel values
		pygame.surfarray.blit_array( self.surface, self.pixelArray )

		# Update display
		pygame.display.update( pygame.Rect( x, y, w, h ) )	

	def setColor( self, colorCode ):

		if COLOR_MODE_4BIT:

			key = self.toBinary( colorCode, 4 )

			if not key in self.colors:

				raise Exception( 'Color selection is not valid' )

			self.curColor = self.colors[ key ] # temp

		else:

			key = str( colorCode )

			if not key in self.colors:

				raise Exception( 'Color selection is not valid - {}'.format( colorCode ) )

			self.curColor = self.colors[ key ] # temp

	def drawPixel( self, x, y ):

		''' Update only the relevant pixel '''

		# Check if coordinates are valid
		if( x < 0 or x >= self.width or y < 0 or y >= self.height ):

			raise Exception( 'drawPixel received invalid argument(s): ( {}, {} )'.format( x, y ) )

		# Draw pixel
		self.pixelArray[ x ][ y ] = self.curColor

		# Mark screen for update
		self.newContent = True

	def flood( self, x, y, len ):

		# Write words to display RAM
		# Assumes display RAM allocates one register per pixel

		for i in range( len ):

			self.pixelArray[ x ][ y ] = self.curColor

			x += 1

			if ( x == self.width ):

				x = 0
				y += 1

	def drawFastVLine( self, x, y, h ):

		# I can easily make this fast for numpy array, but what would be hardware equivalent?
		pass

	def drawFastHLine( self, x, y, w ):

		# Check if coordinates are valid
		if(
			w <= 0 or 
			x <  0 or ( x + w ) > self.width or
			y <  0 or         y > self.height
		):
			raise Exception( 'drawFastHLine received invalid argument(s): ( {}, {}, {} )'.format( x, y, w ) )

		# Draw line
		self.flood( x, y, w )

		# Mark screen for update
		self.newContent = True

	def fillScreen( self ):

		self.flood( 0, 0, self.width * self.height )

		# Mark screen for update
		self.newContent = True

	def getPixel( self, x, y ):

		# Check if coordinates are valid
		if(
			x < 0 or x >= self.width or
			y < 0 or y >= self.height
		):
			raise Exception( 'getPixel received invalid argument(s): ( {}, {} )'.format( x, y ) )

		# Get color
		color = self.pixelArray[ x ][ y ]

		# Lookup colorCode
		for key, value in self.colors.items():

			if value == color:

				colorCode = key

		# Write to memory
		self.main_memory.write( 1, colorCode, 1, SCREEN_MEMORY_MAP )  # TODO, get better location


	def replaceMainWithDisplayMemory( self, x, y, w, h ):

		#TODO
		pass


	def replaceDisplayWithMainMemory( self, x, y, w, h ):

		# TODO - make this faster...

		# Check if coordinates are valid
		if(
			w <= 0 or
			h <= 0 or
			x <  0 or ( x + w ) > self.width or
			y <  0 or ( y + h ) > self.height
		):
			raise Exception( 'replaceDisplayWithMainMemory received invalid argument(s): ( {}, {}, {}, {} )'.format( x, y, w, h ) )

		# Replace
		if( w == self.width and h == self.height ):

			if COLOR_MODE_4BIT:

				self.getPixelsFromMain_4BitMode_fast( x, y, w, h )

			else:

				self.getPixelsFromMain_1BitMode_fast( x, y, w, h )

		else:

			if COLOR_MODE_4BIT:

				self.getPixelsFromMain_4BitMode( x, y, w, h )

			else:

				self.getPixelsFromMain_1BitMode( x, y, w, h )

		# Mark screen for update
		self.newContent = True

		# Hmmm...
		# self.updateScreen_partial( x, y, w, h )

	def getPixelsFromMain_1BitMode( self, x, y, w, h ):

		# Slow cause iterating per pixel?

		x0 = x
		x2 = x + w

		for y in range( y, y + h ):

			x = x0

			regIdx_ = self.screenMemStart + ( y * self.nRegistersPerRow )  # exp comp

			while x < x2:

				regIdx = regIdx_ + ( x // self.nPixelsPerWord )  # exp comp

				register = self.main_memory.read( regIdx )

				register = self.toBinary( register, self.N )

				for i in range( x % self.N, self.N ):  # exp comp

					pixel = register[ i ]

					color = self.colors[ pixel ]  # look up corresponding color

					self.pixelArray[ x ][ y ] = color

					x += 1

					if x == x2:

						break

	def getPixelsFromMain_1BitMode_fast( self ):

		x = 0
		y = 0

		for regIdx in range( self.screenMemStart, self.screenMemEnd ):

			register = self.main_memory.read( regIdx )

			register = self.toBinary( register, self.N )

			for i in range( self.N ):

				pixel = register[ i ]

				color = self.colors[ pixel ]  # look up corresponding color

				self.pixelArray[ x ][ y ] = color

				x += 1

				if ( x == self.width ):

					x = 0
					y += 1

	def getPixelsFromMain_4BitMode( self, x, y, w, h ):

		# TODO, and test!
		pass

	def getPixelsFromMain_4BitMode_fast( self ):

		x = 0
		y = 0

		for idx in range( self.screenMemStart, self.screenMemEnd ):

			register = self.main_memory.read( idx )

			register = self.toBinary( register, self.N )

			for i in range( 0, self.N, 4 ):

				pixel = register[ i : i + 4 ]

				color = self.colors[ pixel ]  # look up corresponding color

				self.pixelArray[ x ][ y ] = color

				x += 1

				if ( x == self.width ):

					x = 0
					y += 1


	# ------

	def updateScreen_old( self ):

		# Blit pixel values
		pygame.surfarray.blit_array( self.surface, self.genPixelArray() )

		# Update display
		pygame.display.flip()

	def genPixelArray( self ):

		if COLOR_MODE_4BIT:

			return self.convertToBlitArray( self.getPixels_4BitMode() )

		else:

			return self.convertToBlitArray( self.getPixels_1BitMode() )
			
	def convertToBlitArray( self, a ):

		''' Pygame 'blit_array' expects a numpy array with [x][y] indexing (i.e. [column][row]) '''
		
		# return numpy.transpose( numpy.array( a ), ( 1, 0, 2 ) )

		return numpy.array( a ).reshape( ( self.height, self.width, 3 ) ).transpose( ( 1, 0, 2 ) )

	def getPixels_1BitMode_old( self ):

		pixels = []

		# for y in range( self.height ):

		# 	row = []

		# 	for x in range( self.nRegistersPerRow ):

		# 		idx = x + y * self.nRegistersPerRow

		# 		register = self.main_memory.read( SCREEN_MEMORY_MAP + idx )

		# 		register = self.toBinary( register, self.N )

		# 		for i in range( self.N ):

		# 			pixel = register[ i ]

		# 			color = self.colors[ pixel ]  # look up corresponding color

		# 			row.append( color )

		# 	pixels.append( row )


		for idx in range( self.screenMemStart, self.screenMemEnd ):

			register = self.main_memory.read( idx )

			register = self.toBinary( register, self.N )

			for i in range( self.N ):

				pixel = register[ i ]

				color = self.colors[ pixel ]  # look up corresponding color

				pixels.append( color )		

		return pixels

	def getPixels_4BitMode_old( self ):

		pixels = []

		# for y in range( self.height ):

		# 	row = []

		# 	for x in range( self.nRegistersPerRow ):

		# 		idx = x + y * self.nRegistersPerRow

		# 		register = self.main_memory.read( SCREEN_MEMORY_MAP + idx )

		# 		register = self.toBinary( register, self.N )

		# 		for i in range( 0, self.N, 4 ):

		# 			pixel = register[ i : i + 4 ]

		# 			color = self.colors[ pixel ]  # look up corresponding color

		# 			row.append( color )

		# 	pixels.append( row )


		for idx in range( self.screenMemStart, self.screenMemEnd ):

			register = self.main_memory.read( idx )

			register = self.toBinary( register, self.N )

			for i in range( 0, self.N, 4 ):

				pixel = register[ i : i + 4 ]

				color = self.colors[ pixel ]  # look up corresponding color

				pixels.append( color )

		return pixels


	# Mouse -----------------------------------------------------

	def handleMousePressed( self, button, pos ):

		''' If mouse button is pressed, write 1 and update mouseX and mouseY '''

		# print( 'Mouse pressed', pos )

		if button == 1:  # left button

			# Write to memory
			#  clk, data, write, address
			self.main_memory.write( 1,        1, 1,  MOUSE_MEMORY_MAP )
			self.main_memory.write( 1, pos[ 0 ], 1, MOUSEX_MEMORY_MAP )
			self.main_memory.write( 1, pos[ 1 ], 1, MOUSEY_MEMORY_MAP )

	def handleMouseReleased( self, button ):

		''' If mouse button is released, write 0 '''

		# if button == 1:  # left button

		# 	# Write to memory
		# 	self.main_memory.write( 1, 0, 1, MOUSE_MEMORY_MAP )

		pass  # Too fast, cleared long before Hack program has chance to see


	# Keyboard --------------------------------------------------

	def handleKeyPressed( self, key, modifier ):

		''' If key is pressed, write keyCode '''

		# Lookup keyCode
		keyCode = self.lookupKey( key, modifier )

		print( 'Key pressed', key, modifier, keyCode )

		# Write to memory
		self.main_memory.write( 1, keyCode, 1, KBD_MEMORY_MAP )

	def handleKeyReleased( self ):

		''' If key is released, write 0 '''

		# Write to memory
		# self.main_memory.write( 1, 0, 1,  KBD_MEMORY_MAP )

		pass  # Too fast, cleared long before Hack program has chance to see

	def lookupKey( self, key, modifier ):

		# If valid, return relevant keyCode
		if key in lookup_keys:

			# Handle shift modified presses
			if modifier == 3 :

				if key in lookup_shiftModifiedKeys:

					return lookup_shiftModifiedKeys[ key ][ 0 ]

				else:

					'''
						Ideally shift modifer would be 0 when shift key pressed alone.
						However not the case. Sometimes it's 0 sometimes it's set (1 or 2).
						Not sure how to work around. For now, ignoring all shift key presses
						where shift modifier is set.
						TLDR, shift key will not register consistently unless used as a modifier
					'''
					return 0

			# Handle caps_lock modified presses
			elif modifier == 8192:

				if key in range( 97, 123 ):  # is a letter

					return lookup_shiftModifiedKeys[ key ][ 0 ]

				else:

					return lookup_keys[ key ][ 0 ]

			else:

				return lookup_keys[ key ][ 0 ]	

		else:

			return 0



'''
    Pygame keyConstants
      www.pygame.org/docs/ref/key.html
'''

lookup_keyModifiers = [

	0,     # None
	1,     # Shift_left
	2,     # Shift_right
	3,     # Shift
	8192,  # Caps
	64,    # Ctrl_left
	128,   # Ctrl_right
	192,   # Ctrl
	256,   # Alt_left
	512,   # Alt_right
	768,   # Alt
	# 1024,  # Meta_left
	# 2048,  # Meta_right
	# 3072,  # Meta
	# 4096,  # Num
	# 16384, # Mode
]

lookup_keys = {

	# Pygame_keyConstant : [ Hack_keyCode, ASCII_character ]
	 32 : [  32 , ' '  ],  # Space
	 39 : [  39 , "'"  ],  # Quote right
	 44 : [  44 , ','  ],  # Comma
	 45 : [  45 , '-'  ],  # Minus
	 46 : [  46 , '.'  ],  # Period
	 47 : [  47 , '/'  ],  # Slash
	 48 : [  48 , '0'  ],
	 49 : [  49 , '1'  ],
	 50 : [  50 , '2'  ],
	 51 : [  51 , '3'  ],
	 52 : [  52 , '4'  ],
	 53 : [  53 , '5'  ],
	 54 : [  54 , '6'  ],
	 55 : [  55 , '7'  ],
	 56 : [  56 , '8'  ],
	 57 : [  57 , '9'  ],
	 59 : [  59 , ';'  ],  # Semicolon
	 61 : [  61 , '='  ],  # Equal
	 91 : [  91 , '['  ],  # Bracket left
	 92 : [  92 , '\\' ],  # Backslash
	 93 : [  93 , ']'  ],  # Bracket right
	 96 : [  96 , '`'  ],  # Quote left
	 97 : [  97 , 'a'  ],
	 98 : [  98 , 'b'  ],
	 99 : [  99 , 'c'  ],
	100 : [ 100 , 'd'  ],
	101 : [ 101 , 'e'  ],
	102 : [ 102 , 'f'  ],
	103 : [ 103 , 'g'  ],
	104 : [ 104 , 'h'  ],
	105 : [ 105 , 'i'  ],
	106 : [ 106 , 'j'  ],
	107 : [ 107 , 'k'  ],
	108 : [ 108 , 'l'  ],
	109 : [ 109 , 'm'  ],
	110 : [ 110 , 'n'  ],
	111 : [ 111 , 'o'  ],
	112 : [ 112 , 'p'  ],
	113 : [ 113 , 'q'  ],
	114 : [ 114 , 'r'  ],
	115 : [ 115 , 's'  ],
	116 : [ 116 , 't'  ],
	117 : [ 117 , 'u'  ],
	118 : [ 118 , 'v'  ],
	119 : [ 119 , 'w'  ],
	120 : [ 120 , 'x'  ],
	121 : [ 121 , 'y'  ],
	122 : [ 122 , 'z'  ],
	  9 : [ 127 , None ],  # Tab
	 13 : [ 128 , None ],  # Enter
	  8 : [ 129 , None ],  # Backspace
	276 : [ 130 , None ],  # Arrow left
	273 : [ 131 , None ],  # Arraw up
	275 : [ 132 , None ],  # Arrow right
	274 : [ 133 , None ],  # Arrow down
	278 : [ 134 , None ],  # Home
	279 : [ 135 , None ],  # End
	280 : [ 136 , None ],  # Page up
	281 : [ 137 , None ],  # Page down
	277 : [ 138 , None ],  # Insert
	127 : [ 139 , None ],  # Delete
	 27 : [ 140 , None ],  # Escape
	282 : [ 141 , None ],  # F1
	283 : [ 142 , None ],  # F2
	284 : [ 143 , None ],  # F3
	285 : [ 144 , None ],  # F4
	286 : [ 145 , None ],  # F5
	287 : [ 146 , None ],  # F6
	288 : [ 147 , None ],  # F7
	289 : [ 148 , None ],  # F8
	290 : [ 149 , None ],  # F9
	291 : [ 150 , None ],  # F10
	292 : [ 151 , None ],  # F11
	293 : [ 152 , None ],  # F12
	304 : [ 153 , None ],  # Shift left
	303 : [ 154 , None ],  # Shift right
	306 : [ 155 , None ],  # Control left
	305 : [ 156 , None ],  # Control right
	308 : [ 157 , None ],  # Alt left
	307 : [ 158 , None ],  # Alt right

	268 : [  42 , '*'  ],  # keypad asterisk
	270 : [  43 , '+'  ],  # keypad plus
	269 : [  45 , '-'  ],  # keypad minus
	266 : [  46 , '.'  ],  # keypad period
	267 : [  47 , '/'  ],  # keypad slash
	256 : [  48 , '0'  ],  # keypad 0
	257 : [  49 , '1'  ],  # keypad 1
	258 : [  50 , '2'  ],  # keypad 2
	259 : [  51 , '3'  ],  # keypad 3
	260 : [  52 , '4'  ],  # keypad 4
	261 : [  53 , '5'  ],  # keypad 5
	262 : [  54 , '6'  ],  # keypad 6
	263 : [  55 , '7'  ],  # keypad 7
	264 : [  56 , '8'  ],  # keypad 8
	265 : [  57 , '9'  ],  # keypad 9
	271 : [ 128 , None ],  # keypad enter
}

lookup_shiftModifiedKeys = {

	# Pygame_keyConstant : [ Hack_keyCode, ASCII_character ]
	 49 : [  33 , '!' ],  # Exclamation,       S + 1
	 39 : [  34 , '"' ],  # Quote double,      S + Quote right
	 51 : [  35 , '#' ],  # Number sign,       S + 3
	 52 : [  36 , '$' ],  # Dollar,            S + 4
	 53 : [  37 , '%' ],  # Percent,           S + 5
	 55 : [  38 , '&' ],  # Ampersand,         S + 7
	 57 : [  40 , '(' ],  # Parenthesis left,  S + 9
	 48 : [  41 , ')' ],  # Parenthesis right, S + 0
	 56 : [  42 , '*' ],  # Asterisk,          S + 8
	 61 : [  43 , '+' ],  # Plus,              S + Equal
	 59 : [  58 , ':' ],  # Colon,             S + Semicolon
	 44 : [  60 , '<' ],  # Less,              S + Comma
	 46 : [  62 , '>' ],  # Greater,           S + Period
	 47 : [  63 , '?' ],  # Question,          S + Slash
	 50 : [  64 , '@' ],  # At,                S + 2
	 97 : [  65 , 'A' ],
	 98 : [  66 , 'B' ],
	 99 : [  67 , 'C' ],
	100 : [  68 , 'D' ],
	101 : [  69 , 'E' ],
	102 : [  70 , 'F' ],
	103 : [  71 , 'G' ],
	104 : [  72 , 'H' ],
	105 : [  73 , 'I' ],
	106 : [  74 , 'J' ],
	107 : [  75 , 'K' ],
	108 : [  76 , 'L' ],
	109 : [  77 , 'M' ],
	110 : [  78 , 'N' ],
	111 : [  79 , 'O' ],
	112 : [  80 , 'P' ],
	113 : [  81 , 'Q' ],
	114 : [  82 , 'R' ],
	115 : [  83 , 'S' ],
	116 : [  84 , 'T' ],
	117 : [  85 , 'U' ],
	118 : [  86 , 'V' ],
	119 : [  87 , 'W' ],
	120 : [  88 , 'X' ],
	121 : [  89 , 'Y' ],
	122 : [  90 , 'Z' ],
	 54 : [  94 , '^' ],  # Caret,             S + 6
	 45 : [  95 , '_' ],  # Underscore,        S + Minus
	 91 : [ 123 , '{' ],  # Brace left,        S + Bracket left
	 92 : [ 124 , '|' ],  # Bar,               S + Backslash
	 93 : [ 125 , '}' ],  # Brace right,       S + Bracket right
	 96 : [ 126 , '~' ],  # Tilde,             S + Quote left
}
