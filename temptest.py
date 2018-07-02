# import Assembler.disassembler as dis

# print( dis.disassemble( '0000000100000000' ) )  #@256
# print( dis.disassemble( '1110110000010000' ) )  # D=A

import Assembler.asm2bin as ass

ass.asm_to_bin (
	'C:/Users/Janet/Desktop/Hack/N2T/Programs/Demos/eo6/demo_eo6.asm',
	'C:/Users/Janet/Desktop/Hack/N2T/Programs/Demos/eo6/bin/demo_eo6.bin',
)