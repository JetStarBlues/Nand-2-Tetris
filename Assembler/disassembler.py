# == Imports =================================================

import Assembler.lookupTables as LT


# == Main ====================================================

def disassemble( instruction ):

	instruction = ''.join( map( str, instruction ) )

	disassembled = ''

	# @address
	if instruction[ 0 ] == '0' :

		disassembled = '@{}'.format( int( instruction[ 1 : ], 2 ) )

	else:

		opcode = instruction[ 1 : 6 ]

		if opcode in LT.fxType_:

			disassembled = LT.fxType_[ opcode ]

			if disassembled == 'AA_IMMED':

				disassembled = '@@{}'.format( int( instruction[ 6 : ], 2 ) )

			elif disassembled == 'DST_EQ_IOBUS':

				dest = LT.dest_[ instruction[ 10 : 13 ] ]

				disassembled = '{} = IOBUS'.format( dest )

		# dest = cmp ; jmp
		else:

			xSel = LT.xySel_[ instruction[  6 :  8 ] ]
			ySel = LT.xySel_[ instruction[  8 : 10 ] ]
			dest = LT.dest_[  instruction[ 10 : 13 ] ]
			jump = LT.jump_[  instruction[ 13 : 16 ] ]

			comp = LT.comp_[ opcode ]
			comp = comp.replace( 'x', xSel )
			comp = comp.replace( 'y', ySel )

			if dest != 'NULL':

				disassembled = '{} = '.format( dest )

			disassembled += comp

			if jump != 'NULL':

				disassembled += ' ; {}'.format( jump )

	return disassembled
