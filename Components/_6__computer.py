''''''''''''''''''''''''''' imports '''''''''''''''''''''''''''''

# Built ins
import time, math

# Hack computer
from ._x__components import *


''''''''''''''''''''''''' MemoryROM '''''''''''''''''''''''''''

class MemoryROMXN_():

	''' Holds program instructions '''

	def __init__( self, X, N ):

		self.ROM = RAMXN_( X, N )
		self.isReady = False

	
	def flash( self, binary_file ):

		''' 
		 Write contents of binary file to ROM 
		  (uses Python logic)
		'''

		time.clock() # start timer
		
		print( 'Starting ROM flash' )

		address = 0

		with open( binary_file, encoding='utf-8' ) as input_file:
				
			for instruction in input_file:

				self.ROM.write( 1, instruction, 1, address )  # write

				address += 1

				time.sleep( CLOCK_HALF_PERIOD ) # wait until write complete

		print( 'Completed ROM flash. Took {} seconds for {} lines'.format( time.clock(), address ) )

		self.isReady = True

		# print( 'E.g. the value stored at register {} is {}'.format( 0, ''.join( map(str, self.ROM.read( 0 ) ) ) ) )


	def read( self, address ):

		return self.ROM.read( address )



''''''''''''''''''''''''' MemoryRAM '''''''''''''''''''''''''''

class MemoryRAMXN_():

	''' Contains,
			data memory map     16k ? |                 0 .. SCREEN_MEMORY_MAP - 1
			screen memory map    8k ? | SCREEN_MEMORY_MAP .. KBD_MEMORY_MAP - 1
			keyboard memory map   1 ? | KBD_MEMORY_MAP
	'''

	def __init__( self, X, N ):

		self.RAM = RAMXN_( X, N )


	def write( self, clk, x, write, address ):

		self.RAM.write( clk, x, write, address )


	def read( self, address ):

		return self.RAM.read( address )



''''''''''''''''''''''''''' CPU '''''''''''''''''''''''''''''

class CPU_():

	''' Fetches and executes program instructions '''

	def __init__( self, N, pC_addressSize ):
		
		self.N = N
		self.A_register = RegisterN_( N )
		self.D_register = RegisterN_( N )
		self.programCounter = ProgramCounterN_( pC_addressSize )


	def doTheThing( self, clk, rst, main_memory, program_memory ):

		# --- Fetch instruction ---
		instruction_address = self.programCounter.read()
		instruction = program_memory.read( instruction_address )


		# --- Execute instruction ---
		'''
		 In the physical implementation, path selection would be accomplished by a tristate buffer, such that 
		 current flows only through the selected path.
		 I'm using an if statement (so sad), to accomplish this in code.
		'''

		if instruction[0] == 0:

			# --- Execute A instruction ---
			self.A_register.write( clk, instruction, 1 ) # write


		else:

			# --- Execute C instruction ---

			# - Computation -
			 
			x = self.D_register.read()

			y = muxN_(
				self.N,
				main_memory.read( self.A_register.read() ),
				self.A_register.read(),
				instruction[3]
			) 

			ALU_out = ALU_( x, y, instruction[4], instruction[5], instruction[6], instruction[7], instruction[8], instruction[9] )


			# - Jump -

			'''
				'JMP'  : '111'
				'JLE'  : '110',
				'JNE'  : '101',
				'JLT'  : '100',
				'JGE'  : '011',
				'JEQ'  : '010',
				'JGT'  : '001',
				'NULL' : '000',
			'''		

			zr = ALU_out[1] # ALU out is zero
			ng = ALU_out[2] # ALU out is negative

			jump = mux8to1_( 
				1,                      # JMP
				or_( zr, ng ),          # JLE
				not_( zr ),             # JNE
				ng,                     # JLT
				or_( zr, not_( ng ) ),  # JGE
				zr,                     # JEQ
				not_( or_( zr, ng ) ),  # JGT
				0,                      # NULL
				instruction[13], instruction[14], instruction[15] 
			)

			increment = 1 # hold high, pC design ensures priority of control bits preserved
			self.programCounter.doTheThing( clk, ALU_out[0], RESET, jump, increment ) # write


			# - Destination -
			
			'''
				'AMD'  : '111'
				'AD'   : '110',
				'AM'   : '101',
				'A'    : '100',
				'MD'   : '011',
				'D'    : '010',
				'M'    : '001',
				'NULL' : '000',
			'''

			writeA = mux8to1_( 1, 1, 1, 1, 0, 0, 0, 0, instruction[13], instruction[14], instruction[15] )
			writeD = mux8to1_( 1, 1, 0, 0, 1, 1, 0, 0, instruction[13], instruction[14], instruction[15] )
			writeM = mux8to1_( 1, 0, 1, 0, 1, 0, 1, 0, instruction[13], instruction[14], instruction[15] )

			self.A_register.write( clk, ALU_out[0], writeA ) # write
			self.D_register.write( clk, ALU_out[0], writeD ) # write
			main_memory.write(     clk, ALU_out[0], writeM ) # write


	def out( self ):
		pass



''''''''''''''''''''''''''' Computer '''''''''''''''''''''''''''''

class ComputerN_():

	''' N bit CPU + RAM + ROM '''

	def __init__( self, N, RAM_size, ROM_size ):

		programCounter_addrSize = int( math.log( ROM_size, 2 ) )  # hmmm....
		self.CPU = CPU_( N, programCounter_addrSize )

		self.main_memory = MemoryRAMXN_( RAM_size, N )
		self.program_memory = MemoryROMXN_( ROM_size, N )

		self.reset = 0


	def __load__( self, binary_file ):

		self.program_memory.flash( binary_file )


	def __run__( self, clk ):

		self.CPU.doTheThing( clk, self.reset, self.main_memory, self.program_memory )

		# reset the reset ...
		if self.reset == 1: self.reset = 0

	
	def __reset__( self ):

		self.reset = 1



''''''''''''''''''''''''''' Screen '''''''''''''''''''''''''''''
# a bit of a hack. Would require drivers in physical implmentation.
''''''''''''''''''''''''''' Keyboard '''''''''''''''''''''''''''''
# a bit of a hack. Would require drivers in physical implmentation.
