''' Computes RAM[1] = 1 + 2 + ... RAM[0]
	Usage: load a value to RAM[0]
'''

RAM = [None] * 19

def init():
	RAM[16] = 1
	RAM[17] = 0
	RAM[0] = 5
	break_condition() # seq

def break_condition():
	d = RAM[16] - RAM[0]
	if d > 0:
		return_state() # goto
	else:
		loop_state() # seq


def loop_state():
	RAM[17] += RAM[16]
	RAM[16] += 1
	break_condition() # goto

def return_state():
	RAM[1] = RAM[17]
	print(RAM[1])
	# return_state() # goto

init()