'''------------------------------ Imports ------------------------------'''

# Built ins
import os

# Hack computer
import Assembler.hl2vm as hl2vm
# import Assembler.vm2asm as vm2asm


'''------------------------------- Main -------------------------------'''

inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS'

# Generate VM files
print( 'Generating OS VM files...' )
hl2vm.genVMFiles( inputDirPath )

# Remove 'Main.vm'
# os.remove( '../tempNotes/MyCompilerOut/OS_standalone/precompiledOS/Main.vm' )

print( 'Done!' )
