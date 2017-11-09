# Code by www.jk-quantized.com

hex2hbin = {

	# PICO-8 palette
	#  www.lexaloffle.com/gfx/pico8_pal_017.png
	'#000000' : '0000',
	'#1D2B53' : '0001',
	'#7E2553' : '0010',
	'#008751' : '0011',
	'#AB5236' : '0100',
	'#5F574F' : '0101',
	'#C2C3C7' : '0110',
	'#FFF1E8' : '0111',
	'#FF004D' : '1000',
	'#FFA300' : '1001',
	'#FFEC27' : '1010',
	'#00E436' : '1011',
	'#29ADFF' : '1100',
	'#83769C' : '1101',
	'#FF77A8' : '1110',
	'#FFCCAA' : '1111',
}

hex2rle = {

	'#000000' : '0',
	'#1D2B53' : '1',
	'#7E2553' : '2',
	'#008751' : '3',
	'#AB5236' : '4',
	'#5F574F' : '5',
	'#C2C3C7' : '6',
	'#FFF1E8' : '7',
	'#FF004D' : '8',
	'#FFA300' : '9',
	'#FFEC27' : '10',
	'#00E436' : '11',
	'#29ADFF' : '12',
	'#83769C' : '13',
	'#FF77A8' : '14',
	'#FFCCAA' : '15',
}

xpm2hex = {
	
	# Map XPM symbols to hex color codes
}

# imageWidth = 220
imageWidth = 512

def generatePy( inputDirPath, inputFilePaths, outputFilePath ):

	with open( outputFilePath, 'w' ) as outputFile:

		outputFile.write( 'data = [\n\n' )

		for inputFilePath in inputFilePaths:

			with open( inputDirPath + inputFilePath, 'r' ) as inputFile:

				outputFile.write( '(\n' )

				for line in inputFile:

					if line[0] == '"' and not line[1].isdigit():

						if 'c' in line:

							xpm2hex[ line[1] ] = line[-10:-3]
							# xpm2hex[ line[1] ] = hex2hbin( line[-9:-2] )

						else:

							s = ''

							curCount = 0
							curChar = line[1]

							for i in range( 1, imageWidth + 1 ):

								symb = line[i]

								if curChar == symb:

									curCount += 1

									if i == imageWidth:

										# s += '{}:{}:'.format( hex2rle[ xpm2hex[ curChar ] ], curCount )
										s += '{},{},'.format( hex2rle[ xpm2hex[ curChar ] ], curCount )

								else:

									# s += '{}:{}:'.format( hex2rle[ xpm2hex[ curChar ] ], curCount )
									s += '{},{},'.format( hex2rle[ xpm2hex[ curChar ] ], curCount )

									# Reset
									curCount = 1
									curChar = symb


							s = "\t'{}',\n".format( s[ : -1 ] )

							outputFile.write( s )


				outputFile.write( '),\n\n')

		outputFile.write( ']\n' )

inputDirPath = 'xpm/'
outputFilePath = 'frames_rle.py'


# import os
# import re
# 
# def getFrameNumber( s ):
# 
# 	n = re.findall(  r'\d+', s )[0]
# 	return int(n)
# 
# inputFilePaths = os.listdir( inputDirPath )
# inputFilePaths.sort( key = getFrameNumber )
# # print( inputFilePaths )
# 
# generatePy( inputDirPath, inputFilePaths, outputFilePath )

generatePy( inputDirPath, [ 'helgram_cropped&cleaned.xpm' ], outputFilePath )
