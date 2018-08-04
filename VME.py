# ========================================================================================
#
#  Description:
#
#    Graphical (GUI) launcher for the VM Emulator.
#
#  Attribution:
#
#     Code by www.jk-quantized.com
#
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
#
# ========================================================================================



'''----------------------------- Imports -----------------------------'''

# General
import subprocess

# Tkinter
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk



'''------------------------------- GUI -------------------------------'''

class GUI ():

	def __init__ ( self ):

		# General
		self.hasExited = False
		self.fileName = None

		# Initialize tkinter
		self.initTkinter()


	def initTkinter ( self ):

		# Settings
		bgColor = '#27282c'
		width   = 400
		height  = 200


		# Window setup
		self.root = tkinter.Tk()
		self.root.wm_title( 'VME Launcher' )
		self.root.iconbitmap( 'Components/favicon.ico' )

		self.root.geometry( '{}x{}'.format( width, height ) )
		self.root.resizable( False, False )
		self.root.configure( background = bgColor )


		# Images
		self.menuDefaultImg = ImageTk.PhotoImage( 

			Image.open( 'Other/GUIImages/menu_default.png' )
		)
		self.menuFileHoverImg = ImageTk.PhotoImage( 

			Image.open( 'Other/GUIImages/menu_file_hover.png' )
		)
		self.menuRunHoverImg = ImageTk.PhotoImage( 

			Image.open( 'Other/GUIImages/menu_run_hover.png' )
		)


		# Background image
		self.menuImgLabel = tkinter.Label(

			self.root,
			image = self.menuDefaultImg,
			borderwidth = 0,
			# background = 'green',
			background = bgColor,
			width = 200,
			height = 175
		)

		self.menuImgLabel.pack()


		# File location label
		self.fileLocLabel = tkinter.Label(

			self.root,
			text = '...',
			background = '#1d2b53',
			foreground = '#29adff',
			height = 25,
			width = 200,
			font = ( 'TkDefaultFont', 7 ),
			# anchor = tkinter.E,  # right align
			padx = 10,
			wraplength = width - 2 * 10
		)

		self.fileLocLabel.pack()


		# Events
		self.root.protocol( 'WM_DELETE_WINDOW', self.quitTkinter )  # when user closes window by clicking X
		self.root.bind( '<Button-1>', self.handleMouseClick )
		self.root.bind( '<Motion>', self.handleMouseMove )


		# Loop
		self.root.mainloop()


	def quitTkinter ( self, ev = None ):

		self.root.quit()

		self.hasExited = True


	def handleMouseClick ( self, ev ):

		if self.fileButtonSelected( ev.x, ev.y ):

			# file = tkinter.filedialog.askopenfilename()
			file = tkinter.filedialog.askdirectory()

			if file:

				self.fileName = file

				print( 'You selected, {}'.format( file ) )

				self.fileLocLabel.configure( text = file )

		elif self.runButtonSelected( ev.x, ev.y ):

			# print( 'Run' )

			if self.fileName:

				subprocess.run( [ 'Python', 'compile&RunVME.py', self.fileName ] )


	def handleMouseMove ( self, ev ):

		''' Button hover effect '''

		# print( '{} {}'.format( ev.x, ev.y ) )

		if self.fileButtonSelected( ev.x, ev.y ):

			self.menuImgLabel.configure(

				image = self.menuFileHoverImg
			)

		elif self.runButtonSelected( ev.x, ev.y ):

			self.menuImgLabel.configure(

				image = self.menuRunHoverImg
			)

		else:

			self.menuImgLabel.configure(

				image = self.menuDefaultImg
			)


	def fileButtonSelected ( self, x, y ):

		return (

			x >= 60  and  # -100
			x <= 114 and  # -100 +54
			y >= 26  and
			y <= 76       # +50
		)


	def runButtonSelected ( self, x, y ):

		return (

			x >= 86  and  # -100
			x <= 142 and  # -100 +56
			y >= 124 and
			y <= 174      # +50
		)



g = GUI()

