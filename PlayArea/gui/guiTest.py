import subprocess
import time

import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk


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
		self.root.resizable( False, False )
		self.root.configure( background = '#27282c' )


		# images
		menuDefaultImg = ImageTk.PhotoImage( 

			Image.open( 'C:/Users/Janet/Desktop/tempMenu/sketches/menu_default.png' )
		)
		emptyButtonImg = ImageTk.PhotoImage(

			Image.open( 'C:/Users/Janet/Desktop/tempMenu/sketches/emptyButton.png' )
		)

		menuImgLabel = tkinter.Label(

			self.root,
			image = menuDefaultImg,
			borderwidth = 0,
			background = 'green',
			width = 190,
			height = 190
		)
		# menuImgLabel.place(

		# 	x = 0,
		# 	y = 0,
		# 	relheight = 1,
		# 	relwidth = 1
		# )
		menuImgLabel.pack()
		
		# events
		# self.root.bind( '<KeyPress>', self._handleKeyPress )
		# self.root.bind( '<KeyRelease>', self._handleKeyRelease )
		self.root.protocol( 'WM_DELETE_WINDOW', self._quitTkinter )  # when user closes window by clicking X

		# ...
		# b = tkinter.Button(

		# 	self.root,
		# 	text = "Hi",
		# 	command = self.doThing,
		# 	background = "red",
		# 	foreground = "white",
		# 	borderwidth = 0,
		# 	cursor = 'hand2',  # pointer
		# )

		self.b = tkinter.Label(

			menuImgLabel,
			# command = self.doThing,
			borderwidth = 0,
			background = 'red',
			image = emptyButtonImg
			# width = 2,  # do the thing needed to make this pixels
			# height = 2,
		)
		# self.b.pack()
		self.b.place(

			x = 55,
			y = 21
		)

		self.b.bind( '<Enter>', self.on_enter0 );  # https://stackoverflow.com/a/49896477
		self.b.bind( '<Leave>', self.on_leave0 );
		self.b.bind( '<Button-1>', self.on_click0 );

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


	def on_enter0 ( self, e ):

		self.b[ 'background' ] = 'red'

	def on_leave0 ( self, e ):

		self.b[ 'background' ] = 'blue'

	def on_click0 ( self, e ):

		print( "Hi!" )



p = GUI()

