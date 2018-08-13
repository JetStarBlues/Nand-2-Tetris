'''----------------------------- Imports -----------------------------'''

# Built ins
import threading
import pygame, numpy

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

		self.zeroN = self.intToBitArray( 0 )
		self.oneN  = self.intToBitArray( 1 )

		# Pygame ---
		self.maxFps = FPS
		self.surface = None
		self.clock = None

		# Screen ---
		self.width = 512
		self.height = 256

		# Memory map ---
		self.addrScreenCmd  = SCREEN_MEMORY_MAP + 0
		self.addrScreenArg0 = SCREEN_MEMORY_MAP + 1
		self.addrScreenArg1 = SCREEN_MEMORY_MAP + 2
		self.addrScreenArg2 = SCREEN_MEMORY_MAP + 3
		self.addrScreenArg3 = SCREEN_MEMORY_MAP + 4
		self.addrScreenArg4 = SCREEN_MEMORY_MAP + 5
		self.addrScreenArg5 = SCREEN_MEMORY_MAP + 6
		self.addrScreenArg6 = SCREEN_MEMORY_MAP + 7

		self.addrMouseP     = MOUSE_MEMORY_MAP + 0
		self.addrMouseX     = MOUSE_MEMORY_MAP + 1
		self.addrMouseY     = MOUSE_MEMORY_MAP + 2

		self.addrKeyP       = KEYBOARD_MEMORY_MAP + 0
		self.addrKeyCode    = KEYBOARD_MEMORY_MAP + 1

		# Commands ---
		self.cmds = [

			None,
			self.setColor,
			self.drawPixel,
			self.getPixel,
			self.fillScreen,
			self.drawFastVLine,
			self.drawFastHLine,
			self.fillRect,
			self.drawPixelBuffer,
			self.drawPixelBuffer4,
		]

		# Colors ---
		self.curColor = ( 0, 0, 0 )

		# 1Bit color
		self.colors_1 = {}

		for key, value in COLOR_PALETTE_1BIT.items():

			self.colors_1[ key ] = self.hex2rgb( value )

		self.nRegistersPerRow_1 = self.width // self.N
		self.nPixelsPerWord_1   = self.N
		self.nRegisters_1       = self.height * self.nRegistersPerRow_1;

		# 4Bit color
		self.colors_4 = {}

		for key, value in COLOR_PALETTE_4BIT.items():

			self.colors_4[ key ] = self.hex2rgb( value )

		self.nRegistersPerRow_4  = self.nRegistersPerRow_1 * 4
		self.nPixelsPerWord_4    = 4
		self.nRegisters_4        = self.height * self.nRegistersPerRow_4;

		# Pixel array ---
		''' Pygame 'blit_array' expects a numpy array with [x][y] indexing (i.e. [column][row])
		    np( nCols, nRows, z ) '''
		self.pixelArray = numpy.full( ( self.width, self.height, 3 ), self.curColor )

	def hex2rgb( self, h ):

		r = int( h[ - 6 : - 4 ], 16 )
		g = int( h[ - 4 : - 2 ], 16 )
		b = int( h[ - 2 :     ], 16 )

		return( r, g, b )

	def intToBitArray( self, x ):

		bStr = bin( x )[ 2 : ].zfill( self.N )

		return tuple( map( int, bStr ) )  # tuple of ints

	def bitArrayToBinaryString( self, x ):

		return ''.join( map( str, x ) )

	def bitArrayToInt( self, x ):

		return int( ''.join( map( str, x ) ), 2 )

	def runAsThread( self ):

		threading.Thread(

			target = self.initPygame,
			name = 'io_thread',
			daemon = False

		).start()

	def initPygame( self ):

		pygame.init()

		pygame.display.set_caption( 'Hack Computer' )

		icon = pygame.image.load( 'Components/favicon.png' )
		pygame.display.set_icon( icon )

		pygame.display.set_mode( ( self.width, self.height ) )

		self.surface = pygame.display.get_surface()

		self.clock = pygame.time.Clock()

		# Init background
		# self.surface.fill( bgColor )
		pygame.display.flip()

		# Start loop
		self.run()

	def quitPygame( self ):

		pygame.quit()

		self.hasExited = True

		print( 'Exited Pygame' )

	def run( self ):

		''' Infinte update loop.
		    Needed to keep Pygame alive. '''

		while not self.hasExited:

			# Poll input devices (mouse, keyboard)
			for event in pygame.event.get():

				# Gracefully handle exit
				if event.type == pygame.QUIT :  # clicked X

					self.quitPygame()

					return

				elif event.type == pygame.KEYDOWN:

					modifier = pygame.key.get_mods()

					self.handleKeyPressed( event.key, modifier )

				elif event.type == pygame.KEYUP:

					self.handleKeyReleased()

				elif event.type == pygame.MOUSEBUTTONDOWN:

					self.handleMousePressed( event.button, event.pos )

				elif event.type == pygame.MOUSEBUTTONUP:

					self.handleMouseReleased( event.button )

				elif event.type == pygame.MOUSEMOTION:

					self.handleMouseMoved( event.pos )

			# Update screen
			# self.updateScreen()

			# Tick
			#  FPS acts as delay (i.e. how often this loop is called)
			self.clock.tick( self.maxFps )
			# self.clock.tick()  # unbound


	# Screen ----------------------------------------------------

	def updateScreen( self ):

		# In hardware, this would be called on rising edge (of not zero)?

		cmd = self.main_memory.read( self.addrScreenCmd )

		if cmd != self.zeroN:

			cmd = self.bitArrayToInt( cmd )

			# print( 'Received screen cmd -', self.cmds[ cmd ].__name__ )

			# Execute command
			self.cmds[ cmd ]()

			# Blit pixel values
			pygame.surfarray.blit_array( self.surface, self.pixelArray )

			# Update display
			pygame.display.flip()

			# Mark completion
			self.main_memory.write( 1, self.zeroN, 1, self.addrScreenCmd )

	def setColor( self ):

		# Get args
		cPtr = self.main_memory.read( self.addrScreenArg0 )
		cPtr = self.bitArrayToInt( cPtr )

		r = self.main_memory.read( cPtr     )
		g = self.main_memory.read( cPtr + 1 )
		b = self.main_memory.read( cPtr + 2 )

		r = self.bitArrayToInt( r )
		g = self.bitArrayToInt( g )
		b = self.bitArrayToInt( b )

		# print( 'setColor( {}, {}, {} )'.format( r, g, b ) )

		# Set color
		self.curColor = ( r, g, b )

	def drawPixel( self ):

		''' Update only the relevant pixel '''

		# Get args
		x = self.main_memory.read( self.addrScreenArg0 )
		y = self.main_memory.read( self.addrScreenArg1 )

		x = self.bitArrayToInt( x )
		y = self.bitArrayToInt( y )

		# Check if coordinates are valid
		if(
			x < 0 or x >= self.width or
			y < 0 or y >= self.height
		):

			raise Exception( 'drawPixel received invalid argument(s): ( {}, {} )'.format( x, y ) )

		# Draw pixel
		self.pixelArray[ x ][ y ] = self.curColor
		# self.surface.set_at( ( x, y ), self.curColor )

	def getPixel( self ):

		# Get args
		x = self.main_memory.read( self.addrScreenArg0 )
		y = self.main_memory.read( self.addrScreenArg1 )

		x = self.bitArrayToInt( x )
		y = self.bitArrayToInt( y )

		# Check if coordinates are valid
		if(
			x < 0 or x >= self.width or
			y < 0 or y >= self.height
		):
			raise Exception( 'getPixel received invalid argument(s): ( {}, {} )'.format( x, y ) )

		# Get color
		color = self.pixelArray[ x ][ y ]

		# Write to memory
		self.main_memory.write( 1, self.intToBitArray( color[ 0 ] ), 1, self.addrScreenArg0 )
		self.main_memory.write( 1, self.intToBitArray( color[ 1 ] ), 1, self.addrScreenArg1 )
		self.main_memory.write( 1, self.intToBitArray( color[ 2 ] ), 1, self.addrScreenArg2 )

	def flood( self, x, y, n ):

		''' Write words to display RAM
		    Assumes display RAM allocates one register per pixel '''

		for i in range( n ):

			self.pixelArray[ x ][ y ] = self.curColor

			x += 1

			if ( x == self.width ):

				x = 0
				y += 1

	def drawFastVLine( self ):

		# Get args
		x = self.main_memory.read( self.addrScreenArg0 )
		y = self.main_memory.read( self.addrScreenArg1 )
		h = self.main_memory.read( self.addrScreenArg2 )

		x = self.bitArrayToInt( x )
		y = self.bitArrayToInt( y )
		h = self.bitArrayToInt( h )

		# Check if coordinates are valid
		if(
			h <= 0 or 
			x <  0 or         x >= self.width or
			y <  0 or ( y + h ) >  self.height
		):
			raise Exception( 'drawFastVLine received invalid argument(s): ( {}, {}, {} )'.format( x, y, h ) )

		# Draw line
		for y2 in range( y, y + h ):

			self.pixelArray[ x ][ y2 ] = self.curColor

	def drawFastHLine( self ):

		# Get args
		x = self.main_memory.read( self.addrScreenArg0 )
		y = self.main_memory.read( self.addrScreenArg1 )
		w = self.main_memory.read( self.addrScreenArg2 )

		x = self.bitArrayToInt( x )
		y = self.bitArrayToInt( y )
		w = self.bitArrayToInt( w )

		# Check if coordinates are valid
		if(
			w <= 0 or 
			x <  0 or ( x + w ) >  self.width or
			y <  0 or         y >= self.height
		):
			raise Exception( 'drawFastHLine received invalid argument(s): ( {}, {}, {} )'.format( x, y, w ) )

		# Draw line
		self.flood( x, y, w )

	def fillScreen( self ):

		self.flood( 0, 0, self.width * self.height )

	def fillRect( self ):

		# Get args
		x = self.main_memory.read( self.addrScreenArg0 )
		y = self.main_memory.read( self.addrScreenArg1 )
		w = self.main_memory.read( self.addrScreenArg2 )
		h = self.main_memory.read( self.addrScreenArg3 )

		x = self.bitArrayToInt( x )
		y = self.bitArrayToInt( y )
		w = self.bitArrayToInt( w )
		h = self.bitArrayToInt( h )

		# Check if coordinates are valid
		if(
			w <= 0 or
			h <= 0 or
			x <  0 or ( x + w ) > self.width or
			y <  0 or ( y + h ) > self.height
		):
			raise Exception( 'fillRect received invalid argument(s): ( {}, {}, {}, {} )'.format( x, y, w, h ) )

		# Draw fill lines horizontally
		for i in range( y, y + h ):

			self.flood( x, i, w )


	def drawPixelBuffer( self, bitMode = 1 ):

		'''
			Draw pixels from main memory.
			'pixBuffer' is a pointer to a location in main memory
			 holding encoded pixel data.
		'''

		# Get args
		pixBuffer = self.main_memory.read( self.addrScreenArg0 )
		srcX      = self.main_memory.read( self.addrScreenArg1 )
		srcY      = self.main_memory.read( self.addrScreenArg2 )
		srcW      = self.main_memory.read( self.addrScreenArg3 )
		srcH      = self.main_memory.read( self.addrScreenArg4 )
		dstX      = self.main_memory.read( self.addrScreenArg5 )
		dstY      = self.main_memory.read( self.addrScreenArg6 )

		pixBuffer = self.bitArrayToInt( pixBuffer )
		srcX      = self.bitArrayToInt( srcX      )
		srcY      = self.bitArrayToInt( srcY      )
		srcW      = self.bitArrayToInt( srcW      )
		srcH      = self.bitArrayToInt( srcH      )
		dstX      = self.bitArrayToInt( dstX      )
		dstY      = self.bitArrayToInt( dstY      )

		# Check if coordinates are valid
		if(
			srcW <= 0 or
			srcH <= 0 or
			srcX <  0 or ( srcX + srcW ) > self.width or
			srcY <  0 or ( srcY + srcH ) > self.height or
			dstX <  0 or ( dstX + srcW ) > self.width or
			dstY <  0 or ( dstY + srcH ) > self.height
		):
			raise Exception( 'drawBuffer received invalid coordinate(s): ( {}, {}, {}, {}, {}, {} )'.format( 

				srcX, srcY, srcW, srcH, dstX, dstY
			) )

		# Replace
		if( srcW == self.width and srcH == self.height ):

			if bitMode == 4:

				self.getPixelsFromMain_4BitMode_fast( pixBuffer )

			else:

				self.getPixelsFromMain_1BitMode_fast( pixBuffer )

		else:

			if bitMode == 4:

				self.getPixelsFromMain_4BitMode( pixBuffer, srcX, srcY, srcW, srcH, dstX, dstY )

			else:

				self.getPixelsFromMain_1BitMode( pixBuffer, srcX, srcY, srcW, srcH, dstX, dstY )

		# Mark screen for update
		self.newContent = True

	def drawPixelBuffer4( self ):

		self.drawPixelBuffer( bitMode = 4 )

	def getPixelsFromMain_1BitMode( self, pixBuffer, srcX, srcY, srcW, srcH, dstX, dstY ):

		startX    = srcX
		endX      = srcX + srcW
		startXDst = dstX

		# startWord = startX // self.nPixelsPerWord_1
		# endWord   = endX // self.nPixelsPerWord_1

		# startWordOffset = startX % self.nPixelsPerWord_1
		# endWordOffset   = endX % self.nPixelsPerWord_1

		( startWord, startWordOffset ) = divmod( startX, self.nPixelsPerWord_1 )
		( endWord, endWordOffset )     = divmod(   endX, self.nPixelsPerWord_1 )

		regIdx = pixBuffer + ( srcY * self.nRegistersPerRow_1 )

		for srcY in range( srcY, srcY + srcH ):

			srcX = startX
			word = startWord
			dstX = startXDst

			for word in range( startWord, endWord + 1 ):

				register = self.main_memory.read( regIdx + word )

				register = self.bitArrayToBinaryString( register )

				for i in range( self.nPixelsPerWord_1 ):

					if word == startWord and i < startWordOffset:

						continue  # skip

					elif word == endWord and i >= endWordOffset:

						break  # done with word

					pixel = register[ i ]

					color = self.colors_1[ pixel ]  # look up corresponding color

					# self.pixelArray[ srcX ][ srcY ] = color
					self.pixelArray[ dstX ][ dstY ] = color

					srcX += 1
					dstX += 1

			dstY += 1
			regIdx += self.nRegistersPerRow_1


	def getPixelsFromMain_1BitMode_fast( self, pixBuffer ):

		x = 0
		y = 0

		for regIdx in range( pixBuffer, pixBuffer + self.nRegisters_1 ):

			register = self.main_memory.read( regIdx )

			register = self.bitArrayToBinaryString( register )

			for i in range( self.N ):

				pixel = register[ i ]

				color = self.colors_1[ pixel ]  # look up corresponding color

				self.pixelArray[ x ][ y ] = color

				x += 1

				if ( x == self.width ):

					x = 0
					y += 1

	def getPixelsFromMain_4BitMode( self, pixBuffer, srcX, srcY, srcW, srcH, dstX, dstY ):

		startX    = srcX
		endX      = srcX + srcW
		startXDst = dstX

		# startWord = startX // self.nPixelsPerWord_4
		# endWord   = endX // self.nPixelsPerWord_4

		# startWordOffset = startX % self.nPixelsPerWord_4
		# endWordOffset   = endX % self.nPixelsPerWord_4

		( startWord, startWordOffset ) = divmod( startX, self.nPixelsPerWord_4 )
		( endWord, endWordOffset )     = divmod(   endX, self.nPixelsPerWord_4 )

		regIdx = pixBuffer + ( srcY * self.nRegistersPerRow_1 )

		for srcY in range( srcY, srcY + srcH ):

			srcX = startX
			word = startWord
			dstX = startXDst

			for word in range( startWord, endWord + 1 ):

				register = self.main_memory.read( regIdx + word )

				register = self.bitArrayToBinaryString( register )

				for i in range( 0, self.N, 4 ):  # loop through pixels in register

					ii = i >> 2  # i // 4  # which pixel among the four is this one?

					if word == startWord and ii < startWordOffset:

						continue  # skip

					elif word == endWord and ii >= endWordOffset:

						break  # done with word

					pixel = register[ i : i + 4 ]

					color = self.colors_4[ pixel ]  # look up corresponding color

					# self.pixelArray[ srcX ][ srcY ] = color
					self.pixelArray[ dstX ][ dstY ] = color

					srcX += 1
					dstX += 1

			dstY += 1
			regIdx += self.nRegistersPerRow_4

	def getPixelsFromMain_4BitMode_fast( self, pixBuffer ):

		x = 0
		y = 0

		for idx in range( pixBuffer, pixBuffer + self.nRegisters_4 ):

			register = self.main_memory.read( idx )

			register = self.bitArrayToBinaryString( register )

			for i in range( 0, self.N, 4 ):  # loop through pixels in register

				pixel = register[ i : i + 4 ]

				color = self.colors_4[ pixel ]  # look up corresponding color

				self.pixelArray[ x ][ y ] = color

				x += 1

				if ( x == self.width ):

					x = 0
					y += 1


	# Mouse -----------------------------------------------------

	def handleMousePressed( self, button, pos ):

		''' If mouse button is pressed, write 1 and update mouseX and mouseY '''

		# print( 'Mouse pressed', pos )

		if button == 1:  # left button

			# Convert to binary
			mouseX = self.intToBitArray( pos[ 0 ] )
			mouseY = self.intToBitArray( pos[ 1 ] )

			# Write to memory
			self.main_memory.write( 1, self.oneN, 1, self.addrMouseP )
			self.main_memory.write( 1,    mouseX, 1, self.addrMouseX )
			self.main_memory.write( 1,    mouseY, 1, self.addrMouseY )

	def handleMouseReleased( self, button ):

		''' If mouse button is released, write 0
		    Note: Too fast, cleared long before Hack program has chance to poll
		'''

		# print( 'Mouse released' )

		if button == 1:  # left button

			# Write to memory
			self.main_memory.write( 1, self.zeroN, 1, self.addrMouseP )

	def handleMouseMoved( self, pos ):

		''' If mouse is moved, update mouseX and mouseY '''

		# Convert to binary
		mouseX = self.intToBitArray( pos[ 0 ] )
		mouseY = self.intToBitArray( pos[ 1 ] )

		# Write to memory
		self.main_memory.write( 1, mouseX, 1, self.addrMouseX )
		self.main_memory.write( 1, mouseY, 1, self.addrMouseY )


	# Keyboard --------------------------------------------------

	def handleKeyPressed( self, key, modifier ):

		''' If key is pressed, write 1 and update keyCode '''

		# Lookup keyCode
		keyCode = self.lookupKey( key, modifier )

		# print( 'Key pressed', key, modifier, keyCode )
		print( 'Key pressed', self.bitArrayToInt( keyCode ) )

		# Write to memory
		self.main_memory.write( 1, self.oneN, 1, self.addrKeyP )
		self.main_memory.write( 1,   keyCode, 1, self.addrKeyCode )

	def handleKeyReleased( self ):

		''' If key is released, write 0
			Note: Too fast, cleared long before Hack program has chance to poll
		'''

		# Write to memory
		self.main_memory.write( 1, self.zeroN, 1, self.addrKeyP )

	def lookupKey( self, key, modifier ):

		if key in lookup_keys:

			# Handle shift modified presses
			if modifier == 3 :

				if key in lookup_shiftModifiedKeys:

					return self.intToBitArray( lookup_shiftModifiedKeys[ key ][ 0 ] )

				else:

					'''
						Ideally shift modifer would be 0 when shift key pressed alone.
						However not the case. Sometimes it's 0 sometimes it's set (1 or 2).
						Not sure how to work around. For now, ignoring all shift key presses
						where shift modifier is set.
						TLDR, shift key will not register consistently unless used as a modifier
					'''
					return self.zeroN

			# Handle caps_lock modified presses
			elif modifier == 8192:

				if key in range( 97, 123 ):  # is a letter

					return self.intToBitArray( lookup_shiftModifiedKeys[ key ][ 0 ] )

				else:

					return self.intToBitArray( lookup_keys[ key ][ 0 ] )

			else:

				return self.intToBitArray( lookup_keys[ key ][ 0 ]	 )

		else:

			return self.zeroN



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
