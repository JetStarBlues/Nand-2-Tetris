'''------------------------------ Imports ------------------------------'''

import Assembler.hl2bin
import Assembler.asm2bin
import Emulators.cpuEmulator

import sys


'''------------------------------- Main -------------------------------'''

# inputDirPath = '../N2T_Code/Programs/EmulatorTests/simple'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/variableOrder'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/multiclass'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/accurateComps'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/includesOfIncludes'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/nonExistMethods'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/Point'
# inputDirPath = '../N2T_Code/Programs/LibraryTests/HashTable'
# inputDirPath = '../N2T_Code/Programs/LibraryTests/LinkedList'
# inputDirPath = '../N2T_Code/Programs/ByOthers/TECS/Pong/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/Creature/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/floatingPoint/sanity'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/floatingPoint/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/Trigonometry/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASchunky'
# inputDirPath = '../N2T_Code/Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASscroller'
# inputDirPath = '../N2T_Code/Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASboing'
# inputDirPath = '../N2T_Code/Programs/General/colorImages/lp'
# inputDirPath = '../N2T_Code/Programs/General/colorImages/sunset'
# inputDirPath = '../N2T_Code/Programs/General/hello'
# inputDirPath = '../N2T_Code/Programs/General/4BitDemo'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/sys'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/string'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/memory'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/math'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/keyboard'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/gfx'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/array'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/font'
# inputDirPath = '../N2T_Code/Programs/precompiledOS'

# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test1_add'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test2_flip'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test3_add'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test4_gt0'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test5_array'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test5a_array'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test6_mult'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test7_fill'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test8_rect_cmd'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test8_rect_buffer'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test11_xor'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test12_shiftLeft'
# inputDirPath = '../N2T_Code/Programs/Assembly/Tests/test13_shiftRight'
inputDirPath = '../N2T_Code/Programs/Assembly/Demos/demo_eo6_buffer'
# inputDirPath = '../N2T_Code/Programs/Assembly/Demos/demo_eo6_color'

if __name__ == '__main__':

	# Get args if any
	args = sys.argv[ 1 : ]

	if len( args ) == 1:

		inputDirPath = args[ 0 ]

	elif len( args ) > 1:

		raise Exception( 'Received unexpected arguments' )


	# Compile
	# Assembler.hl2bin.compileBinaries        = True
	# Assembler.hl2bin.useBespokeCompatibleVM = True
	# Assembler.hl2bin.useTECSCompatibleVM    = False

	# Assembler.hl2bin.hl_to_bin( inputDirPath )
	Assembler.asm2bin.genBINFile( inputDirPath )
	# Assembler.asm2bin.genBINFile( inputDirPath, debug = True )
	print()


	# Run
	Emulators.cpuEmulator.run( '{}/Main.bin'.format( inputDirPath ) )
