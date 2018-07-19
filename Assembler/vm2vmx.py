# ========================================================================================
#
#  Description:
#
#     Generates a merged copy of the Hack VM (virtual machine) files present in a directory
#
#  Attribution:
#
#     Code by www.jk-quantized.com
#
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
#
# ========================================================================================


# == Imports =======================================================

# Built ins
import os


# == Main ==========================================================

def getVMFilesFromDir( dirPath ):

	fileNames = os.listdir( dirPath )

	filePaths = []

	for fileName in fileNames:

		if fileName[ -2 : ] == 'vm':

			filePath = dirPath + '/' + fileName

			filePaths.append( filePath )

	return filePaths


def genVMXFile( inputDirPath, libraryPaths = None, extension = 'vmx' ):

	''' Merge the vm files in a directory into a single 'vmx' file '''

	# Get input file paths
	inputFilePaths = getVMFilesFromDir( inputDirPath )

	if libraryPaths:

		inputFilePaths.extend( libraryPaths )

	# Get output file path
	outputFilePath = inputDirPath + '/Main.' + extension

	# Setup for execution
	with open( outputFilePath, 'w' ) as outputFile:

		# Insert call to Sys.init
		outputFile.write( 'call Sys.init 0\n' )

	# Read and write
	for inputFilePath in inputFilePaths:

		print( ' - Merging {}'.format( inputFilePath ) )

		with open( inputFilePath, 'r' ) as inputFile:

			with open( outputFilePath, 'a' ) as outputFile:

				for line in inputFile:

					outputFile.write( line )

	# print( 'Done' )
