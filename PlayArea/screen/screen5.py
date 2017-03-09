from tkinter import *

from frames import *  # pixel data

# Setup ---
root = Tk()
root.wm_title('Hack')
root.iconbitmap('favicon.ico')

width = 512
height = 256
img = PhotoImage( width = width, height = height )

label = Label(root)
label.pack()
label.config( image = img )


# Pixel data ---
	# See imported file ...


# Render ---

image_idx = 0

frame_duration = 1  # so slow =/
# frame_duration = 100

def updateImage( ev = None ):

	global image_idx

	img.put( data[image_idx], to = (0, 0, width, height) ) # update image

	image_idx = ( image_idx + 1 ) % len(data)  # increment index

	# print( image_idx )

	root.after( frame_duration, updateImage ) # set timer

updateImage()


root.bind( '<space>', updateImage )


root.mainloop()