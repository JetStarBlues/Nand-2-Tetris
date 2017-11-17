// --- Creates an array 
//      (in this case of length 10, base address 100, and all values set to -1)
// --- Usage: ...


// Declare variables ---
@100
D = A
@arr
M = D	// RAM[arr] = 100   // base address of array

@10
D = A
@n
M = D	// RAM[n] = 10 		// length of array

@i
M = 0	// RAM[i] = 0


// For loop --
(LOOP)

	@i
	D = M
	@n
	D = D - M
	@END
	D ; JEQ 	// if i == n, goto END

	@arr
	D = M
	@i
	A = D + M	// addr = 100 + i 	// select register
	M = -1		// RAM[addr] = -1 	// set value

	@i
	M = M + 1 	// i++

	@LOOP
	0 ; JMP 	// iterate


// End loop --
(END)

	@END
	0 ; JMP