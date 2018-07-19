# ========================================================================================
#
#  Description:
#
#    Compiles Hack HL (high level) code to Hack BIN (binary) code
#
#  Attribution:
#
#    Code by www.jk-quantized.com
#
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
#
# ========================================================================================


# == Imports =======================================================

import Assembler.hl2vm as hl2vm
import Assembler.vm2asm as vm2asm
import Assembler.vm2vmx as vm2vmx
import Assembler.asm2bin as asm2bin


# == Main ==========================================================

# Use VM instructions that are compatible with the official TECS specifications
# useTECSCompatibleVM = True
useTECSCompatibleVM = False

# Use VM instructions that are compatible with our bespoke CPU
useBespokeCompatibleVM = True
# useBespokeCompatibleVM = False

compileBinaries = True  # Generate assembly and binary files
# compileBinaries = False

OSPath = '../N2T_Code/Programs/precompiledOS'


def compileOS():

	# Generate VM files
	print( 'Generating OS VM files...' )
	hl2vm.genVMFiles( OSPath, useTECSCompatibleVM, useBespokeCompatibleVM )


def hl_to_bin( inputDirPath ):

	# Compile OS
	compileOS()

	VM_includes = [

		OSPath + '/GlobalConstants.vm',
		OSPath + '/Array.vm',
		OSPath + '/DataMemory.vm',
		OSPath + '/Math.vm',
		OSPath + '/Font.vm',
		OSPath + '/Colors.vm',
		OSPath + '/GFX.vm',
		OSPath + '/Keyboard.vm',
		OSPath + '/String.vm',
		OSPath + '/Sys.vm',
	]

	# Generate VM files and return includes
	print( 'Generating VM files...' )
	VM_includes.extend( hl2vm.genVMFiles( inputDirPath, useTECSCompatibleVM, useBespokeCompatibleVM ) )

	# Generate VMX file
	print( 'Generating VMX file...' )
	# vm2vmx.genVMXFile( inputDirPath )
	vm2vmx.genVMXFile( inputDirPath, libraryPaths = VM_includes )

	if compileBinaries:

		# Generate ASM file
		print( 'Generating assembly file...' )
		# vm2asm.genASMFile( inputDirPath )
		vm2asm.genASMFile( inputDirPath, libraryPaths = VM_includes )
		# vm2asm.genASMFile( inputDirPath, libraryPaths = VM_includes, debug = True )

		# Generate BIN file
		print( 'Generating binary file...' )
		asm2bin.genBINFile( inputDirPath )
		# asm2bin.genBINFile( inputDirPath, debug = True )

	print( 'Done!' )
