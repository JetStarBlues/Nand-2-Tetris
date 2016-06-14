''''
	Constants that specify functionality of the Hack computer
'''

# --- Hack Hardware ---------------------------------

N_BITS = 16

CLOCK_HALF_PERIOD = 0.005 # 0.02  # seconds   ( clock rate = 1 / (2 * halfperiod) )

SCREEN_REFRESH_RATE = 100  # ms

ROM_SIZE = 2**15
RAM_SIZE = 2**15

# RAM Allocation
DATA_MEMORY_MAP   = 0
SCREEN_MEMORY_MAP = 16384
KBD_MEMORY_MAP    = 24576



# --- Hack Software ---------------------------------




# --- Simulator UI -----------------------------------

SCREEN_BACKGROUND_COLOR = '#FFFCF3'
SCREEN_FOREGROUND_COLOR = '#717164'
