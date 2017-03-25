'''------------------------------ Imports ------------------------------'''

# Hack computer
from Components import *
from Assembler.hl2bin import *


'''------------------------------- Main -------------------------------'''

libs = [

	'Programs/Libraries/OS'
]

inputDirPath = 'Programs/Tests/Chapter_12'
# inputDirPath = 'Programs/ByOthers/MarkArmbrust/Creature'
# inputDirPath = 'Programs/ByOthers/GavinStewart/GASscroller'

hl_to_bin( inputDirPath, libs )
