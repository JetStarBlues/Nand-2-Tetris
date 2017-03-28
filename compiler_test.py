'''------------------------------ Imports ------------------------------'''

# Hack computer
from Components import *
from Assembler.hl2bin import *


'''------------------------------- Main -------------------------------'''


inputDirPath = 'C:/Users/Janet/Desktop/tempNotes/MyCompilerOut/languageTest'
# inputDirPath = 'Programs/Tests/Chapter_12'
# inputDirPath = 'Programs/ByOthers/MarkArmbrust/Creature'
# inputDirPath = 'Programs/ByOthers/GavinStewart/GASscroller'

hl_to_bin( inputDirPath )
