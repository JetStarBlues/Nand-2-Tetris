# ========================================================================================
#
# Description:
#	Compiles Hack HL (high level) code to Hack BIN (binary) code
#
# Attribution:
# 	Code by www.jk-quantized.com
#
# Redistribution and use of this code in source and binary forms must retain
# the above attribution notice and this condition.
#
# ========================================================================================


# == Imports =======================================================

import Assembler.hl2vm as hl2vm
import Assembler.vm2asm as vm2asm
import Assembler.asm2bin as asm2bin


# == Main ==========================================================

def hl_to_bin( inputDirPath ):

	VM_includes = [

		# OS files
		# 'Programs/Libraries/OS/Array.vm',
		# 'Programs/Libraries/OS/Keyboard.vm',
		# 'Programs/Libraries/OS/Math.vm',
		# 'Programs/Libraries/OS/Memory.vm',
		# 'Programs/Libraries/OS/Output.vm',
		# 'Programs/Libraries/OS/Screen.vm',
		# 'Programs/Libraries/OS/String.vm',
		# 'Programs/Libraries/OS/Sys.vm',

		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/Array.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/DataMemory.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/Font.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/GFX.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/GlobalConstants.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiled/Keyboard.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/Math.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/String.vm',
		'../tempNotes/MyCompilerOut/OS_standalone/precompiled/Sys.vm',

		#TODO... use precompiled ASM file instead (also make fx etc that gens this on demand)...
	]

	# Generate VM files and return includes
	print( 'Generating VM files...' )
	VM_includes.extend( hl2vm.genVMFiles( inputDirPath ) )

	# Generate ASM file
	print( 'Generating assembly file...' )
	vm2asm.genASMFile( inputDirPath, libraryPaths = VM_includes, debug = False )
	# vm2asm.genASMFile( inputDirPath, libraryPaths = VM_includes, debug = True )

	# Generate BIN file
	print( 'Generating binary file...' )
	asm2bin.genBINFile( inputDirPath )

	print( 'Done!' )
