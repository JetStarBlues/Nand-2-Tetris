'''------------------------------ Imports ------------------------------'''

# Built ins
import os

# Hack computer
from Components import *



'''------------------------------ Setup --------------------------------'''

# programPath = 'Programs/Tests/Chapter_12/Main.bin'
# programPath = 'Programs/ByOthers/MarkArmbrust/Creature/Main.bin'
# programPath = 'Programs/ByOthers/GavinStewart/GASchunky/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/hello_ex/Main.bin'
programPath = '../tempNotes/MyCompilerOut/OS_standalone/math_ex/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/math/Main.bin'
# programPath = 'Programs/Demos/bin/demo_eo6.bin'
# programPath = 'Programs/Demos/bin/demo_eo6_color.bin'

debugMode = True



'''----------------------------- Main -----------------------------------'''

# Initialize computer
computer = ComputerN_( N_BITS, DATA_MEMORY_SIZE, PROGRAM_MEMORY_SIZE )
computer.program_memory.flash( programPath )

# Initialize IO
io = IO( N_BITS, computer.data_memory )

# Initialize clock
clock = Clock()

#
def update():

	computer.run( clock.value )  # tick

	if io.hasExited:

		clock.stop()
		print( 'See you later!' )



'''------------------------------ Debug ---------------------------------'''

instructionAddress = None

def updateWithDebug():

	global instructionAddress

	instructionAddress = computer.CPU.programCounter.read()

	update()

	# debug()
	debug2File()

	if breakpoint():

		clock.stop()
		# io.quitPygame()  # call crashes for some reason
		print( 'Breakpoint reached' )


def breakpoint():

	# return computer.data_memory.RAM.registers[ 8000 ] == 6
	# return computer.data_memory.RAM.registers[ 4 ] == 9999

	pass


def debug():

	# print( clock.currentCycle )

	print( '{} ------------'.format( instructionAddress ) )
	print( disassemble( computer.program_memory.read( instructionAddress ) ) )
	print( '' )

	print( 'SP    {}'.format( computer.data_memory.read(  0 ) ) )
	print( 'LCL   {}'.format( computer.data_memory.read(  1 ) ) )
	print( 'ARG   {}'.format( computer.data_memory.read(  2 ) ) )
	print( 'THIS  {}'.format( computer.data_memory.read(  3 ) ) )
	print( 'THAT  {}'.format( computer.data_memory.read(  4 ) ) )
	print( 'GP0   {}'.format( computer.data_memory.read( 13 ) ) )
	print( 'GP1   {}'.format( computer.data_memory.read( 14 ) ) )
	print( 'GP2   {}'.format( computer.data_memory.read( 15 ) ) )
	print( '' )

	# static 16..255
	print( 'Static' )
	for i in range( 16, 256 ):
		print( '{:<3}  {}'.format( i, computer.data_memory.read( i ) ) )
	print( '' )

	# stack 256..2047
	print( 'Stack' )
	for i in range( 256, computer.data_memory.read( 0 ) + 1 ):
		print( '{:<4}  {}'.format( i, computer.data_memory.read( i ) ) )
	print( '' )

	# heap 2048..16383
	print( 'Heap' )
	for i in range( 2048, 16384 ):
		print( '{:<5}  {}'.format( i, computer.data_memory.read( i ) ) )
	print( '' )


debugPath = 'C:/Users/Janet/Desktop/Temp/DumpDebug/'

def debug2File():

	filePath = debugPath + str( clock.currentCycle )

	with open( filePath, 'w' ) as file:

		file.write( '{} ------------'.format( instructionAddress ) + '\n' )
		file.write( disassemble( computer.program_memory.read( instructionAddress ) ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'SP    {}'.format( computer.data_memory.read(  0 ) ) + '\n' )
		file.write( 'LCL   {}'.format( computer.data_memory.read(  1 ) ) + '\n' )
		file.write( 'ARG   {}'.format( computer.data_memory.read(  2 ) ) + '\n' )
		file.write( 'THIS  {}'.format( computer.data_memory.read(  3 ) ) + '\n' )
		file.write( 'THAT  {}'.format( computer.data_memory.read(  4 ) ) + '\n' )
		file.write( 'GP0   {}'.format( computer.data_memory.read( 13 ) ) + '\n' )
		file.write( 'GP1   {}'.format( computer.data_memory.read( 14 ) ) + '\n' )
		file.write( 'GP2   {}'.format( computer.data_memory.read( 15 ) ) + '\n' )
		file.write( '' + '\n' )

		# static 16..255
		file.write( 'Static' + '\n' )
		for i in range( 16, 256 ):
			file.write( '{:<3}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )

		# stack 256..2047
		file.write( 'Stack' + '\n' )
		for i in range( 256, computer.data_memory.read( 0 ) + 1 ):
			file.write( '{:<4}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )

		# heap 2048..16383
		file.write( 'Heap' + '\n' )
		for i in range( 2048, 16384 ):
			file.write( '{:<5}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )


lookup_comp = {

	'110101010' : '0',
	'110111111' : '1',
	'110111010' : '-1',
	'110001100' : 'D',
	'110110000' : 'A',
	'110001101' : '!D',
	'110110001' : '!A',
	'110001111' : '-D',
	'110110011' : '-A',
	'110011111' : 'D+1',
	'110110111' : 'A+1',
	'110001110' : 'D-1',
	'110110010' : 'A-1',
	'110000010' : 'D+A',
	'110000010' : 'A+D',
	'110010011' : 'D-A',
	'110000111' : 'A-D',
	'110000000' : 'D&A',
	'110000000' : 'A&D',
	'110010101' : 'D|A',
	'110010101' : 'A|D',
	'111110000' : 'M',
	'111110001' : '!M',
	'111110011' : '-M',
	'111110111' : 'M+1',
	'111110010' : 'M-1',
	'111000010' : 'D+M',
	'111000010' : 'M+D',
	'111010011' : 'D-M',
	'111000111' : 'M-D',
	'111000000' : 'D&M',
	'111000000' : 'M&D',
	'111010101' : 'D|M',
	'111010101' : 'M|D',

	'101000000' : 'D^M',
	'101000000' : 'M^D',
	'100000000' : 'D^A',
	'100000000' : 'A^D',
	'011000000' : 'D<<M',
	'010000000' : 'D<<A',
	'001000000' : 'D>>M',
	'000000000' : 'D>>A',
}

lookup_dest = {
	
	'000' : 'NULL',
	'001' : 'M',
	'010' : 'D',
	'100' : 'A',
	'011' : 'DM',
	'011' : 'MD',
	'101' : 'AM',
	'101' : 'MA',
	'110' : 'AD',
	'110' : 'DA',
	'111' : 'MDA',
	'111' : 'MAD',
	'111' : 'AMD',
	'111' : 'ADM',
	'111' : 'DMA',
	'111' : 'DAM',
}

lookup_jump = {
	
	'000' : 'NULL',
	'001' : 'JGT',
	'010' : 'JEQ',
	'100' : 'JLT',
	'011' : 'JGE',
	'110' : 'JLE',
	'101' : 'JNE',
	'111' : 'JMP',
}

def disassemble( instruction ):

	instruction = ''.join( map( str, instruction ) )

	disassembled = ''

	# @address
	if instruction[0] == '0' :

		disassembled = '@{}'.format( int( instruction[ 1 : ], 2 ) )

	# dest = cmp ; jmp
	else :

		comp = lookup_comp[ instruction[  1 : 10 ] ]
		dest = lookup_dest[ instruction[ 10 : 13 ] ]
		jump = lookup_jump[ instruction[ 13 : 16 ] ]

		if dest != 'NULL':
			disassembled += dest + ' = '

		disassembled += comp

		if jump != 'NULL':
			disassembled += ' ; ' + jump

	return disassembled



'''----------------------------- Run -----------------------------------'''

# Remove existing logs
if debugMode:
	for f in os.listdir( debugPath ): os.remove( debugPath + f )

# Setup callbacks
if debugMode:
	clock.callbackRising = updateWithDebug
else:
	clock.callbackRising = update

# Start
clock.run()
print( 'Program has started' )
