// --- Creates an array 
//      (in this case of length 10, base address 100, and all values set to -1)
// --- Usage: ...


// Setup --
@100
D = A
@baseAddr
M = D	// RAM[baseAddr] = 100   // base address of array

@10
D = A
@length
M = D	// RAM[length] = 10 	 // length of array

@i
M = 0	// RAM[i] = 0



// For loop --
(LOOP)

	@i
	D = M
	@length
	D = D - M
	@END
	D ; JEQ     // if i == length, goto END

	@baseAddr
	D = M
	@i
	D = D + M	
	@addr
	M = D       // addr = 100 + i

	@0
	D = M
	@addr
	A = M       // RAM[ RAM[addr] ]     // select register
	M = D       // RAM[@addr] = RAM[0]	// set value

	@i
	M = M + 1 	// i++

	@LOOP
	0 ; JMP 	// iterate


// End loop --
(END)

	@END
	0 ; JMP
