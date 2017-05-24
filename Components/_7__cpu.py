'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''------------------------------- CPU -------------------------------'''

'''
	Instruction - 0123456789ABCDEF

		0 -> opCode

		if opcode == 0, address instruction

			123456789ABCDEF -> address

		else, computation instruction

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


	def doTheThing( self, clk, RESET, data_memory, program_memory ):

		'''
			. All computations happen regardless of instruction.
			. Multiplexers determine whether to ignore or act on computation results.
			. Assumes all memory modules can be read asynchronously
		'''

		# --- Fetch instruction ---
		instruction_address = self.programCounter.read()
		instruction = program_memory.read( instruction_address )
		# print( instruction_address, instruction )


		# --- Execute instruction ---

		increment = 1  # Hold high. PC design ensures priority ( reset -> jump -> increment )


		# - Computation - 

		# ALU -
		x = self.D_register.read()

		y = muxN_(

			self.N,
			data_memory.read( self.A_register.readDecimal() ),
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

		# Jump -

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

		jumpLogic = mux8to1_(
			
			1,                      # JMP
			or_( zr, ng ),          # JLE
			not_( zr ),             # JNE
			ng,                     # JLT
			not_( ng ),             # JGE
			zr,                     # JEQ
			not_( or_( zr, ng ) ),  # JGT
			0,                      # NULL
			instruction[ self.jmp + 0 ], instruction[ self.jmp + 1 ], instruction[ self.jmp + 2 ] 
		)


		# - Switching -

		writeA = mux_(

			instruction[ self.dst + 0 ],
			1,
			instruction[ self.opcode ]
		)

		writeD = mux_(

			instruction[ self.dst + 1 ],
			0,
			instruction[ self.opcode ]
		)

		writeM = mux_(

			instruction[ self.dst + 2 ],
			0,
			instruction[ self.opcode ]
		)

		jump = mux_(

			jumpLogic,
			0,
			instruction[ self.opcode ]
		)

		dataIn_A_Register = muxN_(

			self.N,
			ALU_out[ 0 ],
			instruction,
			instruction[ self.opcode ]
		)


		# - Writes -

		self.programCounter.doTheThing( clk, self.A_register.read(), RESET, jump, increment )

		self.A_register.write( clk, dataIn_A_Register, writeA )
		self.D_register.write( clk, ALU_out[ 0 ], writeD )
		data_memory.write( clk, ALU_out[ 0 ], writeM, self.A_register.readDecimal() )			
