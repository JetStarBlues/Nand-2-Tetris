// --- Draw a rectangle at (0,0) that has
//		width 16px and height RAM[0]px
// --- Usage: load non-negative number into RAM[0]


// Setup ---

@SCREEN	// @16384
D = A
@addr
M = D 	// RAM[addr] = 16384   // @addr is a pointer

@0
D = M
@n
M = D 	// @n = RAM[0]

@r
M = 0 	// @r = 0


// Main loop ---

(LOOP)
	@r
	D = M
	@n
	D = D - M
	@END
	D ; JEQ 	// if r == n, goto END

	@addr
	A = M 		// set current RAM address to contents of RAM[addr]
	M = -1		// RAM[ @addr ] = -1  // RAM[ RAM[addr] ]

	@32
	D = A
	@addr
	M = D + M 	// RAM[addr] += 32

	@r
	M = M + 1 	// RAM[r] += 1

	@LOOP
	0 ; JMP


// End loop ---

(END)
	@END
	0 ; JMP