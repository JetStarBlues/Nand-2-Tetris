'''----------------------------- Imports -----------------------------'''

# Built ins
import time

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

	
	def flash( self, binary_file ):

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

		with open( binary_file, encoding = 'utf-8' ) as input_file:
				
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



'''---------------------------- RAM Memory ----------------------------'''

class MemoryRAMXN_():

	''' Holds generated data '''

	def __init__( self, X, N ):

		self.RAM = RAMXN_( X, N )


	def write( self, clk, x, write, address ):

		self.RAM.write( clk, x, write, address )


	def read( self, address ):

		return self.RAM.read( address )



'''----------------------------- Computer -----------------------------'''

class ComputerN_():

	''' N bit CPU + RAM + ROM '''

	def __init__( self, N, RAM_size, ROM_size ):

		self.CPU = CPU_( N )
		self.data_memory = MemoryRAMXN_( RAM_size, N )
		self.program_memory = MemoryROMXN_( ROM_size, N )

		self.reset = 0  # If true(1), sets program counter value to zero


	def load( self, binary_file ):

		self.program_memory.flash( binary_file )


	def run( self, clk ):

		self.CPU.doTheThing( clk, self.reset, self.data_memory, self.program_memory )

		# reset the reset ...
		# if self.reset == 1: self.reset = 0

	
	# def reset( self ):

	# 	self.reset = 1

