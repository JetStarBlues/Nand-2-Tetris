''''''''''''''''''''''''' imports '''''''''''''''''''''''''''

# import Assembler...


''''''''''''''''''''''''''' main '''''''''''''''''''''''''''''

# asm_to_bin( 'test1.hasm', 'bin/test.bin' )


files = [
	'test1_addTo',
	'test2_flip',
	'test3_add',
	'test4_gt0',
	'test5_array',
	'test5a_array',
	'test6_mult',
	'test8_fill',
	'test9_rect',
]

for file in files:
	print(file)
	in_ = file + '.hasm'
	out_ = 'bin/' + file + '.bin'
	asm_to_bin( in_, out_ )