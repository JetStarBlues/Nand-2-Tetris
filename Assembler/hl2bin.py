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
import Assembler.vm2vmx as vm2vmx


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

		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/Array.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/DataMemory.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/Font.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/GFX.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/GlobalConstants.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/Keyboard.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/Math.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/String.vm',
		# '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/Sys.vm',

		#TODO... use precompiled ASM file instead...
	]

	# Generate VM files and return includes
	print( 'Generating VM files...' )
	VM_includes.extend( hl2vm.genVMFiles( inputDirPath ) )

	# Generate VMX file
	print( 'Generating VMX file...' )
	# vm2vmx.genVMXFile( inputDirPath )
	vm2vmx.genVMXFile( inputDirPath, libraryPaths = VM_includes )

	# Generate ASM file
	# print( 'Generating assembly file...' )
	# vm2asm.genASMFile( inputDirPath )
	# vm2asm.genASMFile( inputDirPath, libraryPaths = VM_includes )
	# vm2asm.genASMFile( inputDirPath, libraryPaths = VM_includes, debug = True )

	# Generate BIN file
	# print( 'Generating binary file...' )
	# asm2bin.genBINFile( inputDirPath )
	# asm2bin.genBINFile( inputDirPath, debug = True )

	print( 'Done!' )
