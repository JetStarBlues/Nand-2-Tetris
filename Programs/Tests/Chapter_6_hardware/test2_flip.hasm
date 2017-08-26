// --- Flips the values of RAM[0] and RAM[1]

@R1
D = M
@temp
M = D	// temp = R1

@R0
D = M
@R1
M = D	// temp = R0

@temp
D = M
@R0
M = D	// R0 = R1

(END)
	@END
	0 ; JMP
