''''''''''''''''''''''''' imports '''''''''''''''''''''''''''

# Built ins
import tkinter
import threading


''''''''''''''''''''''''' screen '''''''''''''''''''''''''''


class Screen():
	'''
		16 bit screen with a 512 x 256 pixels display.
		Specifications hardcoded for simplicity.

		Data stored using a 256 x 512 array to help with tkinter draw speed
		(In lieu of using a 1 x 8192 array which more closely resembles RAM).
	'''

	def __init__( self ):

		self.N = 16

		# Screen dimensions ---
		self.width = 512
		self.height = 256		
		self.registersPerRow = self.width // self.N


		# Pixel array ---
		self.pixels = [ [0] * self.width for _ in range( self.height ) ]


		# Initialize tkinter ---
		self.refreshRate = 100  # ms
		self.root = None
		self.img = None

		threading.Thread( 
			target = self._initTkinter,
			name = 'screen_thread'
		).start()


	def update( self ):

		# Format array to tkinter string ---
		data = [ '{' + ''.join( map( str, row ) ) + '} ' for row in self.pixels ]
		data = ''.join( data )

		data = data.replace( '0', 'white ' ).replace( '1', 'black ' )


		# Update tkinter ---
		self._updateTkinterImg( data )


	def write( self, x, address ):

		# Psuedo N bit RAM interface ---
		#  Maps RAM access style to pixel array access style

		row = address // self.registersPerRow
		col_0 = address % self.registersPerRow * self.N

		for col, bit in zip( range( col_0, col_0 + self.N ), range( 0, self.N ) ):
			self.pixels[row][col] = x[bit]


	def _initTkinter( self ):

		self.root = tkinter.Tk()
		self.root.wm_title('Hack')
		self.root.iconbitmap('favicon.ico')
		
		self.root.bind( '<Escape>', self._quitTkinter )

		self.img = tkinter.PhotoImage( width = self.width, height = self.height )

		label = tkinter.Label(self.root)
		label.pack()
		label.config( image = self.img )

		self.update()

		self.root.mainloop()


	def _updateTkinterImg( self, data ):

		self.img.put( data, to = (0, 0, self.width, self.height) )

		self.root.after( self.refreshRate, self.update )  # set timer


	def _quitTkinter( self, ev = None ):

		self.root.quit()


screen = Screen()

v = '1' * 16
screen.write( v, 0 * 32 + 10 )
screen.write( v, 1 * 32 + 10 )
screen.write( v, 2 * 32 + 10 )
screen.write( v, 3 * 32 + 10 )
screen.write( v, 4 * 32 + 10 )