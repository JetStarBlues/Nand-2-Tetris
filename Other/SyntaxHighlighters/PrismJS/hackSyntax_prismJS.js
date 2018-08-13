// By www.jk-quantized.com

Prism.languages.hackhl = {

	'comment': [ 

		/\/\*[\w\W]*?\*\//,  // multi-line
		/\/\/.*\r?\n/        // single line
	],

	'char': {
		pattern : /(')(\\(?:\r\n|[\w\W])|(?!\1)[^\\\r\n])?\1/,
		greedy: true
	},

	'string': {
		pattern: /(")(\\(?:\r\n|[\w\W])|(?!\1)[^\\\r\n])*\1/,
		greedy: true
	},

	'function': /[A-Za-z_][A-Za-z_0-9]*(?=\s*[\(|{])/i,

	'keyword': /\b(if|else|while|let|do|return|for|include|break|continue|void|bool|char|int|class)\b/,

	'property': /\b(field|static|constructor|method|function|var|const)\b/,

	'constant': /\b(true|false|null|this)\b/,

	'number' : [

		/\b[0-9]+\b/,            // decimal
		/\b0[Bb][01]+\b/,        // binary
		/\b0[Xx][0-9A-Fa-f]+\b/  // hexadecimal
	],

	'punctuation' : /[\.,;\(\)\[\]{}]/,

	'operator' : /(=|==|<=|>=|<|>|!=|-|\+|\*|\/|%|>>|<<|!|~|&|\^|\||&=|\^=|\|=|\-=|\+=|\*=|\/=|%=|>>=|<<=)/,

}

Prism.languages.hackvm = {

	'comment': /\/\/.*\r?\n/,

	'function' : /[A-Za-z_][A-Za-z_0-9]*\.[A-Za-z_][A-Za-z_0-9]*(?=\s+)/,

	'keyword': /\b(push|pop|goto|if-goto|return|add|sub|neg|eq|gt|lt|gte|lte|ne|and|or|not|label|function|call)\b/,

	'property': /\b(argument|constant|local|static|temp|this|that|pointer)\b/,

	'number' : /\b[0-9]+\b/,

}

Prism.languages.hackasm = {

	'comment': /\/\/.*\r?\n/,

	'constant': /\b(NULL|SCREEN|KEYBOARD|MOUSE|R0|R1|R2|R3|R4|R5|R6|R7|R8|R9|R10|R11|R12|R13|R14|R15|SP|LCL|ARG|THIS|THAT|TEMP|GP)\b/,

	'function' : {

		'pattern' : /(@|(\(\s*))[A-Za-z_][A-Za-z_0-9]*/,

		'lookbehind' : true
	},

	'keyword': /@|(\b(JGT|JEQ|JGE|JLT|JNE|JLE|JMP)\b)/,

	'number' : /\b[0-9]+\b/,

	'operator' : /(-|\+|>>|<<|!|&|\^|\||=|;)/,

	'punctuation' : /[\(\)]/,
}