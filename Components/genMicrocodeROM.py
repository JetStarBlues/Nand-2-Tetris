# __ Specify types and order ______________

instructionTypes = [

	'i_intAck',
	'i_cInstruction',
	'i_AImmediate',
	'i_AAImmediate',
	'i_rdIODatabus',
	'i_reti',
	'i_nop',
	'i_halt',
]

controlBits = [

	'c_cInstruction',
	'c_ARegisterWr',
	'c_ARegisterInSel_instructionRegister',
	'c_AARegisterWr',
	'c_instructionRegisterWr',
	'c_ProgramCounterIncrement',
	'c_ProgramCounterWr',
	'c_ProgramCounterInSel_ISRHandler',
	'c_rdIODatabus',
	'c_enableInterrupts',
	'c_disableInterrupts',
	'c_acknowledgeInterrupt',
	'c_servicedInterrupt',
	'c_enableRegisterBackup',
	'c_disableRegisterBackup',
	'c_restoreRegisters',
	'c_halt',
]


# __ Defaults _____________________________

fetch = {

	'c_cInstruction'                       : 0,
	'c_ARegisterWr'                        : 0,
	'c_ARegisterInSel_instructionRegister' : 0,
	'c_AARegisterWr'                       : 0,
	'c_instructionRegisterWr'              : 1,
	'c_ProgramCounterIncrement'            : 1,
	'c_ProgramCounterWr'                   : 0,
	'c_ProgramCounterInSel_ISRHandler'     : 0,
	'c_rdIODatabus'                        : 0,
	'c_enableInterrupts'                   : 0,
	'c_disableInterrupts'                  : 0,
	'c_acknowledgeInterrupt'               : 0,
	'c_servicedInterrupt'                  : 0,
	'c_enableRegisterBackup'               : 0,
	'c_disableRegisterBackup'              : 0,
	'c_restoreRegisters'                   : 0,
	'c_halt'                               : 0,
}

default = {

	'c_cInstruction'                       : 0,
	'c_ARegisterWr'                        : 0,
	'c_ARegisterInSel_instructionRegister' : 0,
	'c_AARegisterWr'                       : 0,
	'c_instructionRegisterWr'              : 0,
	'c_ProgramCounterIncrement'            : 0,
	'c_ProgramCounterWr'                   : 0,
	'c_ProgramCounterInSel_ISRHandler'     : 0,
	'c_rdIODatabus'                        : 0,
	'c_enableInterrupts'                   : 0,
	'c_disableInterrupts'                  : 0,
	'c_acknowledgeInterrupt'               : 0,
	'c_servicedInterrupt'                  : 0,
	'c_enableRegisterBackup'               : 0,
	'c_disableRegisterBackup'              : 0,
	'c_restoreRegisters'                   : 0,
	'c_halt'                               : 0,
}


# __ Init all as nops _____________________

nSteps = 4

mCode = {}

for instr in instructionTypes:

	mCode[ instr ] = []

	mCode[ instr ].append( fetch.copy() )

	for i in range( nSteps - 1 ):

		mCode[ instr ].append( default.copy() )		


# __ Specialize ___________________________

# i_intAck

## save state
mCode[ 'i_intAck' ][ 1 ][ 'c_disableInterrupts'    ] = 1
mCode[ 'i_intAck' ][ 1 ][ 'c_enableRegisterBackup' ] = 1  # TODO, redact c_disableRegisterBackup
mCode[ 'i_intAck' ][ 1 ][ 'c_acknowledgeInterrupt' ] = 1  # caller should place ISR# in IO databus (downside bus not available for ISR...)

## save ISR number
# TODO, redact c_disableRegisterBackup
mCode[ 'i_intAck' ][ 1 ][ 'c_BRegisterWr'  ] = 1  # read IOdatabus...?
mCode[ 'i_intAck' ][ 1 ][ 'c_BRegisterInSel_??iodbus'  ] = 1

## goto ISR handler
mCode[ 'i_intAck' ][ 2 ][ 'c_ProgramCounterWr'               ] = 1
mCode[ 'i_intAck' ][ 2 ][ 'c_ProgramCounterInSel_ISRHandler' ] = 1  # goto ISR


# i_cInstruction
mCode[ 'i_cInstruction' ][ 1 ][ 'c_cInstruction' ] = 1


# i_AImmediate
mCode[ 'i_AImmediate' ][ 1 ][ 'c_ARegisterWr'                        ] = 1
mCode[ 'i_AImmediate' ][ 1 ][ 'c_ARegisterInSel_instructionRegister' ] = 1


# i_AAImediate
mCode[ 'i_AAImmediate' ][ 1 ][ 'c_AARegisterWr' ] = 1


# i_rdIODatabus
mCode[ 'i_rdIODatabus' ][ 1 ][ 'c_cInstruction' ] = 1
mCode[ 'i_rdIODatabus' ][ 1 ][ 'c_rdIODatabus'  ] = 1  # xySel invalid, dst valid, jmp NULL


# i_reti
mCode[ 'i_reti' ][ 1 ][ 'c_restoreRegisters'     ] = 1

mCode[ 'i_reti' ][ 2 ][ 'c_enableInterrupts'     ] = 1
mCode[ 'i_reti' ][ 2 ][ 'c_servicedInterrupt'    ] = 1
mCode[ 'i_reti' ][ 2 ][ 'c_enableRegisterBackup' ] = 1


# i_halt
mCode[ 'i_halt' ][ 1 ][ 'c_halt' ] = 1  # stored in ff
mCode[ 'i_halt' ][ 2 ][ 'c_halt' ] = 1  # whyNot?
mCode[ 'i_halt' ][ 3 ][ 'c_halt' ] = 1  # whyNot?


# __ Generate ROM _________________________

print( 'nIstructions {}'.format( len( instructionTypes ) ) )
print( 'nControlBits {}'.format( len( controlBits ) ) )

n = 0

for instr in instructionTypes:

	print( '# {}'.format( instr ) )

	m = mCode[ instr ]

	for i in range( nSteps ):

		s = m[ i ]

		bits = [ s[ cBit ] for cBit in controlBits ]

		print( '( {} ), {:2}'.format(

			', '.join( map( str, bits ) ),
			n
		) )

		n += 1

