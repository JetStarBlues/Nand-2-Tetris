// --- Begin pointer setup

// set SP
@256
D = A
@SP
M = D

// set LCL
@LCL
M = D

// set ARG
@ARG
M = D

// set THIS
@9999
D = A
@THIS
M = D

// set THAT
@THAT
M = D

// --- end pointer setup


// --- Call Sys.init()
@Sys.init
0 ; JMP


// --- Begin generic functions

// genericReturn
($_genericReturn)
@LCL
D = M
@curLCL
M = D
@5
A = D - A
D = M
@13
M = D
@SP
A = M - 1
D = M
@ARG
A = M
M = D
@ARG
D = M
@SP
M = D + 1
A = D - 1
D = M
@THAT
M = D
@2
D = A
@curLCL
A = M - D
D = M
@THIS
M = D
@3
D = A
@curLCL
A = M - D
D = M
@ARG
M = D
@4
D = A
@curLCL
A = M - D
D = M
@LCL
M = D
@13
A = M
0 ; JMP

// genericCall
($_genericCall)
@SP
A = M
M = D
@SP
M = M + 1
@LCL
D = M
@SP
A = M
M = D
@SP
M = M + 1
@ARG
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
@THAT
D = M
@SP
A = M
M = D
@SP
M = M + 1
@15
D = M
@5
D = D + A
@SP
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
@14
A = M
0 ; JMP

// genericComparisonOp
($_greaterThan)
@comp_true
D ; JGT
@comp_false
0 ; JMP

($_greaterThanOrEqual)
@comp_true
D ; JGE
@comp_false
0 ; JMP

($_lessThanOrEqual)
@comp_true
D ; JLE
@comp_false
0 ; JMP

($_equal)
@comp_true
D ; JEQ
@comp_false
0 ; JMP

($_lessThan)
@comp_true
D ; JLT
@comp_false
0 ; JMP

($_notEqual)
@comp_true
D ; JNE
@comp_false
0 ; JMP

($_genericComparisonOp)
@SP
AM = M - 1
D = M
A = A - 1
D = M - D
@14
A = M
0 ; JMP
(comp_false)
D = 0
@comp_end
0 ; JMP
(comp_true)
D = 1
(comp_end)
@SP
A = M - 1
M = D
@15
A = M
0 ; JMP

// --- end generic functions


// === Keyboard ===

// function Keyboard.init 0
(Keyboard.init)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Keyboard.keyPressed 0
(Keyboard.keyPressed)
// push constant 24576
@24576
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Memory.peek 1
@Memory.peek
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction0
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction0)
// return
@$_genericReturn
0 ; JMP
// function Keyboard.readChar 2
(Keyboard.readChar)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@2
D = A
@SP
M = M + D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.printChar 1
@Output.printChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction1
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction1)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Keyboard.readChar.WHILE_EXP0)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction2
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction2)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction3
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction3)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Keyboard.readChar.WHILE_END0
D ; JNE
// call Keyboard.keyPressed 0
@Keyboard.keyPressed
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction4
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction4)
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction5
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction5)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Keyboard.readChar.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Keyboard.readChar.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Keyboard.readChar.IF_TRUE0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Keyboard.readChar.IF_FALSE0)
// goto WHILE_EXP0
@Keyboard.readChar.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Keyboard.readChar.WHILE_END0)
// call String.backSpace 0
@String.backSpace
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction6
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction6)
// call Output.printChar 1
@Output.printChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction7
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction7)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Output.printChar 1
@Output.printChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction8
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction8)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Keyboard.readLine 5
(Keyboard.readLine)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@5
D = A
@SP
M = M + D
// push constant 80
@80
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.new 1
@String.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction9
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction9)
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Output.printString 1
@Output.printString
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction10
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction10)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call String.newLine 0
@String.newLine
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction11
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction11)
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call String.backSpace 0
@String.backSpace
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction12
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction12)
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Keyboard.readLine.WHILE_EXP0)
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Keyboard.readLine.WHILE_END0
D ; JNE
// call Keyboard.readChar 0
@Keyboard.readChar
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction13
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction13)
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction14
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction14)
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Keyboard.readLine.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Keyboard.readLine.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Keyboard.readLine.IF_TRUE0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction15
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction15)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Keyboard.readLine.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Keyboard.readLine.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Keyboard.readLine.IF_TRUE1)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.eraseLastChar 1
@String.eraseLastChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction16
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction16)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END1
@Keyboard.readLine.IF_END1
0 ; JMP
// label IF_FALSE1
(Keyboard.readLine.IF_FALSE1)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction17
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction17)
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END1
(Keyboard.readLine.IF_END1)
// label IF_FALSE0
(Keyboard.readLine.IF_FALSE0)
// goto WHILE_EXP0
@Keyboard.readLine.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Keyboard.readLine.WHILE_END0)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Keyboard.readInt 2
(Keyboard.readInt)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@2
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Keyboard.readLine 1
@Keyboard.readLine
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction18
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction18)
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.intValue 1
@String.intValue
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction19
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction19)
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.dispose 1
@String.dispose
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction20
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction20)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Memory ===

// function Memory.init 0
(Memory.init)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 0
@SP
AM = M - 1
D = M
@Memory.0
M = D
// push constant 2048
@2048
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Memory.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 14334
@14334
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 2049
@2049
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Memory.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 2050
@2050
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Memory.peek 0
(Memory.peek)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Memory.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Memory.poke 0
(Memory.poke)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Memory.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Memory.alloc 1
(Memory.alloc)
@SP
A = M
M = 0
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction21
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction21)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Memory.alloc.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Memory.alloc.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Memory.alloc.IF_TRUE0)
// push constant 5
@5
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction22
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction22)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Memory.alloc.IF_FALSE0)
// push constant 2048
@2048
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Memory.alloc.WHILE_EXP0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction23
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction23)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Memory.alloc.WHILE_END0
D ; JNE
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Memory.alloc.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Memory.alloc.WHILE_END0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 16379
@16379
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction24
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction24)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Memory.alloc.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Memory.alloc.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Memory.alloc.IF_TRUE1)
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction25
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction25)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(Memory.alloc.IF_FALSE1)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction26
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction26)
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Memory.alloc.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Memory.alloc.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Memory.alloc.IF_TRUE2)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction27
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction27)
// if-goto IF_TRUE3
@SP
AM = M - 1
D = M
@Memory.alloc.IF_TRUE3
D ; JNE
// goto IF_FALSE3
@Memory.alloc.IF_FALSE3
0 ; JMP
// label IF_TRUE3
(Memory.alloc.IF_TRUE3)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 4
@4
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END3
@Memory.alloc.IF_END3
0 ; JMP
// label IF_FALSE3
(Memory.alloc.IF_FALSE3)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END3
(Memory.alloc.IF_END3)
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE2
(Memory.alloc.IF_FALSE2)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// return
@$_genericReturn
0 ; JMP
// function Memory.deAlloc 2
(Memory.deAlloc)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@2
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction28
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction28)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Memory.deAlloc.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Memory.deAlloc.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Memory.deAlloc.IF_TRUE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END0
@Memory.deAlloc.IF_END0
0 ; JMP
// label IF_FALSE0
(Memory.deAlloc.IF_FALSE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction29
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction29)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Memory.deAlloc.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Memory.deAlloc.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Memory.deAlloc.IF_TRUE1)
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END1
@Memory.deAlloc.IF_END1
0 ; JMP
// label IF_FALSE1
(Memory.deAlloc.IF_FALSE1)
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END1
(Memory.deAlloc.IF_END1)
// label IF_END0
(Memory.deAlloc.IF_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Array ===

// function Array.new 0
(Array.new)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction30
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction30)
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Array.new.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Array.new.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Array.new.IF_TRUE0)
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction31
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction31)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Array.new.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Memory.alloc 1
@Memory.alloc
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction32
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction32)
// return
@$_genericReturn
0 ; JMP
// function Array.dispose 0
(Array.dispose)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push pointer 0
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Memory.deAlloc 1
@Memory.deAlloc
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction33
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction33)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Main ===

// function Main.main 0
(Main.main)
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.new 1
@String.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction34
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction34)
// push constant 72
@72
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction35
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction35)
// push constant 105
@105
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction36
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction36)
// push constant 33
@33
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction37
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction37)
// call Output.printString 1
@Output.printString
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction38
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction38)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Screen ===

// function Screen.init 1
(Screen.init)
@SP
A = M
M = 0
@SP
M = M + 1
// push constant 16384
@16384
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 1
@SP
AM = M - 1
D = M
@Screen.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop static 2
@SP
AM = M - 1
D = M
@Screen.2
M = D
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction39
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction39)
// pop static 0
@SP
AM = M - 1
D = M
@Screen.0
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Screen.init.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction40
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction40)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Screen.init.WHILE_END0
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Screen.init.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Screen.init.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.clearScreen 1
(Screen.clearScreen)
@SP
A = M
M = 0
@SP
M = M + 1
// label WHILE_EXP0
(Screen.clearScreen.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 8192
@8192
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction41
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction41)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Screen.clearScreen.WHILE_END0
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Screen.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Screen.clearScreen.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Screen.clearScreen.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.updateLocation 0
(Screen.updateLocation)
// push static 2
@Screen.2
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.updateLocation.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.updateLocation.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.updateLocation.IF_TRUE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Screen.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Screen.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END0
@Screen.updateLocation.IF_END0
0 ; JMP
// label IF_FALSE0
(Screen.updateLocation.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Screen.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Screen.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END0
(Screen.updateLocation.IF_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.setColor 0
(Screen.setColor)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop static 2
@SP
AM = M - 1
D = M
@Screen.2
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawPixel 3
(Screen.drawPixel)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@3
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction42
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction42)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 511
@511
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction43
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction43)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction44
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction44)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 255
@255
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction45
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction45)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.drawPixel.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.drawPixel.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.drawPixel.IF_TRUE0)
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction46
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction46)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Screen.drawPixel.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction47
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction47)
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction48
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction48)
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction49
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction49)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction50
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction50)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawConditional 0
(Screen.drawConditional)
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.drawConditional.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.drawConditional.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.drawConditional.IF_TRUE0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.drawPixel 2
@Screen.drawPixel
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction51
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction51)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END0
@Screen.drawConditional.IF_END0
0 ; JMP
// label IF_FALSE0
(Screen.drawConditional.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.drawPixel 2
@Screen.drawPixel
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction52
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction52)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END0
(Screen.drawConditional.IF_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawLine 11
(Screen.drawLine)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@11
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction53
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction53)
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 511
@511
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction54
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction54)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction55
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction55)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 255
@255
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction56
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction56)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.drawLine.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.drawLine.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.drawLine.IF_TRUE0)
// push constant 8
@8
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction57
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction57)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Screen.drawLine.IF_FALSE0)
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// call Math.abs 1
@Math.abs
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction58
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction58)
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// call Math.abs 1
@Math.abs
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction59
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction59)
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction60
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction60)
// pop local 6
@6
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction61
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction61)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction62
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction62)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Screen.drawLine.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Screen.drawLine.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Screen.drawLine.IF_TRUE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 2
@2
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 3
@3
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(Screen.drawLine.IF_FALSE1)
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Screen.drawLine.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Screen.drawLine.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Screen.drawLine.IF_TRUE2)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 8
@8
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction63
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction63)
// pop local 7
@7
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END2
@Screen.drawLine.IF_END2
0 ; JMP
// label IF_FALSE2
(Screen.drawLine.IF_FALSE2)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 8
@8
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction64
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction64)
// pop local 7
@7
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END2
(Screen.drawLine.IF_END2)
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction65
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction65)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 5
@5
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction66
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction66)
// pop local 9
@9
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction67
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction67)
// pop local 10
@10
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.drawConditional 3
@Screen.drawConditional
D = A
@14
M = D
@3
D = A
@15
M = D
@$_returnFromGenericFunction68
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction68)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Screen.drawLine.WHILE_EXP0)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 8
@8
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction69
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction69)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Screen.drawLine.WHILE_END0
D ; JNE
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction70
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction70)
// if-goto IF_TRUE3
@SP
AM = M - 1
D = M
@Screen.drawLine.IF_TRUE3
D ; JNE
// goto IF_FALSE3
@Screen.drawLine.IF_FALSE3
0 ; JMP
// label IF_TRUE3
(Screen.drawLine.IF_TRUE3)
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 9
@9
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 5
@5
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END3
@Screen.drawLine.IF_END3
0 ; JMP
// label IF_FALSE3
(Screen.drawLine.IF_FALSE3)
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 10
@10
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 5
@5
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 7
@7
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE4
@SP
AM = M - 1
D = M
@Screen.drawLine.IF_TRUE4
D ; JNE
// goto IF_FALSE4
@Screen.drawLine.IF_FALSE4
0 ; JMP
// label IF_TRUE4
(Screen.drawLine.IF_TRUE4)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END4
@Screen.drawLine.IF_END4
0 ; JMP
// label IF_FALSE4
(Screen.drawLine.IF_FALSE4)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END4
(Screen.drawLine.IF_END4)
// label IF_END3
(Screen.drawLine.IF_END3)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.drawConditional 3
@Screen.drawConditional
D = A
@14
M = D
@3
D = A
@15
M = D
@$_returnFromGenericFunction71
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction71)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Screen.drawLine.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Screen.drawLine.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawRectangle 9
(Screen.drawRectangle)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@9
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction72
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction72)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction73
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction73)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction74
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction74)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 511
@511
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction75
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction75)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction76
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction76)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 255
@255
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction77
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction77)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.drawRectangle.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.drawRectangle.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.drawRectangle.IF_TRUE0)
// push constant 9
@9
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction78
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction78)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Screen.drawRectangle.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction79
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction79)
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction80
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction80)
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 7
@7
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction81
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction81)
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction82
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction82)
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 8
@8
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 7
@7
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// not
@SP
A = M - 1
M = ! M
// pop local 6
@6
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 8
@8
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 5
@5
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction83
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction83)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Screen.drawRectangle.WHILE_EXP0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction84
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction84)
// not
@SP
A = M - 1
M = ! M
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Screen.drawRectangle.WHILE_END0
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction85
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction85)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Screen.drawRectangle.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Screen.drawRectangle.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Screen.drawRectangle.IF_TRUE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction86
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction86)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END1
@Screen.drawRectangle.IF_END1
0 ; JMP
// label IF_FALSE1
(Screen.drawRectangle.IF_FALSE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction87
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction87)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP1
(Screen.drawRectangle.WHILE_EXP1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction88
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction88)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END1
@SP
AM = M - 1
D = M
@Screen.drawRectangle.WHILE_END1
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction89
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction89)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP1
@Screen.drawRectangle.WHILE_EXP1
0 ; JMP
// label WHILE_END1
(Screen.drawRectangle.WHILE_END1)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction90
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction90)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END1
(Screen.drawRectangle.IF_END1)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Screen.drawRectangle.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Screen.drawRectangle.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawHorizontal 11
(Screen.drawHorizontal)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@11
D = A
@SP
M = M + D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.min 2
@Math.min
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction91
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction91)
// pop local 7
@7
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.max 2
@Math.max
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction92
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction92)
// pop local 8
@8
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction93
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction93)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 256
@256
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction94
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction94)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// push local 7
@7
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 512
@512
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction95
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction95)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// push local 8
@8
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction96
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction96)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.drawHorizontal.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.drawHorizontal.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.drawHorizontal.IF_TRUE0)
// push local 7
@7
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.max 2
@Math.max
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction97
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction97)
// pop local 7
@7
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 8
@8
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 511
@511
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.min 2
@Math.min
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction98
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction98)
// pop local 8
@8
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 7
@7
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction99
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction99)
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 7
@7
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction100
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction100)
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 9
@9
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 8
@8
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction101
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction101)
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 8
@8
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction102
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction102)
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 10
@10
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 9
@9
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// not
@SP
A = M - 1
M = ! M
// pop local 5
@5
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 10
@10
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push static 0
@Screen.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction103
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction103)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 6
@6
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 6
@6
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction104
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction104)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Screen.drawHorizontal.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Screen.drawHorizontal.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Screen.drawHorizontal.IF_TRUE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction105
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction105)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END1
@Screen.drawHorizontal.IF_END1
0 ; JMP
// label IF_FALSE1
(Screen.drawHorizontal.IF_FALSE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 5
@5
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction106
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction106)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Screen.drawHorizontal.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction107
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction107)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Screen.drawHorizontal.WHILE_END0
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction108
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction108)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Screen.drawHorizontal.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Screen.drawHorizontal.WHILE_END0)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.updateLocation 2
@Screen.updateLocation
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction109
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction109)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END1
(Screen.drawHorizontal.IF_END1)
// label IF_FALSE0
(Screen.drawHorizontal.IF_FALSE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawSymetric 0
(Screen.drawSymetric)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// call Screen.drawHorizontal 3
@Screen.drawHorizontal
D = A
@14
M = D
@3
D = A
@15
M = D
@$_returnFromGenericFunction110
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction110)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// call Screen.drawHorizontal 3
@Screen.drawHorizontal
D = A
@14
M = D
@3
D = A
@15
M = D
@$_returnFromGenericFunction111
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction111)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// call Screen.drawHorizontal 3
@Screen.drawHorizontal
D = A
@14
M = D
@3
D = A
@15
M = D
@$_returnFromGenericFunction112
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction112)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// call Screen.drawHorizontal 3
@Screen.drawHorizontal
D = A
@14
M = D
@3
D = A
@15
M = D
@$_returnFromGenericFunction113
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction113)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Screen.drawCircle 3
(Screen.drawCircle)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@3
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction114
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction114)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 511
@511
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction115
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction115)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction116
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction116)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 255
@255
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction117
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction117)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Screen.drawCircle.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Screen.drawCircle.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Screen.drawCircle.IF_TRUE0)
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction118
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction118)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Screen.drawCircle.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction119
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction119)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 511
@511
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction120
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction120)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction121
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction121)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 255
@255
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction122
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction122)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Screen.drawCircle.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Screen.drawCircle.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Screen.drawCircle.IF_TRUE1)
// push constant 13
@13
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction123
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction123)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(Screen.drawCircle.IF_FALSE1)
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.drawSymetric 4
@Screen.drawSymetric
D = A
@14
M = D
@4
D = A
@15
M = D
@$_returnFromGenericFunction124
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction124)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Screen.drawCircle.WHILE_EXP0)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction125
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction125)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Screen.drawCircle.WHILE_END0
D ; JNE
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction126
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction126)
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Screen.drawCircle.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Screen.drawCircle.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Screen.drawCircle.IF_TRUE2)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction127
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction127)
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END2
@Screen.drawCircle.IF_END2
0 ; JMP
// label IF_FALSE2
(Screen.drawCircle.IF_FALSE2)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction128
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction128)
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 5
@5
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END2
(Screen.drawCircle.IF_END2)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Screen.drawSymetric 4
@Screen.drawSymetric
D = A
@14
M = D
@4
D = A
@15
M = D
@$_returnFromGenericFunction129
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction129)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Screen.drawCircle.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Screen.drawCircle.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Math ===

// function Math.init 1
(Math.init)
@SP
A = M
M = 0
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction130
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction130)
// pop static 1
@SP
AM = M - 1
D = M
@Math.1
M = D
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction131
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction131)
// pop static 0
@SP
AM = M - 1
D = M
@Math.0
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Math.init.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction132
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction132)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Math.init.WHILE_END0
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Math.init.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Math.init.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Math.abs 0
(Math.abs)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction133
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction133)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Math.abs.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Math.abs.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Math.abs.IF_TRUE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Math.abs.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Math.multiply 5
(Math.multiply)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@5
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction134
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction134)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction135
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction135)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction136
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction136)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction137
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction137)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.abs 1
@Math.abs
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction138
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction138)
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.abs 1
@Math.abs
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction139
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction139)
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction140
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction140)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Math.multiply.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Math.multiply.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Math.multiply.IF_TRUE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Math.multiply.IF_FALSE0)
// label WHILE_EXP0
(Math.multiply.WHILE_EXP0)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction141
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction141)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Math.multiply.WHILE_END0
D ; JNE
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction142
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction142)
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Math.multiply.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Math.multiply.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Math.multiply.IF_TRUE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(Math.multiply.IF_FALSE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Math.multiply.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Math.multiply.WHILE_END0)
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Math.multiply.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Math.multiply.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Math.multiply.IF_TRUE2)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE2
(Math.multiply.IF_FALSE2)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Math.divide 4
(Math.divide)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@4
D = A
@SP
M = M + D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction143
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction143)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Math.divide.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Math.divide.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Math.divide.IF_TRUE0)
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction144
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction144)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Math.divide.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction145
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction145)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction146
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction146)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction147
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction147)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction148
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction148)
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.abs 1
@Math.abs
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction149
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction149)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.abs 1
@Math.abs
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction150
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction150)
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Math.divide.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction151
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction151)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Math.divide.WHILE_END0
D ; JNE
// push constant 32767
@32767
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction152
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction152)
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Math.divide.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Math.divide.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Math.divide.IF_TRUE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction153
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction153)
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Math.divide.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Math.divide.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Math.divide.IF_TRUE2)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE2
(Math.divide.IF_FALSE2)
// label IF_FALSE1
(Math.divide.IF_FALSE1)
// goto WHILE_EXP0
@Math.divide.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Math.divide.WHILE_END0)
// label WHILE_EXP1
(Math.divide.WHILE_EXP1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction154
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction154)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END1
@SP
AM = M - 1
D = M
@Math.divide.WHILE_END1
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction155
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction155)
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE3
@SP
AM = M - 1
D = M
@Math.divide.IF_TRUE3
D ; JNE
// goto IF_FALSE3
@Math.divide.IF_FALSE3
0 ; JMP
// label IF_TRUE3
(Math.divide.IF_TRUE3)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 1
@Math.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE3
(Math.divide.IF_FALSE3)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP1
@Math.divide.WHILE_EXP1
0 ; JMP
// label WHILE_END1
(Math.divide.WHILE_END1)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE4
@SP
AM = M - 1
D = M
@Math.divide.IF_TRUE4
D ; JNE
// goto IF_FALSE4
@Math.divide.IF_FALSE4
0 ; JMP
// label IF_TRUE4
(Math.divide.IF_TRUE4)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE4
(Math.divide.IF_FALSE4)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Math.sqrt 4
(Math.sqrt)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@4
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction156
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction156)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Math.sqrt.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Math.sqrt.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Math.sqrt.IF_TRUE0)
// push constant 4
@4
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction157
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction157)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Math.sqrt.IF_FALSE0)
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Math.sqrt.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction158
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction158)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Math.sqrt.WHILE_END0
D ; JNE
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Math.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction159
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction159)
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction160
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction160)
// not
@SP
A = M - 1
M = ! M
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction161
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction161)
// not
@SP
A = M - 1
M = ! M
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Math.sqrt.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Math.sqrt.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Math.sqrt.IF_TRUE1)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(Math.sqrt.IF_FALSE1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Math.sqrt.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Math.sqrt.WHILE_END0)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Math.max 0
(Math.max)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction162
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction162)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Math.max.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Math.max.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Math.max.IF_TRUE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Math.max.IF_FALSE0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Math.min 0
(Math.min)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction163
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction163)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Math.min.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Math.min.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Math.min.IF_TRUE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Math.min.IF_FALSE0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === String ===

// function String.new 0
(String.new)
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Memory.alloc 1
@Memory.alloc
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction164
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction164)
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction165
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction165)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.new.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.new.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.new.IF_TRUE0)
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction166
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction166)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.new.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction167
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction167)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@String.new.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@String.new.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(String.new.IF_TRUE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction168
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction168)
// pop this 1
@1
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(String.new.IF_FALSE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop this 0
@0
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop this 2
@2
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push pointer 0
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.dispose 0
(String.dispose)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push this 0
@0
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction169
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction169)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.dispose.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.dispose.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.dispose.IF_TRUE0)
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Array.dispose 1
@Array.dispose
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction170
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction170)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.dispose.IF_FALSE0)
// push pointer 0
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Memory.deAlloc 1
@Memory.deAlloc
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction171
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction171)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.length 0
(String.length)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.charAt 0
(String.charAt)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction172
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction172)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction173
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction173)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction174
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction174)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.charAt.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.charAt.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.charAt.IF_TRUE0)
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction175
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction175)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.charAt.IF_FALSE0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.setCharAt 0
(String.setCharAt)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction176
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction176)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction177
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction177)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction178
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction178)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.setCharAt.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.setCharAt.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.setCharAt.IF_TRUE0)
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction179
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction179)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.setCharAt.IF_FALSE0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.appendChar 0
(String.appendChar)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 0
@0
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction180
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction180)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.appendChar.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.appendChar.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.appendChar.IF_TRUE0)
// push constant 17
@17
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction181
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction181)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.appendChar.IF_FALSE0)
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop this 2
@2
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push pointer 0
@THIS
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.eraseLastChar 0
(String.eraseLastChar)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction182
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction182)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.eraseLastChar.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.eraseLastChar.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.eraseLastChar.IF_TRUE0)
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction183
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction183)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.eraseLastChar.IF_FALSE0)
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop this 2
@2
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.intValue 5
(String.intValue)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@5
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction184
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction184)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.intValue.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.intValue.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.intValue.IF_TRUE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// label IF_FALSE0
(String.intValue.IF_FALSE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 45
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction185
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction185)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@String.intValue.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@String.intValue.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(String.intValue.IF_TRUE1)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop local 4
@4
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(String.intValue.IF_FALSE1)
// label WHILE_EXP0
(String.intValue.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction186
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction186)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@String.intValue.WHILE_END0
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction187
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction187)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 9
@9
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction188
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction188)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// not
@SP
A = M - 1
M = ! M
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@String.intValue.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@String.intValue.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(String.intValue.IF_TRUE2)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 10
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction189
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction189)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE2
(String.intValue.IF_FALSE2)
// goto WHILE_EXP0
@String.intValue.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(String.intValue.WHILE_END0)
// push local 4
@4
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE3
@SP
AM = M - 1
D = M
@String.intValue.IF_TRUE3
D ; JNE
// goto IF_FALSE3
@String.intValue.IF_FALSE3
0 ; JMP
// label IF_TRUE3
(String.intValue.IF_TRUE3)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE3
(String.intValue.IF_FALSE3)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.setInt 4
(String.setInt)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@4
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop pointer 0
@SP
AM = M - 1
D = M
@THIS
M = D
// push this 0
@0
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction190
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction190)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@String.setInt.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@String.setInt.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(String.setInt.IF_TRUE0)
// push constant 19
@19
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction191
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction191)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(String.setInt.IF_FALSE0)
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction192
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction192)
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction193
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction193)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@String.setInt.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@String.setInt.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(String.setInt.IF_TRUE1)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE1
(String.setInt.IF_FALSE1)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(String.setInt.WHILE_EXP0)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction194
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction194)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@String.setInt.WHILE_END0
D ; JNE
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 10
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction195
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction195)
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 10
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction196
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction196)
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 1
@1
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@String.setInt.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(String.setInt.WHILE_END0)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@String.setInt.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@String.setInt.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(String.setInt.IF_TRUE2)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 45
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE2
(String.setInt.IF_FALSE2)
// push this 0
@0
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction197
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction197)
// if-goto IF_TRUE3
@SP
AM = M - 1
D = M
@String.setInt.IF_TRUE3
D ; JNE
// goto IF_FALSE3
@String.setInt.IF_FALSE3
0 ; JMP
// label IF_TRUE3
(String.setInt.IF_TRUE3)
// push constant 19
@19
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction198
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction198)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE3
(String.setInt.IF_FALSE3)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction199
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction199)
// if-goto IF_TRUE4
@SP
AM = M - 1
D = M
@String.setInt.IF_TRUE4
D ; JNE
// goto IF_FALSE4
@String.setInt.IF_FALSE4
0 ; JMP
// label IF_TRUE4
(String.setInt.IF_TRUE4)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop this 2
@2
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END4
@String.setInt.IF_END4
0 ; JMP
// label IF_FALSE4
(String.setInt.IF_FALSE4)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop this 2
@2
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP1
(String.setInt.WHILE_EXP1)
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction200
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction200)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END1
@SP
AM = M - 1
D = M
@String.setInt.WHILE_END1
D ; JNE
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 1
@1
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push this 2
@2
D = A
@THIS
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop this 2
@2
D = A
@THIS
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP1
@String.setInt.WHILE_EXP1
0 ; JMP
// label WHILE_END1
(String.setInt.WHILE_END1)
// label IF_END4
(String.setInt.IF_END4)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Array.dispose 1
@Array.dispose
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction201
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction201)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.newLine 0
(String.newLine)
// push constant 128
@128
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.backSpace 0
(String.backSpace)
// push constant 129
@129
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function String.doubleQuote 0
(String.doubleQuote)
// push constant 34
@34
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Sys ===

// function Sys.init 0
(Sys.init)
// call Memory.init 0
@Memory.init
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction202
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction202)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Math.init 0
@Math.init
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction203
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction203)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Screen.init 0
@Screen.init
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction204
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction204)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Output.init 0
@Output.init
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction205
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction205)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Keyboard.init 0
@Keyboard.init
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction206
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction206)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Main.main 0
@Main.main
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction207
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction207)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Sys.halt 0
@Sys.halt
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction208
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction208)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Sys.halt 0
(Sys.halt)
// label WHILE_EXP0
(Sys.halt.WHILE_EXP0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Sys.halt.WHILE_END0
D ; JNE
// goto WHILE_EXP0
@Sys.halt.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Sys.halt.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Sys.wait 1
(Sys.wait)
@SP
A = M
M = 0
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction209
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction209)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Sys.wait.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Sys.wait.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Sys.wait.IF_TRUE0)
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction210
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction210)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Sys.wait.IF_FALSE0)
// label WHILE_EXP0
(Sys.wait.WHILE_EXP0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction211
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction211)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Sys.wait.WHILE_END0
D ; JNE
// push constant 50
@50
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP1
(Sys.wait.WHILE_EXP1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction212
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction212)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END1
@SP
AM = M - 1
D = M
@Sys.wait.WHILE_END1
D ; JNE
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP1
@Sys.wait.WHILE_EXP1
0 ; JMP
// label WHILE_END1
(Sys.wait.WHILE_END1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Sys.wait.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Sys.wait.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Sys.error 0
(Sys.error)
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.new 1
@String.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction213
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction213)
// push constant 69
@69
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction214
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction214)
// push constant 82
@82
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction215
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction215)
// push constant 82
@82
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.appendChar 2
@String.appendChar
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction216
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction216)
// call Output.printString 1
@Output.printString
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction217
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction217)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Output.printInt 1
@Output.printInt
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction218
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction218)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Sys.halt 0
@Sys.halt
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction219
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction219)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP

// === Output ===

// function Output.init 0
(Output.init)
// push constant 16384
@16384
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 4
@SP
AM = M - 1
D = M
@Output.4
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop static 2
@SP
AM = M - 1
D = M
@Output.2
M = D
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 0
@SP
AM = M - 1
D = M
@Output.0
M = D
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call String.new 1
@String.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction220
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction220)
// pop static 3
@SP
AM = M - 1
D = M
@Output.3
M = D
// call Output.initMap 0
@Output.initMap
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction221
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction221)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// call Output.createShiftedMap 0
@Output.createShiftedMap
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction222
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction222)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.initMap 0
(Output.initMap)
// push constant 127
@127
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction223
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction223)
// pop static 5
@SP
AM = M - 1
D = M
@Output.5
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction224
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction224)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction225
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction225)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 33
@33
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction226
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction226)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 34
@34
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 20
@20
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction227
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction227)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction228
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction228)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 36
@36
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction229
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction229)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 37
@37
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 49
@49
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction230
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction230)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 38
@38
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction231
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction231)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 39
@39
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction232
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction232)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 40
@40
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction233
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction233)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 41
@41
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction234
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction234)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 42
@42
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction235
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction235)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 43
@43
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction236
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction236)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 44
@44
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction237
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction237)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 45
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction238
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction238)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 46
@46
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction239
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction239)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 47
@47
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction240
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction240)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction241
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction241)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 49
@49
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction242
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction242)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 50
@50
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction243
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction243)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction244
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction244)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 52
@52
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 16
@16
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 26
@26
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 25
@25
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 60
@60
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction245
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction245)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 53
@53
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction246
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction246)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction247
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction247)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 55
@55
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 49
@49
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction248
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction248)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 56
@56
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction249
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction249)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 57
@57
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 62
@62
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction250
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction250)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 58
@58
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction251
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction251)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction252
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction252)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 60
@60
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction253
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction253)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 61
@61
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction254
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction254)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 62
@62
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction255
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction255)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 64
@64
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction256
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction256)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction257
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction257)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 65
@65
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction258
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction258)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 66
@66
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction259
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction259)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 67
@67
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction260
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction260)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 68
@68
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction261
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction261)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 69
@69
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction262
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction262)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 70
@70
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction263
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction263)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 71
@71
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 44
@44
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction264
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction264)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 72
@72
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction265
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction265)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 73
@73
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction266
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction266)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 74
@74
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 60
@60
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction267
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction267)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 75
@75
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction268
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction268)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 76
@76
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction269
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction269)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 77
@77
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 33
@33
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction270
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction270)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 78
@78
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 55
@55
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 55
@55
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction271
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction271)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 79
@79
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction272
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction272)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 80
@80
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction273
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction273)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 81
@81
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 59
@59
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction274
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction274)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 82
@82
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction275
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction275)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 83
@83
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction276
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction276)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 84
@84
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 45
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction277
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction277)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 85
@85
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction278
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction278)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 86
@86
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction279
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction279)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 87
@87
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction280
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction280)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 88
@88
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction281
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction281)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 89
@89
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction282
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction282)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 90
@90
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 49
@49
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 35
@35
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction283
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction283)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 91
@91
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction284
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction284)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 92
@92
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction285
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction285)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 93
@93
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction286
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction286)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 94
@94
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 8
@8
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction287
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction287)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 95
@95
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction288
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction288)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 96
@96
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction289
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction289)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 97
@97
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction290
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction290)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 98
@98
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction291
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction291)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 99
@99
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction292
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction292)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 100
@100
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 60
@60
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction293
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction293)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 101
@101
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction294
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction294)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 102
@102
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 38
@38
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction295
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction295)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 103
@103
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 62
@62
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction296
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction296)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 104
@104
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 55
@55
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction297
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction297)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 105
@105
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction298
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction298)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 106
@106
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 56
@56
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction299
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction299)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 107
@107
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction300
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction300)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 108
@108
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 14
@14
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction301
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction301)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 109
@109
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 29
@29
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 43
@43
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 43
@43
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 43
@43
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 43
@43
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction302
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction302)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 110
@110
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 29
@29
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction303
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction303)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 111
@111
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction304
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction304)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 112
@112
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction305
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction305)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 113
@113
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 62
@62
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction306
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction306)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 114
@114
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 29
@29
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 55
@55
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction307
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction307)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 115
@115
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction308
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction308)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 116
@116
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 4
@4
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 28
@28
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction309
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction309)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 117
@117
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 54
@54
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction310
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction310)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 118
@118
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction311
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction311)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 119
@119
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 18
@18
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction312
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction312)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 120
@120
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 30
@30
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction313
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction313)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 121
@121
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 62
@62
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 48
@48
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 24
@24
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 15
@15
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction314
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction314)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 122
@122
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 27
@27
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 51
@51
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction315
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction315)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 123
@123
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 56
@56
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 56
@56
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction316
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction316)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 124
@124
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction317
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction317)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 125
@125
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 56
@56
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 12
@12
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction318
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction318)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 126
@126
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 38
@38
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 45
@45
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 25
@25
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.create 12
@Output.create
D = A
@14
M = D
@12
D = A
@15
M = D
@$_returnFromGenericFunction319
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction319)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.create 1
(Output.create)
@SP
A = M
M = 0
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction320
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction320)
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 5
@Output.5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 2
@2
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 3
@3
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 3
@3
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 4
@4
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 4
@4
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 5
@5
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 5
@5
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 6
@6
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 6
@6
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 7
@7
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 7
@7
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 8
@8
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 8
@8
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 9
@9
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 9
@9
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 10
@10
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 10
@10
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push argument 11
@11
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.createShiftedMap 4
(Output.createShiftedMap)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@4
D = A
@SP
M = M + D
// push constant 127
@127
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction321
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction321)
// pop static 6
@SP
AM = M - 1
D = M
@Output.6
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Output.createShiftedMap.WHILE_EXP0)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 127
@127
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction322
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction322)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Output.createShiftedMap.WHILE_END0
D ; JNE
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 5
@Output.5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Array.new 1
@Array.new
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction323
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction323)
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 6
@Output.6
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP1
(Output.createShiftedMap.WHILE_EXP1)
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction324
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction324)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END1
@SP
AM = M - 1
D = M
@Output.createShiftedMap.WHILE_END1
D ; JNE
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 256
@256
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction325
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction325)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP1
@Output.createShiftedMap.WHILE_EXP1
0 ; JMP
// label WHILE_END1
(Output.createShiftedMap.WHILE_END1)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction326
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction326)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.createShiftedMap.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.createShiftedMap.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.createShiftedMap.IF_TRUE0)
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END0
@Output.createShiftedMap.IF_END0
0 ; JMP
// label IF_FALSE0
(Output.createShiftedMap.IF_FALSE0)
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END0
(Output.createShiftedMap.IF_END0)
// goto WHILE_EXP0
@Output.createShiftedMap.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Output.createShiftedMap.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.getMap 1
(Output.getMap)
@SP
A = M
M = 0
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction327
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction327)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 126
@126
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction328
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction328)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.getMap.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.getMap.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.getMap.IF_TRUE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop argument 0
@0
D = A
@ARG
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Output.getMap.IF_FALSE0)
// push static 2
@Output.2
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Output.getMap.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Output.getMap.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Output.getMap.IF_TRUE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 5
@Output.5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END1
@Output.getMap.IF_END1
0 ; JMP
// label IF_FALSE1
(Output.getMap.IF_FALSE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 6
@Output.6
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END1
(Output.getMap.IF_END1)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.drawChar 4
(Output.drawChar)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@4
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Output.getMap 1
@Output.getMap
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction329
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction329)
// pop local 2
@2
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Output.drawChar.WHILE_EXP0)
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 11
@11
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction330
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction330)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Output.drawChar.WHILE_END0
D ; JNE
// push static 2
@Output.2
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.drawChar.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.drawChar.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.drawChar.IF_TRUE0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 4
@Output.4
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 256
@256
D = A
@SP
A = M
M = D
@SP
M = M + 1
// neg
@SP
A = M - 1
M = - M
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END0
@Output.drawChar.IF_END0
0 ; JMP
// label IF_FALSE0
(Output.drawChar.IF_FALSE0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 4
@Output.4
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 255
@255
D = A
@SP
A = M
M = D
@SP
M = M + 1
// and
@SP
AM = M - 1
D = M
A = A - 1
M = M & D
// pop local 3
@3
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_END0
(Output.drawChar.IF_END0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 4
@Output.4
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 2
@2
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push that 0
@0
D = A
@THAT
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 3
@3
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// pop pointer 1
@SP
AM = M - 1
D = M
@THAT
M = D
// push temp 0
@5
D = M
@SP
A = M
M = D
@SP
M = M + 1
// pop that 0
@0
D = A
@THAT
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Output.drawChar.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Output.drawChar.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.moveCursor 0
(Output.moveCursor)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction331
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction331)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 22
@22
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction332
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction332)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction333
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction333)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 63
@63
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction334
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction334)
// or
@SP
AM = M - 1
D = M
A = A - 1
M = M | D
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.moveCursor.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.moveCursor.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.moveCursor.IF_TRUE0)
// push constant 20
@20
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Sys.error 1
@Sys.error
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction335
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction335)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label IF_FALSE0
(Output.moveCursor.IF_FALSE0)
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.divide 2
@Math.divide
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction336
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction336)
// pop static 0
@SP
AM = M - 1
D = M
@Output.0
M = D
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 352
@352
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction337
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction337)
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// push argument 1
@1
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 2
@2
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Math.multiply 2
@Math.multiply
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction338
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction338)
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction339
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction339)
// pop static 2
@SP
AM = M - 1
D = M
@Output.2
M = D
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.drawChar 1
@Output.drawChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction340
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction340)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.printChar 0
(Output.printChar)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.newLine 0
@String.newLine
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction341
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction341)
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction342
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction342)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.printChar.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.printChar.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.printChar.IF_TRUE0)
// call Output.println 0
@Output.println
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction343
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction343)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END0
@Output.printChar.IF_END0
0 ; JMP
// label IF_FALSE0
(Output.printChar.IF_FALSE0)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.backSpace 0
@String.backSpace
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction344
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction344)
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction345
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction345)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Output.printChar.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Output.printChar.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Output.printChar.IF_TRUE1)
// call Output.backSpace 0
@Output.backSpace
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction346
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction346)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END1
@Output.printChar.IF_END1
0 ; JMP
// label IF_FALSE1
(Output.printChar.IF_FALSE1)
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Output.drawChar 1
@Output.drawChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction347
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction347)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push static 2
@Output.2
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Output.printChar.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Output.printChar.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Output.printChar.IF_TRUE2)
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop static 0
@SP
AM = M - 1
D = M
@Output.0
M = D
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// label IF_FALSE2
(Output.printChar.IF_FALSE2)
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction348
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction348)
// if-goto IF_TRUE3
@SP
AM = M - 1
D = M
@Output.printChar.IF_TRUE3
D ; JNE
// goto IF_FALSE3
@Output.printChar.IF_FALSE3
0 ; JMP
// label IF_TRUE3
(Output.printChar.IF_TRUE3)
// call Output.println 0
@Output.println
D = A
@14
M = D
@0
D = A
@15
M = D
@$_returnFromGenericFunction349
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction349)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto IF_END3
@Output.printChar.IF_END3
0 ; JMP
// label IF_FALSE3
(Output.printChar.IF_FALSE3)
// push static 2
@Output.2
D = M
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop static 2
@SP
AM = M - 1
D = M
@Output.2
M = D
// label IF_END3
(Output.printChar.IF_END3)
// label IF_END1
(Output.printChar.IF_END1)
// label IF_END0
(Output.printChar.IF_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.printString 2
(Output.printString)
@SP
D = M
A = D
M = 0
D = D + 1
A = D
M = 0
D = D + 1
@2
D = A
@SP
M = M + D
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.length 1
@String.length
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction350
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction350)
// pop local 1
@1
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// label WHILE_EXP0
(Output.printString.WHILE_EXP0)
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 1
@1
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// lt
@$_lessThan
D = A
@14
M = D
@$_returnFromGenericFunction351
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction351)
// not
@SP
A = M - 1
M = ! M
// if-goto WHILE_END0
@SP
AM = M - 1
D = M
@Output.printString.WHILE_END0
D ; JNE
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.charAt 2
@String.charAt
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction352
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction352)
// call Output.printChar 1
@Output.printChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction353
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction353)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push local 0
@0
D = A
@LCL
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// pop local 0
@0
D = A
@LCL
D = M + D
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// goto WHILE_EXP0
@Output.printString.WHILE_EXP0
0 ; JMP
// label WHILE_END0
(Output.printString.WHILE_END0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.printInt 0
(Output.printInt)
// push static 3
@Output.3
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push argument 0
@0
D = A
@ARG
A = M + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call String.setInt 2
@String.setInt
D = A
@14
M = D
@2
D = A
@15
M = D
@$_returnFromGenericFunction354
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction354)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push static 3
@Output.3
D = M
@SP
A = M
M = D
@SP
M = M + 1
// call Output.printString 1
@Output.printString
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction355
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction355)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.println 0
(Output.println)
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 352
@352
D = A
@SP
A = M
M = D
@SP
M = M + 1
// add
@SP
AM = M - 1
D = M
A = A - 1
M = M + D
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 0
@SP
AM = M - 1
D = M
@Output.0
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop static 2
@SP
AM = M - 1
D = M
@Output.2
M = D
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 8128
@8128
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction356
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction356)
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.println.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.println.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.println.IF_TRUE0)
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// label IF_FALSE0
(Output.println.IF_FALSE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP
// function Output.backSpace 0
(Output.backSpace)
// push static 2
@Output.2
D = M
@SP
A = M
M = D
@SP
M = M + 1
// if-goto IF_TRUE0
@SP
AM = M - 1
D = M
@Output.backSpace.IF_TRUE0
D ; JNE
// goto IF_FALSE0
@Output.backSpace.IF_FALSE0
0 ; JMP
// label IF_TRUE0
(Output.backSpace.IF_TRUE0)
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// gt
@$_greaterThan
D = A
@14
M = D
@$_returnFromGenericFunction357
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction357)
// if-goto IF_TRUE1
@SP
AM = M - 1
D = M
@Output.backSpace.IF_TRUE1
D ; JNE
// goto IF_FALSE1
@Output.backSpace.IF_FALSE1
0 ; JMP
// label IF_TRUE1
(Output.backSpace.IF_TRUE1)
// push static 0
@Output.0
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop static 0
@SP
AM = M - 1
D = M
@Output.0
M = D
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 1
@1
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// goto IF_END1
@Output.backSpace.IF_END1
0 ; JMP
// label IF_FALSE1
(Output.backSpace.IF_FALSE1)
// push constant 31
@31
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 0
@SP
AM = M - 1
D = M
@Output.0
M = D
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// eq
@$_equal
D = A
@14
M = D
@$_returnFromGenericFunction358
D = A
@15
M = D
@$_genericComparisonOp
0 ; JMP
($_returnFromGenericFunction358)
// if-goto IF_TRUE2
@SP
AM = M - 1
D = M
@Output.backSpace.IF_TRUE2
D ; JNE
// goto IF_FALSE2
@Output.backSpace.IF_FALSE2
0 ; JMP
// label IF_TRUE2
(Output.backSpace.IF_TRUE2)
// push constant 8128
@8128
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// label IF_FALSE2
(Output.backSpace.IF_FALSE2)
// push static 1
@Output.1
D = M
@SP
A = M
M = D
@SP
M = M + 1
// push constant 321
@321
D = A
@SP
A = M
M = D
@SP
M = M + 1
// sub
@SP
AM = M - 1
D = M
A = A - 1
M = M - D
// pop static 1
@SP
AM = M - 1
D = M
@Output.1
M = D
// label IF_END1
(Output.backSpace.IF_END1)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// pop static 2
@SP
AM = M - 1
D = M
@Output.2
M = D
// goto IF_END0
@Output.backSpace.IF_END0
0 ; JMP
// label IF_FALSE0
(Output.backSpace.IF_FALSE0)
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// not
@SP
A = M - 1
M = ! M
// pop static 2
@SP
AM = M - 1
D = M
@Output.2
M = D
// label IF_END0
(Output.backSpace.IF_END0)
// push constant 32
@32
D = A
@SP
A = M
M = D
@SP
M = M + 1
// call Output.drawChar 1
@Output.drawChar
D = A
@14
M = D
@1
D = A
@15
M = D
@$_returnFromGenericFunction359
D = A
@$_genericCall
0 ; JMP
($_returnFromGenericFunction359)
// pop temp 0
@5
D = A
@13
M = D
@SP
AM = M - 1
D = M
@13
A = M
M = D
// push constant 0
@0
D = A
@SP
A = M
M = D
@SP
M = M + 1
// return
@$_genericReturn
0 ; JMP