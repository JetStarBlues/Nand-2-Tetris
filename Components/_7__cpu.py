'''----------------------------- Imports -----------------------------'''

# Hack computer
from ._x__components import *


'''------------------------------- CPU -------------------------------'''

'''
	Instruction - FEDCBA9876543210  // msb to lsb
	              0123456789ABCDEF  // array indexing

		F . 0  -> TECS instruction type (C if 1, @ if 0)
		E . 1  -> op
		D . 2  -> op
		C . 3  -> op
		B . 4  -> op
		A . 5  -> op
		9 . 6  -> xSel
		8 . 7  -> xSel
		7 . 8  -> ySel
		6 . 9  -> ySel
		5 . A  -> dst
		4 . B  -> dst
		3 . C  -> dst
		2 . D  -> jmp
		1 . E  -> jmp
		0 . F  -> jmp

	x/y sel
		0     D
		1     A
		2     B
		3     M

	dst
		0     NULL
		1     D
		2     A
		3     B
		4     M
		5     unused
		6     unused
		7     unused

	jmp
		0     NULL
		1     JGT
		2     JEQ
		3     JGE
		4     JLT
		5     JNE
		6     JLE
		7     JMP
'''

class CPU_():

	''' Fetches and executes program instructions '''

	def __init__( self, N ):
		
		self.N = N

		# Counters
		self.programCounter = CounterN_( 2 * N )

		nStepsPerInstruction = 4
		self.microCounter    = CounterN_( nStepsPerInstruction )

		# Internal ROM
		nInstructionTypes = 7
		nEntriesM         = nInstructionTypes * nStepsPerInstruction
		nControlSignals   = 18 ?
		nBitsInOpType     = 3
		nBitsInStep       = 2
		self.microcodeROM = ROMXN_( nEntriesM, nControlSignals )

		nEntriesA     = 32
		nBitsInfxSel  = 4
		nBitsInfxFlag = 5
		self.ALUROM   = ROMXN_( nEntriesA, nBitsInfxSel + nBitsInfxFlag )
		
		self.initInternalROM()

		# Registers
		self.A_register               = RegisterN_( N )
		self.D_register               = RegisterN_( N )
		self.B_register               = RegisterN_( N )
		self.AA_register              = RegisterN_( N )
		self.instruction_register     = RegisterN_( N )
		self.IOInput_register         = RegisterN_( N )

		self.ABkp_register            = RegisterN_( N )
		self.DBkp_register            = RegisterN_( N )
		self.BBkp_register            = RegisterN_( N )
		self.AABkp_register           = RegisterN_( N )
		self.instructionBkp_register  = RegisterN_( N )
		self.PCBkp_register           = RegisterN_( 2 * N )

		# Flip flops
		self.interruptsEnabled_ff     = DFlipFlop()
		self.interruptAcknowledged_ff = DFlipFlop()
		self.backupEnabled_ff         = DFlipFlop()

		# Initial (reset) values
		'''
		    interruptsEnabled_ff     = 1
		    interruptAcknowledged_ff = 0
		    backupEnabled_ff         = 1
		    programCounterOut        = 0
		    microCounterOut          = 0
		'''

		# Instruction decode
		self.TECSInstrType = 0
		self.op            = 1
		self.xSel          = 6
		self.ySel          = 8
		self.dst           = 10
		self.jmp           = 13

		self.nBitsInOp = 5

		# Corresponds to encoding in instruction...
		self.op_AAimmed     = ( 0, 0, 0, 0, 0 )
		self.op_reti        = ( 0, 0, 0, 0, 0 )
		self.op_nop         = ( 0, 0, 0, 0, 0 )
		self.op_dstEqIOBus  = ( 0, 0, 0, 0, 0 )

		# Corresponds to microcode ROM base address...
		self.opType_Aimmed      = self.intToBitArray( 0, nBitsInOpType )
		self.opType_AAimmed     = self.intToBitArray( 1, nBitsInOpType )
		self.opType_dstEqCmpJmp = self.intToBitArray( 2, nBitsInOpType )
		self.opType_dstEqIOBus  = self.intToBitArray( 3, nBitsInOpType )
		self.opType_intAck      = self.intToBitArray( 4, nBitsInOpType )
		self.opType_reti        = self.intToBitArray( 5, nBitsInOpType )
		self.opType_nop         = self.intToBitArray( 6, nBitsInOpType )

		# Location of ISRHandler in program
		self.ISRHandlerAddress = self.intToBitArray( 0, 2 * N )

		# Miscellaneous
		self.zero = self.intToBitArray( 0, N )
		self.AA_registerMask = ( 0, ) * 6 + ( 1, ) * 10


	def intToBitArray( self, x, N ):

		z = bin( x )[ 2 : ].zfill( N )

		return tuple( map( int, z ) )


	def initInternalROM( self ):

		# Microcode ROM
		'''
			                                     |  opType_Aimmed       |  opType_AAimmed      |  opType_dstEqCmpJmp  |  opType_dstEqIOBus   |  opType_intAck       |  opType_reti         |  opType_nop          |
			                                     |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |
			-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			c_cInst                              |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_ARegisterWr                        |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_ARegisterInSel_instructionRegister |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_AARegisterWr                       |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_instructionRegisterWr              |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |
			c_PCIncrement                        |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |
			c_PCWr                               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |
			c_PCInSel_ISRHandler                 |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |
			c_readIODatabus                      |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |
			c_dstInSel_IOInputRegister           |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_enableInterrupts                   |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |
			c_disableInterrupts                  |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_acknowledgeInterrupt               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_servicedInterrupt                  |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |
			c_enableRegisterBackup               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |
			c_disableRegisterBackup              |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_restoreRegisters                   |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |
		'''
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  0 )
		self.microcodeROM.write( 1, ( 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  1 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  2 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  3 )

		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  4 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  5 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  6 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  7 )

		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  8 )
		self.microcodeROM.write( 1, ( 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  9 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 10 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 11 )

		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 12 )
		self.microcodeROM.write( 1, ( 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0 ), 1, 13 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 14 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 15 )

		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 16 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0 ), 1, 17 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 18 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 19 )

		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 20 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ), 1, 21 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0 ), 1, 22 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 23 )

		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 24 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 25 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 26 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 27 )


		# ALU ROM
		'''
			op       fsel   flags                composite
			-----    ----   -----                ----------
			0        add    zx,     zy           0000 10100
			1        add    zx, nx, zy, ny, no   0000 11111
			- 1      add    zx, nx, zy           0000 11100
			x        and            zy, ny       0001 00110
			! x      and            zy, ny, no   0001 00111
			- x      add            zy, ny, no   0000 00111
			x + 1    add        nx, zy, ny, no   0000 01111
			x - 1    add            zy, ny       0000 00110
			x + y    add                         0000 00000
			x - y    add        nx,         no   0000 01001
			x & y    and                         0001 00000
			x | y    and        nx,     ny, no   0001 01011
			x ^ y    xor                         0010 00000
			x >> y   lsr                         0011 00000
			x << y   lsl                         0100 00000
			x * y    mul                         0101 00000
			x / y    div                         0110 00000
		'''

		self.ALUROM.write(  1, ( 0, 0, 0, 0, 1, 0, 1, 0, 0 ), 1,  0  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 1, 1, 1, 1, 1 ), 1,  1  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 1, 1, 1, 0, 0 ), 1,  2  )
		self.ALUROM.write(  1, ( 0, 0, 0, 1, 0, 0, 1, 1, 0 ), 1,  3  )
		self.ALUROM.write(  1, ( 0, 0, 0, 1, 0, 0, 1, 1, 1 ), 1,  4  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 0, 0, 1, 1, 1 ), 1,  5  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 0, 1, 1, 1, 1 ), 1,  6  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 0, 0, 1, 1, 0 ), 1,  7  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  8  )
		self.ALUROM.write(  1, ( 0, 0, 0, 0, 0, 1, 0, 0, 1 ), 1,  9  )
		self.ALUROM.write(  1, ( 0, 0, 0, 1, 0, 0, 0, 0, 0 ), 1, 10  )
		self.ALUROM.write(  1, ( 0, 0, 0, 1, 0, 1, 0, 1, 1 ), 1, 11  )
		self.ALUROM.write(  1, ( 0, 0, 1, 0, 0, 0, 0, 0, 0 ), 1, 12  )
		self.ALUROM.write(  1, ( 0, 0, 1, 1, 0, 0, 0, 0, 0 ), 1, 13  )
		self.ALUROM.write(  1, ( 0, 1, 0, 0, 0, 0, 0, 0, 0 ), 1, 14  )
		self.ALUROM.write(  1, ( 0, 1, 0, 1, 0, 0, 0, 0, 0 ), 1, 15  )
		self.ALUROM.write(  1, ( 0, 1, 1, 0, 0, 0, 0, 0, 0 ), 1, 16  )


	def compareOp( self, a, b ):

		# submodule, dry
		c = xorN_( self.nBitsInOp, a, b )
		d = orN_( self.nBitsInOp, c )
		return d



	def doTheThing( self, clk, RESET, interruptRequested, IODataBus, data_memory, program_memory ):

		'''
			. Everything happens at once/simultaneously
			. Assumes all memory modules can be read asynchronously
		'''

		# Constants -

		# Always increment microCounter
		microCounterIn        = 0
		microCounterWr        = 0
		microCounterIncrement = 1


		# Read memory -

		D_registerOut              = self.D_register.read()
		A_registerOut              = self.A_register.read()
		B_registerOut              = self.B_register.read()
		AA_registerOut             = self.AA_register.read()
		instruction_registerOut    = self.instruction_register.read()
		IOInput_registerOut        = self.IOInput_register.read()

		ABkp_registerOut           = self.ABkp_register.read()
		DBkp_registerOut           = self.DBkp_register.read()
		BBkp_registerOut           = self.BBkp_register.read()
		AABkp_registerOut          = self.AABkp_register.read()
		instructionBkp_registerOut = self.instructionBkp_register.read()
		PCBkp_registerOut          = self.PCBkp_register.read()

		# interruptsEnabled          = self.interruptsEnabled_ff.read()
		# interruptAcknowledged      = self.interruptAcknowledged_ff.read()
		# backupEnabled              = self.backupEnabled_ff.read()

		instruction  = instruction_registerOut
		lowerAddress = A_registerOut
		upperAddress = AA_registerOut

		dataMemoryOut = data_memory.read( lowerAddress )

		instructionAddress = self.programCounter.read()
		microStep          = self.microCounter.read()

		programMemoryOut = program_memory.read( self.programCounter.read() )


		# Decode -

		op = instruction[ self.op : self.op + self.nBitsInOp ]

		aInst = not_( instruction[ self.TECSInstrType ] )

		instructionType_p = muxN_(

			self.N,

			self.opType_Aimmed,
			iDecode0,

			aInst
		)
		iDecode0 = muxN_(

			self.N,

			self.opType_AAimmed,
			iDecode1,

			self.compareOp( op, self.op_AAimmed )
		)
		iDecode1 = muxN_(

			self.N,

			self.opType_reti,
			iDecode2,

			self.compareOp( op, self.op_reti )
		)
		iDecode2 = muxN_(

			self.N,

			self.opType_nop,
			iDecode3,

			self.compareOp( op, self.op_nop )
		)
		iDecode3 = muxN_(

			self.N,

			self.opType_dstEqIOBus,
			self.opType_dstEqCmpJmp,

			self.compareOp( op, self.op_dstEqIOBus )
		)

		instructionType = muxN_(

			self.N,

			self.opType_intAck,
			instructionType_p,

			and_( interruptRequested, interruptsEnabled )
		)

		microAddress = instructionType + microStep   # 3bits(8) + 2bits(4)

		microInstruction = self.microcodeROM.read( microAddress )


		# Control signals -

		c_cInst                              = microInstruction[ .. ]
		c_ARegisterWr                        = microInstruction[ .. ]
		c_ARegisterInSel_instructionRegister = microInstruction[ .. ]
		c_AARegisterWr                       = microInstruction[ .. ]
		c_instructionRegisterWr              = microInstruction[ .. ]
		c_PCIncrement                        = microInstruction[ .. ]
		c_PCWr                               = microInstruction[ .. ]
		c_PCInSel_ISRHandler                 = microInstruction[ .. ]
		c_readIODatabus                      = microInstruction[ .. ]
		c_dstInSel_IOInputRegister           = microInstruction[ .. ]
		c_enableInterrupts                   = microInstruction[ .. ]
		c_disableInterrupts                  = microInstruction[ .. ]
		c_acknowledgeInterrupt               = microInstruction[ .. ]
		c_servicedInterrupt                  = microInstruction[ .. ]
		c_enableRegisterBackup               = microInstruction[ .. ]
		c_disableRegisterBackup              = microInstruction[ .. ]
		c_restoreRegisters                   = microInstruction[ .. ]


		# Hold value over time (via register), but switch immediately with control signal
		'''
			     en | 100x
			    dis | 001x
			 regOut | x110
			desired | 110x
		'''
		interruptsEnabled = and_(

			or_( c_enableInterrupts, self.interruptsEnabled_ff.read() ),
			not_( c_disableInterrupts )
		)
		interruptAcknowledged = and_(

			or_( c_acknowledgeInterrupt, self.interruptAcknowledged_ff.read() ),
			not_( c_servicedInterrupt )
		)
		backupEnabled = and_(

			or_( c_enableRegisterBackup, self.backupEnabled_ff.read() ),
			not_( c_disableRegisterBackup )
		)


		# x,y select -

		x = muxN4to1_(

			self.N,

			D_registerOut,
			A_registerOut,
			B_registerOut,
			dataMemoryOut,

			instruction[ self.xSel + 0 ], instruction[ self.xSel + 1 ]
		)

		y = muxN4to1_(

			self.N,

			D_registerOut,
			A_registerOut,
			B_registerOut,
			dataMemoryOut,

			instruction[ self.ySel + 0 ], instruction[ self.ySel + 1 ]
		)


		# ALU -

		ALU_control = self.ALUROM.read( op )

		ALU_out = ALU_( self.N, x, y, ALU_control )

		z  = ALU_out[ 0 ]  # result of computation
		zr = ALU_out[ 1 ]  # result is zero
		ng = ALU_out[ 2 ]  # result is negative


		# Jump -

		jump = muxN8to1_(

			self.N,

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


		# Write data select -

		D_registerIn = muxN4to1_(

			self.N,

			self.zero,
			DBkp_registerOut,
			IOInput_registerOut,
			z,

			c_restoreRegisters, c_dstInSel_IOInputRegister
		)

		B_registerIn = muxN4to1_(

			self.N,

			self.zero,
			BBkp_registerOut,
			IOInput_registerOut,
			z,

			c_restoreRegisters, c_dstInSel_IOInputRegister
		)

		A_registerIn = muxN8to1_(

			self.N,

			self.zero,
			self.zero,
			self.zero,
			instruction,
			self.zero,
			ABkp_registerOut,
			IOInput_registerOut,
			z,

			c_ARegisterInSel_instructionRegister, c_restoreRegisters, c_dstInSel_IOInputRegister
		)

		AA_registerIn = andN_( self.N, instruction, self.AA_registerMask )

		IOInput_registerIn = bufferN_( self.N, c_readIODatabus, IODatabus )

		dataMemoryIn = muxN_(

			self.N,

			IOInput_registerOut,
			z,

			c_dstInSel_IOInputRegister
		)

		PCIn = muxN4to1_(

			self.N * 2,

			self.zero    + self.zero,
			PCBkp_registerOut,
			self.zero    + ISRHandlerAddress,
			upperAddress + lowerAddress,

			c_restoreRegisters, c_PCInSel_ISRHandler
		)


		# Write dst select -

		dst = decoder3to8_(   # returns ( q7, q6, q5, q4, q3, q2, q1, q0 )

			instruction[ self.dst + 0 ],
			instruction[ self.dst + 1 ],
			instruction[ self.dst + 2 ],
		)

		D_registerWr =      and_( dst[ 7 - 1 ], c_cInst )
		A_registerWr = or_( and_( dst[ 7 - 2 ], c_cInst ), c_ARegisterWr )
		B_registerWr =      and_( dst[ 7 - 3 ], c_cInst )
		dataMemoryWr =      and_( dst[ 7 - 4 ], c_cInst )

		PCWr = or_( and_( jump, c_cInst ), c_PCWr ) 


		# Write memory -

		self.D_register.write             ( clk, D_registerIn,         D_registerWr            )
		self.A_register.write             ( clk, A_registerIn,         A_registerWr            )
		self.B_register.write             ( clk, B_registerIn,         B_registerWr            )
		self.AA_register.write            ( clk, AA_registerIn,        c_AARegisterWr          )
		self.instruction_register.write   ( clk, programMemoryOut,     c_instructionRegisterWr )
		self.IOInput_register.write       ( clk, IOInput_registerIn,   c_readIODatabus         )

		self.DBkp_register.write          ( clk, D_registerIn,            and_( backupEnabled, D_registerWr            ) )
		self.ABkp_register.write          ( clk, A_registerIn,            and_( backupEnabled, A_registerWr            ) )
		self.BBkp_register.write          ( clk, B_registerIn,            and_( backupEnabled, B_registerWr            ) )
		self.AABkp_register.write         ( clk, AA_registerOut,          and_( backupEnabled, c_AARegisterWr          ) )
		self.instructionBkp_register.write( clk, instruction_registerOut, and_( backupEnabled, c_instructionRegisterWr ) )
		self.PCBkp_register.write         ( clk, instructionAddress,      and_( backupEnabled, c_instructionRegisterWr ) )

		self.interruptsEnabled_ff.doTheThing    ( clk,             c_disableInterrupts,     or_( RESET, c_enableInterrupts ),     0 )
		self.interruptAcknowledged_ff.doTheThing( clk, or_( RESET, c_servicedInterrupt ),               c_acknowledgeInterrupt,   0 )
		self.backupEnabled_ff.doTheThing        ( clk,             c_disableRegisterBackup, or_( RESET, c_enableRegisterBackup ), 0 )

		data_memory.write( clk, dataMemoryIn, dataMemoryWr, lowerAddress )	

		self.programCounter.doTheThing( clk, RESET, PCIn, PCWr, c_PCIncrement )

		self.microCounter.doTheThing( clk, RESET, microCounterIn, microCounterWr, microCounterIncrement )
