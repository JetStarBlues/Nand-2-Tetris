'''----------------------------- Imports -----------------------------'''

# Built ins
import time
import os

# Hack computer
from ._x__components import *


'''---------------------------- ROM Memory ----------------------------'''

class MemoryROMXN_():

	''' Holds program instructions '''

	def __init__( self, X, N ):

		self.isReady = False

		self.X = X
		self.N = N		

		self.ROM = RAMXN_( X, N )

	
	def flash( self, binaryFile ):

		''' 
		 Write contents of binary file to ROM 
		  (uses Python logic)
		'''

		startTime = time.time()
		
		print( '\nStarting ROM flash' )

		if self.isReady:                        # if previously written to,
		
			self.ROM = RAMXN_( self.X, self.N ) #  cheap way to clear all registers
		
		self.isReady = False		

		address = 0

		with open( binaryFile, encoding = 'utf-8' ) as input_file:
				
			for instruction in input_file:

				instruction = instruction.rstrip()  # remove newline characters

				instruction = tuple( map( int, instruction ) ) # convert to tuple of ints

				self.ROM.write( 1, instruction, 1, address )  # write

				address += 1

		print( 'Completed ROM flash. Took {} seconds for {} lines\n'.format( time.time() - startTime, address ) )

		self.isReady = True

		# print( 'E.g. the value stored at register {} is {}'.format( 0, ''.join( map(str, self.ROM.read( 0 ) ) ) ) )


	def read( self, address ):

		return self.ROM.read( address )


	def readDecimal( self, address ):

		return self.ROM.readDecimal( address )



'''---------------------------- RAM Memory ----------------------------'''

class MemoryRAMXN_():

	''' Holds generated data '''

	def __init__( self, X, N ):

		self.RAM = RAMXN_( X, N )


	def write( self, clk, x, write, address ):

		self.RAM.write( clk, x, write, address )


	def read( self, address ):

		return self.RAM.read( address )


	def readDecimal( self, address ):

		return self.RAM.readDecimal( address )



'''----------------------------- Computer -----------------------------'''

class ComputerN_():

	''' N bit CPU + RAM + ROM '''

	def __init__( self, N, RAMSize, ROMSize ):

		self.N = N

		# Memory
		self.data_memory = MemoryRAMXN_( RAMSize, N )
		# self.program_memory = MemoryROMXN_( ROMSize, N )
		self.maxROMSize = ROMSize

		# CPU
		self.CPU = CPU_( N )

		# Signals (input)
		self.reset              = 1  # Start with known state
		self.interruptRequested = 0

		# Signals (output)
		self.halted             = 0

		# Buses
		self.IODatabus = ( 0, ) * N


	def load( self, binaryFile ):

		binaryFileSize = os.path.getsize( binaryFile )

		programSize = binaryFileSize // 18  # 1 byte for 0/1, 2 bytes for \n ... so 18 bytes per line

		if ( programSize <= self.maxROMSize ):

			self.program_memory = MemoryROMXN_( programSize + 1, self.N )  # init as size of program

			self.program_memory.flash( binaryFile )


	def run( self, clk ):

		self.CPU.doTheThing(

			self,  # pass CPU a pointer to self...

			clk,
			self.reset,
			self.interruptRequested,

			self.IODatabus
		)

		# Reset the reset
		# Poll in lieu of hardware button
		if self.reset == 1: self.reset = 0

	
	def reset( self ):

		self.reset = 1
