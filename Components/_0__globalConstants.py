''''
	Constants that specify functionality of the Hack computer
'''

# --- Hack Hardware ---------------------------------

N_BITS = 16

CLOCK_HALF_PERIOD = 0.02  # seconds   ( clock rate = 1 / (2 * halfperiod) )

SCREEN_FPS = 1
# SCREEN_FPS = 15
# SCREEN_FPS = 30

# Note, addressable memory is one less than N_BITS since 
#  first bit reserved ( used to decide if A or C instruction )
PROGRAM_MEMORY_SIZE = 2**26
DATA_MEMORY_SIZE    = 2**16

# RAM Allocation (compatible)
STATIC_START = 16
STATIC_END   = 255  # TODO, make static bigger
STACK_START  = 256
STACK_END    = 2047
HEAP_START   = 2048
HEAP_END     = 32755  # 32767 - ( 8 + 2 + 3 ) + 1

SCREEN_MEMORY_MAP   = HEAP_END + 0   # 8
KEYBOARD_MEMORY_MAP = HEAP_END + 8   # 2
MOUSE_MEMORY_MAP    = HEAP_END + 10  # 3
# IO_BANK1_MEMORY_MAP = None  # 15 downto 0
# IO_BANK2_MEMORY_MAP = None  # 31 downto 16


# Performance mode --
# Uses python built-ins for arithmetic operations and storage
PERFORMANCE_MODE = True

if PERFORMANCE_MODE :
	CLOCK_HALF_PERIOD = 0  # Can get away with no clock period as flip flops are not used for memory


# --- Emulator --------------------------------------

COLOR_PALETTE_1BIT = {

	'0' : '#FFFCF3',
	'1' : '#717164',
}

COLOR_PALETTE_4BIT = {

	# PICO-8 palette
	#  www.lexaloffle.com/gfx/pico8_pal_017.png
	#  www.lexaloffle.com/pico-8.php?page=faq
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
