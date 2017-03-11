''' Testing PyGame

	Installing PyGame:
		python -m pip install pygame
		python -m pip instanll numpy
'''

import pygame

import numpy

from frames2 import *

pygame.init()

pygame.display.set_caption( 'Hack Computer' )  # title

w = 512
h = 256

display = pygame.display.set_mode( ( w, h ) )

clock = pygame.time.Clock()


bgCol = ( 0, 10, 30 )  # ( r, g, b )
# display.fill( bgCol )


def transpose( a ):

	return list( map( list, zip( * a ) ) )

def convertToValid( a ):

	t = transpose( a )       # transpose to [ x, y ]
	return numpy.array( t )  # convert to numpy array


# pixels = convertToValid( data )
# pygame.surfarray.blit_array( display, pixels )


frames = [ convertToValid( frame ) for frame in data ]
print( 'Finished data prep' )

frameIdx = 0

def updateFrame():

	global frameIdx

	pygame.surfarray.blit_array( display, frames[ frameIdx ] )

	frameIdx = ( frameIdx + 1 ) % len( frames )

def handleKeyDown( key ):

	if key == pygame.K_LEFT:

		display.fill( ( 30, 10, 20 ) )


def loop():

	while True:

		for event in pygame.event.get():

			# print( event )

			if event.type == pygame.QUIT:  # click X

				pygame.quit()

				print( 'See you later!' )

				return

			if event.type == pygame.KEYDOWN:

				handleKeyDown( event.key )


		# mouse = pygame.mouse.get_pos()
		# print( mouse )

		updateFrame()

		pygame.display.update()

		clock.tick( 60 )  # fps

loop()
