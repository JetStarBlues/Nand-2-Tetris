// --- Multiplies R0 and R1 and stores the result in R2.
// --- Usage: load numbers into RAM[0] and RAM[1]


// Setup ---
@R2 	// sum
M = 0
@i
M = 0


// Main loop ---
(LOOP)

	@i
	D = M
	@R0
	D = D - M
	@END
	D ; JEQ 	// if i == RO, goto END

	@R1
	D = M
	@R2
	M = D + M 	// sum += R1

	@i
	M = M + 1 	// i += 1

	@LOOP
	0 ; JMP 	// iterate


// End loop ---
(END)

	@END
	0 ; JMP