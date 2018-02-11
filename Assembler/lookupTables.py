'''------------------------------ Imports ------------------------------'''

import Components._0__globalConstants as GC


'''----------------------------- Main -----------------------------------'''

comp = {

	# fub1, fub0, ySel, zx, nx, zy, ny, f, no
	'0'    : '110101010',
	'1'    : '110111111',
	'-1'   : '110111010',
	'D'    : '110001100',
	'A'    : '110110000',
	'!D'   : '110001101',
	'!A'   : '110110001',
	'-D'   : '110001111',
	'-A'   : '110110011',
	'D+1'  : '110011111',
	'A+1'  : '110110111',
	'D-1'  : '110001110',
	'A-1'  : '110110010',
	'D+A'  : '110000010',
	'A+D'  : '110000010',  # order doesn't matter
	'D-A'  : '110010011',
	'A-D'  : '110000111',
	'D&A'  : '110000000',
	'A&D'  : '110000000',  # order doesn't matter
	'D|A'  : '110010101',
	'A|D'  : '110010101',  # order doesn't matter
	'M'    : '111110000',
	'!M'   : '111110001',
	'-M'   : '111110011',
	'M+1'  : '111110111',
	'M-1'  : '111110010',
	'D+M'  : '111000010',
	'M+D'  : '111000010',  # order doesn't matter
	'D-M'  : '111010011',
	'M-D'  : '111000111',
	'D&M'  : '111000000',
	'M&D'  : '111000000',  # order doesn't matter
	'D|M'  : '111010101',
	'M|D'  : '111010101',  # order doesn't matter

	'D^M'  : '101000000',
	'M^D'  : '101000000',  # order doesn't matter
	'D^A'  : '100000000',
	'A^D'  : '100000000',  # order doesn't matter
	'D<<M' : '011000000',
	'D<<A' : '010000000',  # not used, can omit to free instruction code
	'D>>M' : '001000000',
	'D>>A' : '000000000',  # not used, can omit to free instruction code
}

dest = {
	
	# d3, d2, d1
	'NULL' : '000',
	'M'    : '001',
	'D'    : '010',
	'A'    : '100',
	'DM'   : '011',
	'MD'   : '011',  # order doesn't matter
	'AM'   : '101',
	'MA'   : '101',  # order doesn't matter
	'AD'   : '110',
	'DA'   : '110',  # order doesn't matter
	'MDA'  : '111',
	'MAD'  : '111',  # order doesn't matter
	'AMD'  : '111',  # order doesn't matter
	'ADM'  : '111',  # order doesn't matter
	'DMA'  : '111',  # order doesn't matter
	'DAM'  : '111'   # order doesn't matter
}

jump = {
	
	# j3, j2, j1
	'NULL' : '000',
	'JGT'  : '001',
	'JEQ'  : '010',
	'JLT'  : '100',
	'JGE'  : '011',
	'JLE'  : '110',
	'JNE'  : '101',
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