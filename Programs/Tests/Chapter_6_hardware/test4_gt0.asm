// --- if RAM[0] > 0, RAM[1] = 1
//              else, RAM[1] = 0
// --- Usage: load a number into ROM[0]

@1       
M = 1    // RAM[1] = 1

@0
D = M    // D = RAM[0]

@4 		  
D ; JGT  // infinite loop, jump to ROM[4] if D > 0

@1
M = 0    // RAM[1] = 0

@8
0 ; JMP  // infinite loop, end loop