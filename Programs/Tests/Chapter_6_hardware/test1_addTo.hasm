// --- Computes RAM[1] = 1 + 2 + ... RAM[0]
// --- Usage: load a value to RAM[0]

// Setup
@16
M = 1		// RAM[16] = 1 // represents i
@17
M = 0		// RAM[17] = 0 // represents sum

// Main loop - break condition
@16
D = M
@0
D = D - M   
@18
D ; JGT		// if i > RAM[0], exit main loop, enter return loop

// Main loop - calculations
@16
D = M
@17
M = D + M 	// sum += i
@16
M = M + 1 	// i += 1
@4
0 ; JMP 	// next iteration of main loop

// Return loop
@17
D = M
@1
M = D 		// RAM[1] = sum
@22
0 ; JMP 	// run return loop indefinitely
