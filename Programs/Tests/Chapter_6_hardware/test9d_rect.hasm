// --- Draw a rectangle at RAM[1] that has
//		width 16px and height RAM[0]px
// --- Usage: load non-negative number into RAM[0]


// Setup ---

@SCREEN		// @16384
D = A
@addr
M = D 		// @addr = 16384

@R1
D = M
@addr
M = D + M 	// @addr += RAM[1]


@R0
D = M
@n
M = D 		// @n = RAM[0]


@i
M = 0 		// @i = 0


// Main loop ---

(LOOP)
	@i
	D = M
	@n
	D = D - M
	@END
	D ; JEQ 	// if i == n, goto END

	@addr
	A = M 		
	M = -1		// RAM[ @addr ] = -1

	@32
	D = A
	@addr
	M = D + M 	// @addr += 32

	@i
	M = M + 1 	// @i += 1

	@LOOP
	0 ; JMP


// End loop ---

(END)
	@END
	0 ; JMP
