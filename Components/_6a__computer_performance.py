'''----------------------------- Imports -----------------------------'''

# Built ins
import time, math

# Hack computer
from ._x__components import *


'''---------------------------- MemoryROM ----------------------------'''

class MemoryROMXN_():

	''' Holds program instructions '''

	def __init__( self, X, N ):

		self.isReady = False

		self.X = X
		self.N = N		

		if PERFORMANCE_MODE:
			self.ROM = RAMXN_performance_( X, N )
		else:
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

		with open( binary_file, encoding='utf-8' ) as input_file:
				
			for instruction in input_file:

				instruction = instruction.rstrip()  # remove newline characters

				self.ROM.write( 1, instruction, 1, address )  # write

				address += 1

		print( 'Completed ROM flash. Took {} seconds for {} lines'.format( time.time() - startTime, address ) )

		self.isReady = True

		# print( 'E.g. the value stored at register {} is {}'.format( 0, ''.join( map(str, self.ROM.read( 0 ) ) ) ) )


	def read( self, address ):

		return self.ROM.read( address )



'''---------------------------- MemoryRAM ----------------------------'''

class MemoryRAMXN_():

	''' Holds generated data '''

	def __init__( self, X, N ):

		if PERFORMANCE_MODE:
			self.RAM = RAMXN_performance_( X, N )
		else:
			self.RAM = RAMXN_( X, N )


	def write( self, clk, x, write, address ):

		self.RAM.write( clk, x, write, address )


	def read( self, address ):

		return self.RAM.read( address )



'''------------------------------- CPU -------------------------------'''

class CPU_():

	''' Fetches and executes program instructions '''

	def __init__( self, N ):
		
		self.N = N

		if PERFORMANCE_MODE:
			self.programCounter = ProgramCounterN_performance_( N )
			self.A_register = RegisterN_performance_( N )
			self.D_register = RegisterN_performance_( N )
		else:
			self.programCounter = ProgramCounterN_( N )
			self.A_register = RegisterN_( N )
			self.D_register = RegisterN_( N )

		# n_bit instruction support
		nUnusedBits = N - 16  # shoved between opcode and ysel
		self.opcode = 0
		self.fub    = 1  + nUnusedBits
		self.ysel   = 3  + nUnusedBits
		self.cmp    = 4  + nUnusedBits
		self.dst    = 10 + nUnusedBits
		self.jmp    = 13 + nUnusedBits


	def doTheThing( self, clk, RESET, main_memory, program_memory ):

		# --- Fetch instruction ---
		instruction_address = self.programCounter.read()
		instruction = program_memory.read( instruction_address )
		# print( instruction_address, instruction )


		# --- Execute instruction ---
		'''
		 In the physical implementation, path selection would be accomplished by a tristate buffer, such that 
		 current flows only through the selected path.
		 I'm using an if statement (so sad), to accomplish this in code.
		'''

		if int( instruction[ self.opcode ] ) == 0:

			# --- Execute A instruction ---
			self.A_register.write( clk, instruction, 1 ) # write

			jump, increment = 0, 1
			self.programCounter.doTheThing( clk, zeroN, RESET, jump, increment ) # increment


		else:

			# --- Execute C instruction ---

			# - Computation -
			 
			x = self.D_register.read()

			y = None

			if PERFORMANCE_MODE:

				y = muxN_performance_(
					self.N,
					main_memory.read( self.A_register.readDecimal() ),
					# ( main_memory.read, ( self.A_register.readDecimal() ) ),  # dnw
					( self.A_register.read, () ),
					instruction[ self.ysel ]
				)

			else:

				y = muxN_(
					self.N,
					main_memory.read( self.A_register.readDecimal() ),
					self.A_register.read(),
					instruction[ self.ysel ]
				)

			ALU_out = ALU_( 
				self.N,
				x, y,
				instruction[ self.fub + 0 ], instruction[ self.fub + 1 ],
				instruction[ self.cmp + 0 ], instruction[ self.cmp + 1 ], instruction[ self.cmp + 2 ], 
				instruction[ self.cmp + 3 ], instruction[ self.cmp + 4 ], instruction[ self.cmp + 5 ] 
			)


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
				instruction[ self.jmp + 0 ], instruction[ self.jmp + 1 ], instruction[ self.jmp + 2 ] 
			)

			increment = 1 # hold high, pC design ensures priority of control bits preserved
			self.programCounter.doTheThing( clk, self.A_register.read(), RESET, jump, increment ) # write


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

			writeA = mux8to1_( 1, 1, 1, 1, 0, 0, 0, 0, instruction[ self.dst + 0 ], instruction[ self.dst + 1 ], instruction[ self.dst + 2 ] )
			writeD = mux8to1_( 1, 1, 0, 0, 1, 1, 0, 0, instruction[ self.dst + 0 ], instruction[ self.dst + 1 ], instruction[ self.dst + 2 ] )
			writeM = mux8to1_( 1, 0, 1, 0, 1, 0, 1, 0, instruction[ self.dst + 0 ], instruction[ self.dst + 1 ], instruction[ self.dst + 2 ] )

			self.A_register.write( clk, ALU_out[0], writeA ) # write
			self.D_register.write( clk, ALU_out[0], writeD ) # write
			main_memory.write(     clk, ALU_out[0], writeM, self.A_register.readDecimal() ) # write


	def out( self ):
		pass



'''----------------------------- Computer -----------------------------'''

class ComputerN_():

	''' N bit CPU + RAM + ROM '''

	def __init__( self, N, RAM_size, ROM_size ):

		self.CPU = CPU_( N )
		self.main_memory = MemoryRAMXN_( RAM_size, N )
		self.program_memory = MemoryROMXN_( ROM_size, N )

		self.reset = 0


	def load( self, binary_file ):

		self.program_memory.flash( binary_file )


	def run( self, clk ):

		self.CPU.doTheThing( clk, self.reset, self.main_memory, self.program_memory )

		# reset the reset ...
		if self.reset == 1: self.reset = 0

	
	def reset( self ):

		self.reset = 1
