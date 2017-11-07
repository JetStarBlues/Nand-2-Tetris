'''------------------------------ Imports ------------------------------'''

from Assembler.hl2bin import *


'''------------------------------- Main -------------------------------'''

inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/pong'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/cadet/Creature'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/gav/GASchunky'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/gav/GASscroller'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/gav/GASboing'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/temp_delete'
# inputDirPath = '../colorImages/lpTest/lpTest'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/temp_testStatics'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/hello'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/sys'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/string'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/memory'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/math'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/keyboard'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/gfx'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/OSLibTests/array'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/includesOfincludes'
# inputDirPath = '../tempNotes/MyCompilerOut/OS_standalone/precompiled'
# inputDirPath = 'Programs/ByOthers/MarkArmbrust/Creature/modifiedCode'
# inputDirPath = 'Programs/ByOthers/GavinStewart/Games&Demos/GASscroller/modifiedCode'

hl_to_bin( inputDirPath )
