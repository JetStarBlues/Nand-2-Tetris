// ============================================================================
//  Instructions not yet implemented in hardware, but will be in near future
// ============================================================================

// Multiply
MACRO MUL ( _rX_, _rY_, _imm_ )

	...

ENDMACRO

// Divide
MACRO DIV ( _rX_, _rY_, _imm_ )

	...

ENDMACRO


// ============================================================================
//  Common instructions not implemented in hardware, with no plans of doing so
// ============================================================================

// Increment register
MACRO INC ( _rX_ )

	ADD _rX_ r0 1

ENDMACRO

// Decrement register
MACRO INC ( _rX_ )

	SUB _rX_ r0 1

ENDMACRO

// Square root
MACRO SQRT ( _rX_ )

	...

ENDMACRO

// Rotatate right
MACRO ROR ( _rX_ )

	...

ENDMACRO

// double word (32bit) arithmetic...? ex. increment, add

