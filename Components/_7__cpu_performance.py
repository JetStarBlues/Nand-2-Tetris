''' Selection is implemented using Python if-statements instead of muxes '''

'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''------------------------------- CPU -------------------------------'''

'''
  Instruction -> 0123456789ABCDEF
    
    0   -> opCode
    1   -> comp, xor
    2   -> comp, bitshift
    3   -> y = A (0) | M (1)
    4   -> comp, zero_x  
    5   -> comp, not_x  
    6   -> comp, zero_y  
    7   -> comp, not_y  
    8   -> comp, and (0) | add (1)  
    9   -> comp, negate_out
    ABC -> destination
    DEF -> jump

    comp(utation) bits are sent to ALU
'''

class CPU_():

	''' Fetches and executes program instructions '''

	def __init__( self, N ):
		
		self.N = N

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
			instruction = int( instruction, 2 )  # convert from binary to integer representation
			self.A_register.write( clk, instruction, 1 )  # write

			jump, increment = 0, 1
			self.programCounter.doTheThing( clk, None, RESET, jump, increment ) # increment


		else:

			# --- Execute C instruction ---

			# - Computation -
			 
			x = self.D_register.read()

			if int( instruction[ self.ysel ] ) == 0:

				y = self.A_register.read()

			else:

				y = main_memory.read( self.A_register.readDecimal() )

			ALU_out = ALU_(

				self.N,
				x, y,
				int( instruction[ self.fub + 0 ] ), int( instruction[ self.fub + 1 ] ),
				int( instruction[ self.cmp + 0 ] ), int( instruction[ self.cmp + 1 ] ), int( instruction[ self.cmp + 2 ] ), 
				int( instruction[ self.cmp + 3 ] ), int( instruction[ self.cmp + 4 ] ), int( instruction[ self.cmp + 5 ] ) 
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

				1,                # JMP
				zr | ng,          # JLE
				not_( zr ),       # JNE
				ng,               # JLT
				not_( ng ),       # JGE
				zr,               # JEQ
				not_( zr | ng ),  # JGT
				0,                # NULL
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
