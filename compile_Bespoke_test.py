'''------------------------------ Imports ------------------------------'''

import Assembler.asm2bin_Bespoke


'''------------------------------- Main -------------------------------'''

# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test1_add'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test2_flip'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test3_gtZero'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test4_statusRegister'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test5_array'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6_macros'
inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6b_org'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6c_defineData'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6a_lpm'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6_mult'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test7_fill'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test8_rect_buffer'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test8_rect_cmd'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test11_miscArith'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test14_linkRegister'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test15_addressVariants'

# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/OPC/fib'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/OPC/seive'


Assembler.asm2bin_Bespoke.genBINFile( inputDirPath, debug = True )
# Assembler.asm2bin_Bespoke.genBINFile( inputDirPath )
