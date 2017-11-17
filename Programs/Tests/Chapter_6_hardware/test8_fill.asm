// --- Fills screen with black when a key is being pressed,
//       and white when no key is pressed


// Setup ---

@SCREEN
D = A
@r
M = D		// r = @SCREEN

@8192
D = A
@n
M = D 		// n = 8192

@r
D = M
@n
M = D + M 	// n += r


// Main loop ---

(CHECK_STATUS)

	@r
	D = M
	@n
	D = D - M
	@END
	D ; JEQ 	// if RAM[r] == n, go to END

	@KBD
	D = M
	@BLACK
	D ; JNE		// if keyPressed != 0, go to BLACK

(WHITE)

	@r
	A = M 		// select RAM[ RAM[r] ]
	M = 0 		// and set its value

	@r
	M = M + 1 	// RAM[r] += 1

	@CHECK_STATUS
	0 ; JMP

(BLACK)

	@r
	A = M 		// select RAM[ RAM[r] ]
	M = -1 		// and set its value

	@r
	M = M + 1 	// RAM[r] += 1

	@CHECK_STATUS
	0 ; JMP
	

// End loop ---

(END)
	@END
	0 ; JMP