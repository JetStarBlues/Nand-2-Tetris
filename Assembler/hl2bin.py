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
useTECSCompatibleVM = False

# Use VM instructions that are compatible with our bespoke CPU
useBespokeCompatibleVM = True

# Generate VMX file (used by VMEmulator)
compileVMX = True

# Generate assembly and binary files
compileBinaries = True

# Use standard library files
useStandardLibrary = True

stdLibClasses = [  # ordered by dependency

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

stdLib_HLPath = '../N2T_Code/OS'
stdLib_VMPath = '../N2T_Code/Programs/precompiledOS'

stdLib_HLFiles = [ '{}/{}.jack'.format( stdLib_HLPath, c ) for c in stdLibClasses ]
stdLib_VMFiles = [ '{}/{}.vm'.format( stdLib_VMPath, c )   for c in stdLibClasses ]


def hl_to_bin( inputDirPath ):

	# Helper... location of Sys.halt in asm/bin
	sysHaltAddress = None

	# Ignore standard library
	if not useStandardLibrary:

		stdLib_HLPath  = None
		stdLib_VMPath  = None
		stdLib_HLFiles = None
		stdLib_VMFiles = None

	# Generate VM files and return includes
	print( 'Generating VM files...' )
	hl2vm.genVMFiles( 

		inputDirPath,
		libInputPaths          = stdLib_HLFiles,
		libOutputPath          = stdLib_VMPath,
		useTECSCompatibleVM    = useTECSCompatibleVM,
		useBespokeCompatibleVM = useBespokeCompatibleVM
	)

	if compileVMX:

		# Generate VMX file
		print( 'Generating VMX file...' )
		# vm2vmx.genVMXFile( inputDirPath )
		vm2vmx.genVMXFile( inputDirPath, libraryPaths = stdLib_VMFiles )

	if compileBinaries:

		# Generate ASM file
		print( 'Generating assembly file...' )
		vm2asm.genASMFile( inputDirPath, libraryPaths = stdLib_VMFiles )
		# vm2asm.genASMFile( inputDirPath, libraryPaths = stdLib_VMFiles, debug = True )

		# Generate BIN file
		print( 'Generating binary file...' )
		# sysHaltAddress = asm2bin.genBINFile( inputDirPath )
		sysHaltAddress = asm2bin.genBINFile( inputDirPath, debug = True )

	print( 'Done!' )

	return sysHaltAddress
