// --- RAM[2] = RAM[0] >> RAM[1]
// --- Usage: load numbers you wish to >> into
//             ROM[0] and ROM[1]

@0
D = M

@1
D = D >> M

@2
M = D

// end loop
@6
0 ; JMP