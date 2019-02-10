// JEQ, JNE, JGT, JLT, JGE, JLE

MACRO JEQ ( _rX_, _rY_, _dest_ )

	CMP  _rX_  _rY_
	JZ   { _dest_ }

ENDMACRO

MACRO JNE ( _rX_, _rY_, _dest_ )

	CMP  _rX_  _rY_
	JNZ  { _dest_ }

ENDMACRO

// stackoverflow.com/a/36909033
MACRO JGT ( _rX_, _rY_, _dest_ )  // JC

	CMP  _rX_  _rY_
	JC   { _dest_ }

ENDMACRO

MACRO JLT ( _rX_, _rY_, _dest_, _rTemp_ )  // NC & NZ

	CMP  _rX_  _rY_
	MOV  _rTemp_  rStatus
	AND  _rTemp_  r0  0b11  // check if both carry(1) and zero(0) bits are clear
	JZ   { _dest_ }

ENDMACRO

MACRO JGE ( _rX_, _rY_, _dest_ )  // C | Z

	CMP  _rX_  _rY_
	JC   { _dest_ }
	JZ   { _dest_ }

ENDMACRO

MACRO JLE ( _rX_, _rY_, _dest_ )  // NC

	CMP  _rX_  _rY_
	JNC  { _dest_ }

ENDMACRO
