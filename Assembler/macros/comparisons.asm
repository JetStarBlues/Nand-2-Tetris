// JEQ, JNE, JGT, JLT, JGE, JLE

MACRO JEQ ( _rValue_, _dest_ )

	SUB  _rValue_    r0
	JZ   { _dest_ }

ENDMACRO

MACRO JNE ( _rValue_, _dest_ )

	SUB  _rValue_    r0
	JNZ  { _dest_ }

ENDMACRO

// stackoverflow.com/a/36909033
MACRO JGT ( _rValue_, _dest_ )  // JC

	SUB  _rValue_   r0
	JC   { _dest_ }

ENDMACRO

MACRO JLT ( _rValue_, _dest_, _rTemp_ )  // NC & NZ

	SUB  _rValue_    r0
	MOV  _rTemp_     rStatus
	AND  _rTemp_     r0       0b110  // check if zero(2) and carry(1) bits are set
	JZ   { _dest_ }  

ENDMACRO

MACRO JGE ( _rValue_, _dest_ )  // C | Z

	SUB  _rValue_    r0
	JC   { _dest_ }  
	JZ   { _dest_ }  

ENDMACRO

MACRO JLE ( _rValue_, _dest_ )  // NC

	SUB  _rValue_    r0
	JNC  { _dest_ }

ENDMACRO
