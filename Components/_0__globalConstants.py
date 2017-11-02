''''
	Constants that specify functionality of the Hack computer
'''

# --- Hack Hardware ---------------------------------

N_BITS = 16

CLOCK_HALF_PERIOD = 0.02  # seconds   ( clock rate = 1 / (2 * halfperiod) )

SCREEN_FPS = 1
# SCREEN_FPS = 3

# Note, addressable memory is one less than N_BITS since 
#  first bit reserved ( used to decide if A or C instruction )
PROGRAM_MEMORY_SIZE = 2**16
DATA_MEMORY_SIZE = 2**16

# RAM Allocation (compatible)
SCREEN_MEMORY_MAP   = 16384
KBD_MEMORY_MAP      = 24576
MOUSE_MEMORY_MAP    = 24577
MOUSEX_MEMORY_MAP   = 24578
MOUSEY_MEMORY_MAP   = 24579
IO_BANK1_MEMORY_MAP = 24580  # 15 downto 0
IO_BANK2_MEMORY_MAP = 24581  # 31 downto 16


# Performance mode --
# Uses python built-ins for arithmetic operations and storage
PERFORMANCE_MODE = True
if PERFORMANCE_MODE :
	CLOCK_HALF_PERIOD = 0  # Can get away with no clock period as flip flops are not used for memory


# Color mode --
COLOR_MODE_4BIT = False
if COLOR_MODE_4BIT :

	# No space is left unallocated
	heapEnd = PROGRAM_MEMORY_SIZE - 8192 * 4 - 6

	KBD_MEMORY_MAP      = heapEnd + 0
	MOUSE_MEMORY_MAP    = heapEnd + 1
	MOUSEX_MEMORY_MAP   = heapEnd + 2
	MOUSEY_MEMORY_MAP   = heapEnd + 3
	IO_BANK1_MEMORY_MAP = heapEnd + 4
	IO_BANK2_MEMORY_MAP = heapEnd + 5
	SCREEN_MEMORY_MAP   = heapEnd + 6


# --- Simulator UI -----------------------------------

SCREEN_BACKGROUND_COLOR = '#FFFCF3'
SCREEN_FOREGROUND_COLOR = '#717164'

COLOR_PALETTE_4BIT = {

	# PICO-8 palette
	#  www.lexaloffle.com/gfx/pico8_pal_017.png
	'0000' : '#000000',
	'0001' : '#1D2B53',
	'0010' : '#7E2553',
	'0011' : '#008751',
	'0100' : '#AB5236',
	'0101' : '#5F574F',
	'0110' : '#C2C3C7',
	'0111' : '#FFF1E8',
	'1000' : '#FF004D',
	'1001' : '#FFA300',
	'1010' : '#FFEC27',
	'1011' : '#00E436',
	'1100' : '#29ADFF',
	'1101' : '#83769C',
	'1110' : '#FF77A8',
	'1111' : '#FFCCAA',
}