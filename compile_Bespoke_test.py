'''------------------------------ Imports ------------------------------'''

import Assembler.asm2bin_Bespoke


'''------------------------------- Main -------------------------------'''

# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test1_add'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test2_flip'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test3_comparisons'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test4_statusRegister'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test5_array'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6a_macros'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6b_org'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test6c_defineData'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test7_lpm'
inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test8_linkRegister'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test9_addressVariants'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test10_miscArith'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test11_interrupt'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test11a_interruptsRTI'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test11b_interruptsSWI'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test990_fill'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test991_rect_cmd'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/Tests/test992_rect_buffer'

# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/OPC/fib'
# inputDirPath = '../N2T_Code/Programs/Assembly/Assembly/OPC/sieve'


Assembler.asm2bin_Bespoke.genBINFile( inputDirPath, debug = True )
# Assembler.asm2bin_Bespoke.genBINFile( inputDirPath )
