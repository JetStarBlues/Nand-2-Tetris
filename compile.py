'''------------------------------ Imports ------------------------------'''

# import Assembler.hl2vm
# import Assembler.vm2asm
# import Assembler.asm2bin

import Assembler.hl2bin


'''------------------------------- Main -------------------------------'''

# inputDirPath = '../N2T_Code/Programs/Uncategorized/gfxDriverComm'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/Point'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/nonExistMethods'
# inputDirPath = '../N2T_Code/Programs/CompilerTests/includesOfIncludes'
# inputDirPath = '../N2T_Code/Programs/HashTable'
# inputDirPath = '../N2T_Code/Programs/LinkedList'
# inputDirPath = '../N2T_Code/Programs/pong'
inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/Creature/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/floatingPoint/sanity'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/floatingPoint/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/MarkArmbrust/Trigonometry/modifiedCode'
# inputDirPath = '../N2T_Code/Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASchunky'
# inputDirPath = '../N2T_Code/Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASscroller'
# inputDirPath = '../N2T_Code/Programs/ByOthers/GavinStewart/Games&Demos/modifiedCode/GASboing'
# inputDirPath = '../N2T_Code/Programs/temp_delete'
# inputDirPath = '../colorImages/lp'
# inputDirPath = '../colorImages/sunset'
# inputDirPath = '../N2T_Code/Programs/temp_testStatics'
# inputDirPath = '../N2T_Code/Programs/hello'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/sys'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/string'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/memory'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/math'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/keyboard'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/gfx'
# inputDirPath = '../N2T_Code/Programs/OSLibTests/array'
# inputDirPath = '../N2T_Code/Programs/precompiled'
# inputDirPath = 'Programs/ByOthers/MarkArmbrust/Creature/modifiedCode'
# inputDirPath = 'Programs/ByOthers/GavinStewart/Games&Demos/GASscroller/modifiedCode'

Assembler.hl2bin.hl_to_bin( inputDirPath )

# TODO: Compile diagram assembly
# Assembler.asm2bin.genBINFile( '../../t' )
