// --- RAM[2] = RAM[0] >> value_specified_below
// --- Usage: load number you wish to >> into ROM[0]

@0
D = M

@7
D = D >> A

@2
M = D

// end loop
@6
0 ; JMP