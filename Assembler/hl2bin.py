# ========================================================================================
#
# Description:
#	Compiles Hack HL (high level) code to Hack BIN (binary) code
#
# Attribution:
# 	Code by www.jk-quantized.com
#
# Redistributions and use of this code in source and binary forms must retain
# the above attribution notice and this condition.
#
# ========================================================================================


# == Imports =======================================================

# Built ins
import re
import os

# Hack computer
import Assembler.hl2vm as hl2vm
import Assembler.vm2asm as vm2asm
import Assembler.asm2bin as asm2bin


# == Main ==========================================================

def hl_to_bin( inputDirPath ):

	# Generate VM files
	hl2vm.genVMFiles( inputDirPath )

	# Generate ASM file
	vm2asm.genASMFile( inputDirPath )

	# Generate BIN file
	asm2bin.genBINFile( inputDirPath )

	print( 'Done' )
