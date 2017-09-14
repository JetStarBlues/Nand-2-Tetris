'''------------------------------ Imports ------------------------------'''

# Built ins
import os

# Hack computer
import Assembler.hl2vm as hl2vm
import Assembler.vm2asm as vm2asm


'''------------------------------- Main -------------------------------'''

inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/precompiled'

# Generate VM files
print( 'Generating VM files...' )
hl2vm.genVMFiles( inputDirPath )

# Remove 'Main.vm'
os.remove( 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/precompiled/Main.vm' )

# Generate ASM file
print( 'Generating assembly file...' )
vm2asm.genASMFile( inputDirPath, debug = True )

print( 'Done!' )
