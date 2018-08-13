'''
	TODO:
		. CS (chip select) equivalent when write to memory mapped IO address
'''

'''----------------------------- Imports -----------------------------'''

# Built ins
import math

# Hack computer
from ._x__components import *
import Assembler.disassembler as dis


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
		
		self.debugMode = False

		self.N = N

		# Program counter
		self.programCounter = CounterN_( 2 * N )

		# Microstep counter
		nStepsPerInstruction = 4
		self.microCounter    = CounterN_( int( math.log( nStepsPerInstruction, 2 ) ) )

		# Microcode ROM
		nControlSignals      = 18
		nInstructionTypes    = 8
		self.nBitsInOpType   = math.ceil( math.log( nInstructionTypes, 2 ) )
		nEntriesMicrocodeROM = nInstructionTypes * nStepsPerInstruction
		self.microcodeROM    = ROMXN_( nEntriesMicrocodeROM, nControlSignals )

		# ALU ROM
		nEntriesALUROM = 32
		nBitsInFxSel   = 4
		nBitsInFxFlags = 5
		self.ALUROM    = ROMXN_( nEntriesALUROM, nBitsInFxSel + nBitsInFxFlags )
		
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
		self.op_AAimmed     = ( 1, 1, 0, 1, 1 )
		self.op_dstEqIOBus  = ( 1, 1, 1, 0, 0 )
		self.op_reti        = ( 1, 1, 1, 0, 1 )
		self.op_nop         = ( 1, 1, 1, 1, 0 )
		self.op_halt        = ( 1, 1, 1, 1, 1 )

		# Corresponds to microcode ROM base address...
		self.opType_Aimmed      = self.intToBitArray( 0, self.nBitsInOpType )
		self.opType_AAimmed     = self.intToBitArray( 1, self.nBitsInOpType )
		self.opType_dstEqCmpJmp = self.intToBitArray( 2, self.nBitsInOpType )
		self.opType_dstEqIOBus  = self.intToBitArray( 3, self.nBitsInOpType )
		self.opType_intAck      = self.intToBitArray( 4, self.nBitsInOpType )
		self.opType_reti        = self.intToBitArray( 5, self.nBitsInOpType )
		self.opType_nop         = self.intToBitArray( 6, self.nBitsInOpType )
		self.opType_halt        = self.intToBitArray( 7, self.nBitsInOpType )

		# Location of ISRHandler in program
		self.ISRHandlerAddress = self.intToBitArray( 0, 2 * N )

		# Miscellaneous
		self.zero = self.intToBitArray( 0, N )
		self.AA_registerMask = ( 0, ) * 6 + ( 1, ) * 10  # ???


		# Temp debug
		self.instructionTypeLookup = {

			( 0, 0, 0 ) : 'opType_Aimmed',
			( 0, 0, 1 ) : 'opType_AAimmed',
			( 0, 1, 0 ) : 'opType_dstEqCmpJmp',
			( 0, 1, 1 ) : 'opType_dstEqIOBus',
			( 1, 0, 0 ) : 'opType_intAck',
			( 1, 0, 1 ) : 'opType_reti',
			( 1, 1, 0 ) : 'opType_nop',
			( 1, 1, 1 ) : 'opType_halt',
		}

		self.opLookup = {

			( 1, 1, 0, 1, 1 ) : 'op_AAimmed',
			( 1, 1, 1, 0, 0 ) : 'op_dstEqIOBus',
			( 1, 1, 1, 0, 1 ) : 'op_reti',
			( 1, 1, 1, 1, 0 ) : 'op_nop',
			( 1, 1, 1, 1, 1 ) : 'op_halt',
		}

		self.ALUFxLookup = {

			( 0, 0, 0, 0, 0 ) : '0',
			( 0, 0, 0, 0, 1 ) : '1',
			( 0, 0, 0, 1, 0 ) : '-1',
			( 0, 0, 0, 1, 1 ) : 'x',
			( 0, 0, 1, 0, 0 ) : '! x',
			( 0, 0, 1, 0, 1 ) : '- x',
			( 0, 0, 1, 1, 0 ) : 'x + 1',
			( 0, 0, 1, 1, 1 ) : 'x - 1',
			( 0, 1, 0, 0, 0 ) : 'x + y',
			( 0, 1, 0, 0, 1 ) : 'x - y',
			( 0, 1, 0, 1, 0 ) : 'x & y',
			( 0, 1, 0, 1, 1 ) : 'x | y',
			( 0, 1, 1, 0, 0 ) : 'x ^ y',
			( 0, 1, 1, 0, 1 ) : 'x >> y',
			( 0, 1, 1, 1, 0 ) : 'x << y',
			( 0, 1, 1, 1, 1 ) : 'x * y',
			( 1, 0, 0, 0, 0 ) : 'x / y',
		}

		self.xyLookup = {

			( 0, 0 ) : 'D',
			( 0, 1 ) : 'A',
			( 1, 0 ) : 'B',
			( 1, 1 ) : 'M',
		}


	def intToBitArray( self, x, N ):

		z = bin( x )[ 2 : ].zfill( N )

		return tuple( map( int, z ) )


	def bitArrayToBinaryString( self, x ):

		return ''.join( map( str, x ) )


	def bitArrayToInt( self, x ):

		return int( ''.join( map( str, x ) ), 2 )


	def initInternalROM( self ):

		# Microcode ROM
		'''
			                                     |  opType_Aimmed       |  opType_AAimmed      |  opType_dstEqCmpJmp  |  opType_dstEqIOBus   |  opType_intAck       |  opType_reti         |  opType_nop          |  opType_halt         |
			                                     |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |  0  1  2  3          |
			------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			c_cInst                              |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_ARegisterWr                        |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_ARegisterInSel_instructionRegister |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_AARegisterWr                       |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_instructionRegisterWr              |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |
			c_PCIncrement                        |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |  1  0  0  0          |
			c_PCWr                               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_PCInSel_ISRHandler                 |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_readIODatabus                      |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_dstInSel_IOInputRegister           |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_enableInterrupts                   |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |
			c_disableInterrupts                  |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_acknowledgeInterrupt               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_servicedInterrupt                  |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |
			c_enableRegisterBackup               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  1  0          |  0  0  0  0          |  0  0  0  0          |
			c_disableRegisterBackup              |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_restoreRegisters                   |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  0  0          |  0  0  0  0          |  0  0  0  0          |
			c_halt                               |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  0  0  0          |  0  1  1  1          |
		'''
		# opType_Aimmed
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  0 )
		self.microcodeROM.write( 1, ( 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  1 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  2 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  3 )
		# opType_AAimmed
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  4 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  5 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  6 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  7 )
		# opType_dstEqCmpJmp
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  8 )
		self.microcodeROM.write( 1, ( 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1,  9 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 10 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 11 )
		# opType_dstEqIOBus
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 12 )
		self.microcodeROM.write( 1, ( 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 13 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 14 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 15 )
		# opType_intAck
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 16 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0 ), 1, 17 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 18 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 19 )
		# opType_reti
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 20 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0 ), 1, 21 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0 ), 1, 22 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 23 )
		# opType_nop
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 24 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 25 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 26 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 27 )
		# opType_halt
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ), 1, 28 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ), 1, 29 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ), 1, 30 )
		self.microcodeROM.write( 1, ( 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 ), 1, 31 )


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

		# if a == b, a ^ b == 0

		# submodule, dry
		c = xorN_( self.nBitsInOp, a, b )
		d = not_( orNto1_( self.nBitsInOp, c ) )
		return d


	def doTheThing( 

			self,

			computer,            # ...

			clk,                 # input
			RESET,               # input
			interruptRequested,  # input

			IODatabus            # bidirectional
		):

		'''
			. Everything happens at once/simultaneously
			. Assumes all memory modules can be read asynchronously
		'''


		# Alias -

		data_memory    = computer.data_memory
		program_memory = computer.program_memory


		# Constants -

		# Always increment microCounter
		microCounterIn        = self.zero
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

		if self.debugMode:

			print( 'instruction         {}'.format( self.bitArrayToBinaryString( instruction ) ) )
			print( '                    {}'.format( dis.disassemble( self.bitArrayToBinaryString( instruction ) ) ) )
			print( 'instructionAddress  {}'.format( self.programCounter.readDecimal() ) )
			print( 'microStep           {}'.format( self.bitArrayToInt( microStep ) ) )

		programMemoryOut = program_memory.read( self.programCounter.read() )


		# Decode -

		op = instruction[ self.op : self.op + self.nBitsInOp ]

		aInst = not_( instruction[ self.TECSInstrType ] )

		iDecode4 = muxN_(

			self.nBitsInOpType,

			self.opType_dstEqIOBus,
			self.opType_dstEqCmpJmp,

			self.compareOp( op, self.op_dstEqIOBus )
		)
		iDecode3 = muxN_(

			self.nBitsInOpType,

			self.opType_halt,
			iDecode4,

			self.compareOp( op, self.op_halt )
		)
		iDecode2 = muxN_(

			self.nBitsInOpType,

			self.opType_nop,
			iDecode3,

			self.compareOp( op, self.op_nop )
		)
		iDecode1 = muxN_(

			self.nBitsInOpType,

			self.opType_reti,
			iDecode2,

			self.compareOp( op, self.op_reti )
		)
		iDecode0 = muxN_(

			self.nBitsInOpType,

			self.opType_AAimmed,
			iDecode1,

			self.compareOp( op, self.op_AAimmed )
		)
		instructionType_p = muxN_(

			self.nBitsInOpType,

			self.opType_Aimmed,
			iDecode0,

			aInst
		)

		interruptsEnabled = 1  # TODO, fix me!

		instructionType = muxN_(

			self.nBitsInOpType,

			self.opType_intAck,
			instructionType_p,

			and_( interruptRequested, interruptsEnabled )
		)

		microAddress = instructionType + microStep   # 3bits(8) + 2bits(4)

		microInstruction = self.microcodeROM.read( microAddress )

		if self.debugMode:

			if op in self.opLookup:

				print( 'op                  {} {}'.format( op, self.opLookup[ op ] ) )

			else:

				print( 'op                  {} alu {}'.format( op, self.ALUFxLookup[ op ] ) )

			print( 'instructionType     {}       {}'.format( instructionType, self.instructionTypeLookup[ instructionType ] ) )
			# print( 'microAddr           {}'.format( microAddress ) )


		# Control signals -

		c_cInst                              = microInstruction[  0 ]
		c_ARegisterWr                        = microInstruction[  1 ]
		c_ARegisterInSel_instructionRegister = microInstruction[  2 ]
		c_AARegisterWr                       = microInstruction[  3 ]
		c_instructionRegisterWr              = microInstruction[  4 ]
		c_PCIncrement                        = microInstruction[  5 ]
		c_PCWr                               = microInstruction[  6 ]
		c_PCInSel_ISRHandler                 = microInstruction[  7 ]
		c_readIODatabus                      = microInstruction[  8 ]
		c_dstInSel_IOInputRegister           = microInstruction[  9 ]
		c_enableInterrupts                   = microInstruction[ 10 ]
		c_disableInterrupts                  = microInstruction[ 11 ]
		c_acknowledgeInterrupt               = microInstruction[ 12 ]
		c_servicedInterrupt                  = microInstruction[ 13 ]
		c_enableRegisterBackup               = microInstruction[ 14 ]
		c_disableRegisterBackup              = microInstruction[ 15 ]
		c_restoreRegisters                   = microInstruction[ 16 ]
		c_halt                               = microInstruction[ 17 ]

		if self.debugMode:

			print( 'controlSignals      ', end='' )
			if c_cInst:                              print( 'c_cInst',                              end = ' | ' )
			if c_ARegisterWr:                        print( 'c_ARegisterWr',                        end = ' | ' )
			if c_ARegisterInSel_instructionRegister: print( 'c_ARegisterInSel_instructionRegister', end = ' | ' )
			if c_AARegisterWr:                       print( 'c_AARegisterWr',                       end = ' | ' )
			if c_instructionRegisterWr:              print( 'c_instructionRegisterWr',              end = ' | ' )
			if c_PCIncrement:                        print( 'c_PCIncrement',                        end = ' | ' )
			if c_PCWr:                               print( 'c_PCWr',                               end = ' | ' )
			if c_PCInSel_ISRHandler:                 print( 'c_PCInSel_ISRHandler',                 end = ' | ' )
			if c_readIODatabus:                      print( 'c_readIODatabus',                      end = ' | ' )
			if c_dstInSel_IOInputRegister:           print( 'c_dstInSel_IOInputRegister',           end = ' | ' )
			if c_enableInterrupts:                   print( 'c_enableInterrupts',                   end = ' | ' )
			if c_disableInterrupts:                  print( 'c_disableInterrupts',                  end = ' | ' )
			if c_acknowledgeInterrupt:               print( 'c_acknowledgeInterrupt',               end = ' | ' )
			if c_servicedInterrupt:                  print( 'c_servicedInterrupt',                  end = ' | ' )
			if c_enableRegisterBackup:               print( 'c_enableRegisterBackup',               end = ' | ' )
			if c_disableRegisterBackup:              print( 'c_disableRegisterBackup',              end = ' | ' )
			if c_restoreRegisters:                   print( 'c_restoreRegisters',                   end = ' | ' )
			if c_halt:                               print( 'c_halt',                               end = ' | ' )
			print()


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

			dataMemoryOut,
			B_registerOut,
			A_registerOut,
			D_registerOut,

			instruction[ self.xSel + 0 ], instruction[ self.xSel + 1 ]
		)

		y = muxN4to1_(

			self.N,

			dataMemoryOut,
			B_registerOut,
			A_registerOut,
			D_registerOut,

			instruction[ self.ySel + 0 ], instruction[ self.ySel + 1 ]
		)


		# ALU -

		ALU_control = self.ALUROM.read( op )

		ALU_out = ALU_( self.N, x, y, ALU_control )

		z  = ALU_out[ 0 ]  # result of computation
		zr = ALU_out[ 1 ]  # result is zero
		ng = ALU_out[ 2 ]  # result is negative

		if self.debugMode:

			# print( 'ALU_control         {}'.format( ALU_control ) )
			print( 'x                   {} {} {}'.format( x, self.xyLookup[ instruction[ self.xSel : self.xSel + 2 ] ], self.bitArrayToInt( x ) ) )
			print( 'y                   {} {} {}'.format( y, self.xyLookup[ instruction[ self.ySel : self.ySel + 2 ] ], self.bitArrayToInt( y ) ) )
			print( 'z                   {}   {}'.format( z, self.bitArrayToInt( z ) ) )


		# Jump -

		jump = mux8to1_(

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

		IOInput_registerIn = bufferN_( self.N, IODatabus, c_readIODatabus )

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
			self.zero    + self.ISRHandlerAddress,
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

		if self.debugMode:

			print( 'dataMemoryWr        {}'.format( dataMemoryWr ) )
			print( 'dataMemoryIn        {} {}'.format( dataMemoryIn, self.bitArrayToInt( dataMemoryIn ) ) )
			# print( 'lowerAddress', lowerAddress )

		self.programCounter.doTheThing( clk, RESET, PCIn, PCWr, c_PCIncrement )

		self.microCounter.doTheThing( clk, RESET, microCounterIn, microCounterWr, microCounterIncrement )

		if self.debugMode:

			print( 'ARegOut             {}'.format( self.A_register.readDecimal() ) )
			print( 'DRegOut             {}'.format( self.D_register.readDecimal() ) )
			print( 'BRegOut             {}'.format( self.B_register.readDecimal() ) )

			# print( 'mem_16 ', data_memory.readDecimal( 16 ) )
			# print( 'mem_17 ', data_memory.readDecimal( 17 ) )
			# print( 'mem_0  ', data_memory.readDecimal( 0 ) )
			# print( 'mem_1  ', data_memory.readDecimal( 1 ) )
			print()


		# Set output signals -

		computer.halted = c_halt
