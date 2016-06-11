''''''''''''''''''''''''' imports '''''''''''''''''''''''''''

# Built ins
import sys

# Hack computer
sys.path.append('../../../')
import Assembler


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

subdir = 'kv_4__computer/'

for file in files:
	# print(file)
	input = subdir + file + '.hasm'
	output = subdir + 'bin/' + file + '.bin'
	Assembler.asm_to_bin( input, output )