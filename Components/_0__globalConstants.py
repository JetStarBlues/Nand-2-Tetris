''''
	Constants that specify functionality of the Hack computer
'''

# --- Hack Hardware ---------------------------------

N_BITS = 16

CLOCK_HALF_PERIOD = 0.02  # seconds   ( clock rate = 1 / (2 * halfperiod) )

# SCREEN_REFRESH_RATE = 100  # ms
SCREEN_FPS = 15

# Note, addressable memory is one less than N_BITS since 
#  first bit reserved ( used to decide if A or C instruction )
ROM_SIZE = 2**15
RAM_SIZE = 2**15

# RAM Allocation
DATA_MEMORY_MAP     = 0
SCREEN_MEMORY_MAP   = 16384
KBD_MEMORY_MAP      = 24576
MOUSE_MEMORY_MAP    = 24577
MOUSEX_MEMORY_MAP   = 24578
MOUSEY_MEMORY_MAP   = 24579
IO_BANK1_MEMORY_MAP = 24580  # 15 downto 0
IO_BANK2_MEMORY_MAP = 24581  # 31 downto 16


# Performance mode --
# Uses python built-ins for arithmetic operations and storage
PERFORMANCE_MODE = False
if PERFORMANCE_MODE :
	CLOCK_HALF_PERIOD = 0  # Can get away with no clock period as flip flops are not used for memory


# Wishlist --
COLOR_MODE_4BIT = False
if COLOR_MODE_4BIT :
	# Revisit. If find clever way to init colors (probably thru software) no need to change any of the following,
	N_BITS = 17  # first bit reserved ( used to decide if A or C instruction )
	RAM_SIZE = 2**16
	KBD_MEMORY_MAP    = 16384
	MOUSE_MEMORY_MAP  = 16385
	MOUSEX_MEMORY_MAP = 16386
	MOUSEY_MEMORY_MAP = 16387
	SCREEN_MEMORY_MAP = 16388


# --- Simulator UI -----------------------------------

SCREEN_BACKGROUND_COLOR = '#FFFCF3'
SCREEN_FOREGROUND_COLOR = '#717164'

COLOR_PALETTE_4BIT = {

	# PICO-8 palette
	#  www.lexaloffle.com/gfx/pico8_pal_017.png
	'0000' : '#FFF1E8',
	'0001' : '#1D2B53',
	'0010' : '#7E2553',
	'0011' : '#008751',
	'0100' : '#AB5236',
	'0101' : '#5F574F',
	'0110' : '#C2C3C7',
	'0111' : '#000000',
	'1000' : '#FF004D',
	'1001' : '#FFA300',
	'1010' : '#FFEC27',
	'1011' : '#00E436',
	'1100' : '#29ADFF',
	'1101' : '#83769C',
	'1110' : '#FF77A8',
	'1111' : '#FFCCAA',
}