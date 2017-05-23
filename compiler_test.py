'''------------------------------ Imports ------------------------------'''

# Hack computer
from Components import *
from Assembler.hl2bin import *


'''------------------------------- Main -------------------------------'''

inputDirPath = 'C:/Users/Janet/Desktop/tempNotes/MyCompilerOut/OS_standalone/hello'
# inputDirPath = 'C:/Users/Janet/Desktop/tempNotes/MyCompilerOut/OS_standalone/math'
# inputDirPath = 'C:/Users/Janet/Desktop/tempNotes/MyCompilerOut/OS_standalone/precompiled'
# inputDirPath = 'Programs/Tests/Chapter_12'
# inputDirPath = 'Programs/ByOthers/MarkArmbrust/Creature'
# inputDirPath = 'Programs/ByOthers/GavinStewart/GASscroller'

hl_to_bin( inputDirPath )
