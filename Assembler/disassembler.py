# TODO: Update for new ISA

# == Imports =================================================

import Assembler.lookupTables as LT


# == Main ====================================================

def disassemble( instruction ):

	instruction = ''.join( map( str, instruction ) )

	disassembled = ''

	# @address
	if instruction[0] == '0' :

		disassembled = '@{}'.format( int( instruction[ 1 : ], 2 ) )

	# dest = cmp ; jmp
	else :

		comp = LT.comp_[ instruction[  1 : 10 ] ]
		dest = LT.dest_[ instruction[ 10 : 13 ] ]
		jump = LT.jump_[ instruction[ 13 : 16 ] ]

		if dest != 'NULL':
			disassembled += dest + ' = '

		disassembled += comp

		if jump != 'NULL':
			disassembled += ' ; ' + jump

	return disassembled