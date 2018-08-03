import subprocess
import time

import tkinter
import tkinter.filedialog


# subprocess.run( [ "python", "../../compile.py" ] )
# subprocess.run( [ "python", "callme.py" ] )


fileSel = ''  # may as well since requiring includes
folderSel = ''



class GUI ():

	''' Input and output devices.
	     Currently consists of screen and keyboard.
	'''

	def __init__ ( self ):

		# General ---
		self.hasExited = False

		# Initialize tkinter ---
		self._initTkinter()


	def _initTkinter ( self ):

		# general
		self.root = tkinter.Tk()
		self.root.wm_title( 'Hack Launcher' )
		# self.root.iconbitmap( 'Components/favicon.ico' )
		self.root.geometry( '400x200' )
		self.root.configure( background='#abcdef')
		
		# events
		# self.root.bind( '<KeyPress>', self._handleKeyPress )
		# self.root.bind( '<KeyRelease>', self._handleKeyRelease )
		# self.root.bind( '<Button-1>', self._handleMouseClick )
		self.root.protocol( 'WM_DELETE_WINDOW', self._quitTkinter )  # when user closes window by clicking X

		# ...
		b = tkinter.Button(
			self.root,
			text = "Hi",
			command = self.doThing,
			background = "red",
			foreground = "white",
			borderwidth = 0,
			cursor = 'hand2'  # pointer
			)
		b.pack()

		self.b2 = tkinter.Button(
			self.root,
			text = "Choose",
			command = self.doThing2,
			borderwidth = 0,
			background = "blue"
			)
		self.b2.pack()

		self.b2.bind( "<Enter>", self.on_enter );  # https://stackoverflow.com/a/49896477
		self.b2.bind( "<Leave>", self.on_leave );

		# self.lText = tkinter.StringVar()
		# self.lText.set( "..." )
		self.l = tkinter.Label( self.root, text = "..." )
		self.l.pack()

		# loop
		# self.update()

		#
		self.root.mainloop()

	def _quitTkinter( self, ev = None ):

		self.root.quit()
		self.hasExited = True


	def doThing ( self ):

		print( "Buenos dias!" )

	def doThing2 ( self ):

		file = tkinter.filedialog.askopenfilename()

		if file:

			print( "You chose," )
			print( file )

			self.l.configure( text = file )

	def on_enter ( self, e ):

		self.b2[ 'background' ] = 'purple'

	def on_leave ( self, e ):

		self.b2[ 'background' ] = 'blue'


p = GUI()

