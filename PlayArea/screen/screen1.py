from tkinter import *

root = Tk()
root.wm_title('Hack')
root.iconbitmap('favicon.ico')

width = 512
height = 256

# stackoverflow.com/a/10423793
img = PhotoImage( width = width, height = height )

w = 100
h = 100

data = (

	'{0000000001} '   # horizontal line
	'{0000000011} '
	'{0000000111} '
	'{0000001111} '
	'{0000011111} '
	'{0000111111} '
	'{0001111111} '
	'{0011111111} '
	'{0111111111} '
	'{1111111111} '
)

data = data.replace( '0', 'white ' ).replace( '1', 'black ' )
img.put( data, to = (20, 20, w, h ) )


label = Label(root)
label.pack()
label.config( image = img )


root.mainloop()