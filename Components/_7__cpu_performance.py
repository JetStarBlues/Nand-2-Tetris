''' Selection is implemented using Python if-statements instead of muxes '''

'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''------------------------------- CPU -------------------------------'''

'''
	Instruction - 0123456789ABCDEF

		0 -> opCode

		if opCode == 0, address instruction

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

		# hmmm
		# self.programMemoryBankSel = RegisterN_( N )  # initializes to zero
		# self.programMemoryBankSel_delay = RegisterN_( N )  # initializes to zero
		# self.delay_wenb = Register_()  # initializes to zero
		# self.dataMemoryBankSel = RegisterN_( N )  # initializes to zero

		# n_bit instruction support
		nUnusedBits = N - 16  # shoved between opcode and ysel
		self.opcode = 0
		self.fub    = 1  + nUnusedBits
		self.ysel   = 3  + nUnusedBits
		self.cmp    = 4  + nUnusedBits
		self.dst    = 10 + nUnusedBits
		self.jmp    = 13 + nUnusedBits


	def doTheThing( self, clk, RESET, data_memory, program_memory ):

		self.doTheThing_V2( clk, RESET, data_memory, program_memory )


	def doTheThing_V1( self, clk, RESET, data_memory, program_memory ):

		'''
		    V1 --
		    . Theoretically uses tristate buffer for switching between A and C instruction processing
		    . Only actions relevant to each instruction occur (are supplied power)
		    . Not sure if possible to physically implement
			. Assumes all memory modules can be read asynchronously
		'''

		# --- Fetch instruction ---

		instruction_address = self.programCounter.read()
		instruction = program_memory.read( instruction_address )
		# print( instruction_address, instruction )


		# --- Execute instruction ---

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

				y = data_memory.read( self.A_register.read() )

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

			zr = ALU_out[ 1 ] # ALU out is zero
			ng = ALU_out[ 2 ] # ALU out is negative

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

			self.A_register.write( clk, ALU_out[ 0 ], int( instruction[ self.dst + 0 ] ) ) # write
			self.D_register.write( clk, ALU_out[ 0 ], int( instruction[ self.dst + 1 ] ) ) # write
			data_memory.write(     clk, ALU_out[ 0 ], int( instruction[ self.dst + 2 ] ), self.A_register.read() ) # write


	def doTheThing_V2( self, clk, RESET, data_memory, program_memory ):

		'''
			V2 -- 
			. All computations happen regardless of instruction.
			. Multiplexers determine whether to ignore or act on computation results.
			. Assumes all memory modules can be read asynchronously
		'''

		# --- Fetch instruction ---

		# self.programMemoryBankSel.write( clk, self.programMemoryBankSel_delay.read(), self.delay_wenb.read() )  # restore
		

		instruction_address = self.programCounter.read()
		# instruction_address = ( self.programMemoryBankSel.read() << ( self.N - 1 ) ) | self.programCounter.read()  # physical wiring workaround
		instruction = program_memory.read( instruction_address )
		# print( instruction_address, instruction )
		# print( '{:<5} {}'.format( instruction_address, instruction_str ) )

		# instruction = [ int( b ) for b in instruction_str ]


		#hmmm
		# wenb = not_( instruction[ self.fub + 0 ] | instruction[ self.fub + 1 ] | instruction[ self.fub + 2 ] )
		# wenb = wenb & instruction[ self.fub + 3 ] & instruction[ self.opcode ]
		# self.delay_wenb.write( clk, wenb, 1 )

		# bank = toInt( instruction[ self.fub + 4 : self.dst ] )  # physical wiring workaround

		# print( 'Bank', wenb, bank )
		# print( 'Bank', self.delay_wenb.read(), bank )

		# self.programMemoryBankSel_delay.write( clk, bank, wenb )
		# self.programMemoryBankSel.write( clk, self.programMemoryBankSel_delay.read(), self.delay_wenb.read() )


		# --- Execute instruction ---

		increment = 1  # Hold high. PC design ensures priority ( reset -> jump -> increment )


		# - Computation -

		# ALU -
		x = self.D_register.read()

		if instruction[ self.ysel ] == 0:

			y = self.A_register.read()

		else:

			y = data_memory.read( self.A_register.read() )

		ALU_out = ALU_(

			self.N,
			x, y,
			instruction[ self.fub + 0 ], instruction[ self.fub + 1 ],
			instruction[ self.cmp + 0 ], instruction[ self.cmp + 1 ], instruction[ self.cmp + 2 ], 
			instruction[ self.cmp + 3 ], instruction[ self.cmp + 4 ], instruction[ self.cmp + 5 ] 
		)

		# print( 'ALU', x, y, ALU_out )

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

		zr = ALU_out[ 1 ] # ALU out is zero
		ng = ALU_out[ 2 ] # ALU out is negative

		jumpLogic = mux8to1_(

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


		# - Switching -

		# A instruction -
		if instruction[ self.opcode ] == 0:

			writeA = 1
			writeD = 0
			writeM = 0

			jump = 0

			# dataIn_A_Register = int( instruction, 2 )  # convert from binary to integer representation
			dataIn_A_Register = int( ''.join( map( str, instruction ) ), 2 )  # convert from binary to integer representation
		
		# C instruction -
		else:

			writeA = instruction[ self.dst + 0 ]
			writeD = instruction[ self.dst + 1 ]
			writeM = instruction[ self.dst + 2 ]

			jump = jumpLogic

			dataIn_A_Register = ALU_out[ 0 ]


		# - Writes -

		# jump |= wenb
		# print( 'PC write', jump, self.A_register.read() )
		self.programCounter.doTheThing( clk, self.A_register.read(), RESET, jump, increment )

		# print( 'A write', writeA, dataIn_A_Register )
		self.A_register.write( clk, dataIn_A_Register, writeA )
		# print( 'D write', writeD, ALU_out[ 0 ] )
		self.D_register.write( clk, ALU_out[ 0 ], writeD )
		# print( 'M write', writeM, ALU_out[ 0 ], self.A_register.read() )
		data_memory.write( clk, ALU_out[ 0 ], writeM, self.A_register.read() )

		# print( 'Bank', self.delay_wenb.read(), self.programMemoryBankSel.read() )
		# self.programMemoryBankSel.write( clk, self.programMemoryBankSel_delay.read(), self.delay_wenb.read() )  # restore
		# self.programMemoryBankSel_delay.write( clk, bank, wenb )  # save
		# self.delay_wenb.write( clk, wenb, 1 )  # save
