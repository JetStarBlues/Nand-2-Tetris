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

# Generate assembly and binary files
compileBinaries = True
# compileBinaries = False

OSClasses = [  # ordered by dependency

	"GlobalConstants",
	"DataMemory",
	"Array",
	"Math",
	"Font",
	"Colors",
	"GFX",
	"String",
	"Keyboard",
	"Mouse",
	"Sys",
]

OS_HLPath = '../N2T_Code/OS'
OS_VMPath = '../N2T_Code/Programs/precompiledOS'

OS_HLFiles = [ '{}/{}.jack'.format( OS_HLPath, c ) for c in OSClasses ]
OS_VMFiles = [ '{}/{}.vm'.format( OS_VMPath, c ) for c in OSClasses ]


# def dirContains  # TODO? check if VM only ASM only


def hl_to_bin( inputDirPath ):


	# Generate VM files and return includes
	print( 'Generating VM files...' )
	hl2vm.genVMFiles( 

		inputDirPath,
		libInputPaths = OS_HLFiles,
		libOutputPath = OS_VMPath,
		useTECSCompatibleVM = useTECSCompatibleVM,
		useBespokeCompatibleVM = useBespokeCompatibleVM
	)

	# Generate VMX file
	print( 'Generating VMX file...' )
	# vm2vmx.genVMXFile( inputDirPath )
	vm2vmx.genVMXFile( inputDirPath, libraryPaths = OS_VMFiles )

	if compileBinaries:

		# Generate ASM file
		print( 'Generating assembly file...' )
		# vm2asm.genASMFile( inputDirPath )
		vm2asm.genASMFile( inputDirPath, libraryPaths = OS_VMFiles )
		# vm2asm.genASMFile( inputDirPath, libraryPaths = OS_VMFiles, debug = True )

		# Generate BIN file
		print( 'Generating binary file...' )
		asm2bin.genBINFile( inputDirPath )
		# asm2bin.genBINFile( inputDirPath, debug = True )

	print( 'Done!' )
