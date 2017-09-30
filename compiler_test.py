'''------------------------------ Imports ------------------------------'''

from Assembler.hl2bin import *


'''------------------------------- Main -------------------------------'''

inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/math_ex'
# inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/hello_ex'
# inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/includesOfincludes'
# inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/hello'
# inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/gfx'
# inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/math'
# inputDirPath = 'C:/Users/Janet/Desktop/Hack/tempNotes/MyCompilerOut/OS_standalone/precompiled'
# inputDirPath = 'Programs/Tests/Chapter_12'
# inputDirPath = 'Programs/ByOthers/MarkArmbrust/Creature'
# inputDirPath = 'Programs/ByOthers/GavinStewart/GASscroller'

hl_to_bin( inputDirPath )
