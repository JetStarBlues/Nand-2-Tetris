'''------------------------------ Imports ------------------------------'''

import Assembler.asm2bin_Bespoke


'''------------------------------- Main -------------------------------'''

inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test1_add'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test2_flip'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test3_add'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test4_gt0'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test5_array'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test5a_array'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6_mult'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test7_fill'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test8_rect_buffer'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test8_rect_cmd'

Assembler.asm2bin_Bespoke.genBINFile( inputDirPath, debug = True )
# Assembler.asm2bin_Bespoke.genBINFile( inputDirPath )
