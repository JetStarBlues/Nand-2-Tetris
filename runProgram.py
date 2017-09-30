# ========================================================================================
# 
#  Description:
# 
#     Runs binary programs generated for the Hack computer.
#     Includes a debugger for troubleshooting.
# 
#  Attribution:
# 
#     Code by www.jk-quantized.com
# 
#  Redistribution and use of this code in source and binary forms must retain
#  the above attribution notice and this condition.
# 
# ========================================================================================


'''------------------------------ Imports ------------------------------'''

# Built ins
import os
import time

# Hack computer
from Components import *



'''------------------------------ Setup --------------------------------'''

# programPath = 'Programs/Tests/Chapter_12/Main.bin'
# programPath = 'Programs/ByOthers/MarkArmbrust/Creature/Main.bin'
# programPath = 'Programs/ByOthers/GavinStewart/GASchunky/Main.bin'
programPath = '../tempNotes/MyCompilerOut/OS_standalone/hello_ex/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/math_ex/Main.bin'
# programPath = '../tempNotes/MyCompilerOut/OS_standalone/math/Main.bin'
# programPath = 'Programs/Demos/bin/demo_eo6.bin'
# programPath = 'Programs/Demos/bin/demo_eo6_color.bin'

debugMode = True
# debugMode = False



'''----------------------------- Main -----------------------------------'''

computer = None
clock    = None
io       = None

startTime = 0


def setup():

	global computer
	global clock
	global io

	# Initialize computer
	computer = ComputerN_( N_BITS, DATA_MEMORY_SIZE, PROGRAM_MEMORY_SIZE )
	computer.program_memory.flash( programPath )

	# Initialize clock
	clock = Clock()

	# Remove existing logs
	if debugMode:
		for f in os.listdir( debugPath ): os.remove( debugPath + f )

	# Setup callbacks
	if debugMode:
		clock.callbackRising = updateWithDebug
	else:
		clock.callbackRising = update

	# Initialize IO
	io = IO( N_BITS, computer.data_memory )
	io.runAsThread()


def update():

	computer.run( clock.value )  # tick

	if io.hasExited:

		clock.stop()
		print( 'See you later!' )


def start():

	global startTime

	setup()

	clock.run()
	print( 'Program has started' )

	startTime = time.time()



'''------------------------------ Debug ---------------------------------'''

instructionAddress = None

def updateWithDebug():

	global instructionAddress

	instructionAddress = computer.CPU.programCounter.read()

	update()

	# if clock.currentCycle > - 1:

	# 	debug2File()

	if breakpoint():

		clock.stop()
		# io.quitPygame()  # call crashes for some reason
		# print( 'Breakpoint reached' )
		print( 'Breakpoint reached after {} clock cycles'.format( clock.currentCycle ) )
		print( 'Took {} seconds to reach breakpoint'.format( time.time() - startTime ) )

		debug2File()


def negate( x ): return ( x ^ ( 2 ** 16 - 1 ) ) + 1


def breakpoint():

	# pass

	# Math_ex test...
	# return computer.data_memory.read( 8000 ) == 6
	# return computer.data_memory.read( 8001 ) == negate( 180 )
	# return computer.data_memory.read( 8002 ) == negate( 18000 )
	# return computer.data_memory.read( 8003 ) == negate( 18000 )
	# return computer.data_memory.read( 8004 ) == 0
	# return computer.data_memory.read( 8005 ) == 3
	# return computer.data_memory.read( 8006 ) == negate( 3000 )
	# return computer.data_memory.read( 8007 ) == 0
	# return computer.data_memory.read( 8008 ) == 3
	# return computer.data_memory.read( 8009 ) == 181
	# return computer.data_memory.read( 8010 ) == 123
	# return computer.data_memory.read( 8011 ) == 123
	# return computer.data_memory.read( 8012 ) == 27
	# return computer.data_memory.read( 8013 ) == 32767
	# return instructionAddress == 16551  # Sys.halt (position changes with recompile)

	# Hello_ex test...
	return instructionAddress == 293  # Sys.halt (position changes with recompile)


def debug():

	# print( clock.currentCycle )

	print( '{} ------------'.format( instructionAddress ) )
	print( disassemble( computer.program_memory.read( instructionAddress ) ) )
	print( '' )

	print( 'D     {}'.format( computer.CPU.D_register.read() ) )
	print( '' )

	print( 'SP    {}'.format( computer.data_memory.read(  0 ) ) )
	print( 'LCL   {}'.format( computer.data_memory.read(  1 ) ) )
	print( 'ARG   {}'.format( computer.data_memory.read(  2 ) ) )
	print( 'THIS  {}'.format( computer.data_memory.read(  3 ) ) )
	print( 'THAT  {}'.format( computer.data_memory.read(  4 ) ) )
	print( 'TMP0  {}'.format( computer.data_memory.read(  5 ) ) )
	print( 'TMP1  {}'.format( computer.data_memory.read(  6 ) ) )
	print( 'TMP2  {}'.format( computer.data_memory.read(  7 ) ) )
	print( 'TMP3  {}'.format( computer.data_memory.read(  8 ) ) )
	print( 'TMP4  {}'.format( computer.data_memory.read(  9 ) ) )
	print( 'TMP5  {}'.format( computer.data_memory.read( 10 ) ) )
	print( 'TMP6  {}'.format( computer.data_memory.read( 11 ) ) )
	print( 'TMP7  {}'.format( computer.data_memory.read( 12 ) ) )
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

	sp = computer.data_memory.read( 0 )

	with open( filePath, 'w' ) as file:

		file.write( '{} ------------'.format( instructionAddress ) + '\n' )
		file.write( disassemble( computer.program_memory.read( instructionAddress ) ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'D     {}'.format( computer.CPU.D_register.read() ) + '\n' )
		file.write( '' + '\n' )

		file.write( 'SP    {}'.format( computer.data_memory.read(  0 ) ) + '\n' )
		file.write( 'LCL   {}'.format( computer.data_memory.read(  1 ) ) + '\n' )
		file.write( 'ARG   {}'.format( computer.data_memory.read(  2 ) ) + '\n' )
		file.write( 'THIS  {}'.format( computer.data_memory.read(  3 ) ) + '\n' )
		file.write( 'THAT  {}'.format( computer.data_memory.read(  4 ) ) + '\n' )
		file.write( 'TMP0  {}'.format( computer.data_memory.read(  5 ) ) + '\n' )
		file.write( 'TMP1  {}'.format( computer.data_memory.read(  6 ) ) + '\n' )
		file.write( 'TMP2  {}'.format( computer.data_memory.read(  7 ) ) + '\n' )
		file.write( 'TMP3  {}'.format( computer.data_memory.read(  8 ) ) + '\n' )
		file.write( 'TMP4  {}'.format( computer.data_memory.read(  9 ) ) + '\n' )
		file.write( 'TMP5  {}'.format( computer.data_memory.read( 10 ) ) + '\n' )
		file.write( 'TMP6  {}'.format( computer.data_memory.read( 11 ) ) + '\n' )
		file.write( 'TMP7  {}'.format( computer.data_memory.read( 12 ) ) + '\n' )
		file.write( 'GP0   {}'.format( computer.data_memory.read( 13 ) ) + '\n' )
		file.write( 'GP1   {}'.format( computer.data_memory.read( 14 ) ) + '\n' )
		file.write( 'GP2   {}'.format( computer.data_memory.read( 15 ) ) + '\n' )
		file.write( '' + '\n' )

		# static 16..255
		file.write( 'Static' + '\n' )
		for i in range( 16, 256 ):
			file.write( '\t{:<3}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )

		# stack 256..2047
		file.write( 'Stack' + '\n' )
		for i in range( 256, sp ):
			file.write( '\t{:<4}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '\t{:<4}  .. ({})'.format( sp, computer.data_memory.read( sp ) ) + '\n' )
		file.write( '' + '\n' )

		# heap 2048..16383
		file.write( 'Heap' + '\n' )
		for i in range( 2048, 16384 ):
			file.write( '\t{:<5}  {}'.format( i, computer.data_memory.read( i ) ) + '\n' )
		file.write( '' + '\n' )


lookup_comp = {

	'110101010' : '0',
	'110111111' : '1',
	'110111010' : '- 1',
	'110001100' : 'D',
	'110110000' : 'A',
	'110001101' : '! D',
	'110110001' : '! A',
	'110001111' : '- D',
	'110110011' : '- A',
	'110011111' : 'D + 1',
	'110110111' : 'A + 1',
	'110001110' : 'D - 1',
	'110110010' : 'A - 1',
	'110000010' : 'D + A',
	'110000010' : 'A + D',
	'110010011' : 'D - A',
	'110000111' : 'A - D',
	'110000000' : 'D & A',
	'110000000' : 'A & D',
	'110010101' : 'D | A',
	'110010101' : 'A | D',
	'111110000' : 'M',
	'111110001' : '! M',
	'111110011' : '- M',
	'111110111' : 'M + 1',
	'111110010' : 'M - 1',
	'111000010' : 'D + M',
	'111000010' : 'M + D',
	'111010011' : 'D - M',
	'111000111' : 'M - D',
	'111000000' : 'D & M',
	'111000000' : 'M & D',
	'111010101' : 'D | M',
	'111010101' : 'M | D',

	'101000000' : 'D ^ M',
	'101000000' : 'M ^ D',
	'100000000' : 'D ^ A',
	'100000000' : 'A ^ D',
	'011000000' : 'D << M',
	'010000000' : 'D << A',
	'001000000' : 'D >> M',
	'000000000' : 'D >> A',
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

# Start
start()
