'''------------------------------ Imports ------------------------------'''

import Components._0__globalConstants as GC


'''----------------------------- Main -----------------------------------'''

xySel = {

	'D' : '00',
	'A' : '01',
	'B' : '10',
	'M' : '11',
}

fxType = {
	
	'AA_IMMED'     : '11100',
	'DST_EQ_IOBUS' : '11101',
	'RETI'         : '11110',
	'NOP'          : '11111',
}

comp = {

	'0'                   : '00000',
	'1'                   : '00001',
	'-1'                  : '00010',
	'([DABM])'            : '00011',  # x
	'!([DABM])'           : '00100',  # ! x
	'-([DABM])'           : '00101',  # - x
	'([DABM])\+1'         : '00110',  # x + 1
	'([DABM])-1'          : '00111',  # x - 1
	'([DABM])\+([DABM])'  : '01000',  # x + y
	'([DABM])-([DABM])'   : '01001',  # x - y
	'([DABM])&([DABM])'   : '01010',  # x & y
	'([DABM])\|([DABM])'  : '01011',  # x | y
	'([DABM])\^([DABM])'  : '01100',  # x ^ y
	'([DABM])>>([DABM])'  : '01101',  # x >> y
	'([DABM])<<([DABM])'  : '01110',  # x << y
	'([DABM])\*([DABM])'  : '01111',  # x * y
	'([DABM])/([DABM])'   : '10000',  # x / y
}

dest = {

	'NULL' : '000',
	'D'    : '001',
	'A'    : '010',
	'B'    : '011',
	'M'    : '100',
}

jump = {

	'NULL' : '000',
	'JGT'  : '001',
	'JEQ'  : '010',
	'JGE'  : '011',
	'JLT'  : '100',
	'JNE'  : '101',
	'JLE'  : '110',
	'JMP'  : '111'
}

globalAddresses = {

	'@R0'     : '@0',   # SP
	'@R1'     : '@1',   # LCL
	'@R2'     : '@2',   # ARG
	'@R3'     : '@3',   # THIS
	'@R4'     : '@4',   # THAT
	'@R5'     : '@5',   # TEMP
	'@R6'     : '@6',   # TEMP
	'@R7'     : '@7',   # TEMP
	'@R8'     : '@8',   # TEMP
	'@R9'     : '@9',   # TEMP
	'@R10'    : '@10',  # TEMP
	'@R11'    : '@11',  # TEMP
	'@R12'    : '@12',  # TEMP
	'@R13'    : '@13',  # GP
	'@R14'    : '@14',  # GP
	'@R15'    : '@15',  # GP

	'@SP'     : '@0',
	'@LCL'    : '@1',
	'@ARG'    : '@2',
	'@THIS'   : '@3',
	'@THAT'   : '@4',
	'@TEMP'   : '@5',
	'@GP'     : '@13',

	'@SCREEN' : '@' + str( GC.SCREEN_MEMORY_MAP ),
	'@KBD'    : '@' + str( GC.KBD_MEMORY_MAP ),
}

def flip( d ):

	return { v : k for k, v in d.items() }

comp_ = flip( comp )
dest_ = flip( dest )
jump_ = flip( jump )