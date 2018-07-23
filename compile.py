'''------------------------------ Imports ------------------------------'''

# import Assembler.hl2vm
# import Assembler.vm2asm
# import Assembler.asm2bin

import Assembler.hl2bin


'''------------------------------- Main -------------------------------'''

inputDirPath = '../N2T_Code/Programs/CompilerTests/accurateComps'
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
# inputDirPath = '../N2T_Code/Programs/OSLibTests/sys'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/string'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/memory'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/math'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/keyboard'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/gfx'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/array'
# inputDirPath = '../N2T_Code/Programs/precompiledOS'

Assembler.hl2bin.hl_to_bin( inputDirPath )

# TODO: Compile diagram assembly
# Assembler.asm2bin.genBINFile( '../../t' )
