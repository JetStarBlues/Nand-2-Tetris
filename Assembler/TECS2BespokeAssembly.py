# Convert TECS style assembly code, to Hack2 assembly

'''
	@#
	@label           // will need a pass to translate labels to constants...
	dst = cmp ; jmp
	(label)
'''

'''
	A -> r1
	D -> r2
'''

# Assumes program only 32k?

# Assumes no whitespace in TECS instruction, and
#  code is compliant (ex valid integers)

regs = {
	
	'rA' : 'r1',
	'rD' : 'r2',
	'rT' : 'r3',
	# r4 reserved
}

compLookup = {

	'0'   : [

		'MOV {} r0'
	],
	'1'   : [

		'MOV {} r0 1'
	],
	'-1'  : [

		'NEG {} r0 1'
	],
	# ---
	'D'   : [

		'MOV {} rD'
	],
	'A'   : [

		'MOV {} rA'
	],
	# ---
	'!D'  : [

		'NOT {} rD'
	],
	'!A'  : [

		'NOT {} rA'
	],
	# ---
	'-D'  : [

		'NEG {} rD'
	],
	'-A'  : [

		'NEG {} rA'
	],
	# ---
	'D+1' : [

		'MOV {} rD',
		'ADD {} r0 1'
	],
	'A+1' : [

		'MOV {} rA',
		'ADD {} r0 1'
	],
	'D-1' : [

		'MOV {} rD',
		'SUB {} r0 1'
	],
	'A-1' : [

		'MOV {} rA',
		'SUB {} r0 1'
	],
	# ---
	'D+A' : [

		'MOV {} rD',
		'ADD {} rA'
	],
	'A+D' : None,  # order doesn't matter
	'D-A' : [

		'MOV {} rD',
		'SUB {} rA'
	],
	'A-D' : [

		'MOV {} rA',
		'SUB {} rD'
	],
	'D&A' : [

		'MOV {} rD',
		'AND {} rA'
	],
	'A&D' : None,  # order doesn't matter
	'D|A' : [

		'MOV {} rD',
		'OR  {} rA'
	],
	'A|D' : None,  # order doesn't matter
	# ---
	'M'   : [

		'LD  {} rA',
	],
	# ---
	'!M'  : [

		'LD  {} rA',
		'NOT {} {}'
	],
	'-M'  : [

		'LD  {} rA',
		'NEG {} {}'
	],
	# ---
	'M+1' : [

		'LD  {} rA',
		'ADD {} r0 1'
	],
	'M-1' : [

		'LD  {} rA',
		'SUB {} r0 1'
	],
	# ---
	'D+M' : [

		'LD  {} rA',
		'ADD {} rD'
	],
	'M+D' : None,  # order doesn't matter
	'D-M' : [

		'LD  rT rA',
		'MOV {} rD',
		'SUB {} rT'
	],
	'M-D' : [

		'LD  {} rA',
		'SUB {} rD'
	],
	'D&M' : [

		'LD  {} rA',
		'AND {} rD'
	],
	'M&D' : None,  # order doesn't matter
	'D|M' : [

		'LD  {} rA',
		'OR  {} rD'
	],
	'M|D' : None,  # order doesn't matter
}

# order doesn't matter
compLookup[ 'A+D' ] = compLookup[ 'D+A' ]
compLookup[ 'A&D' ] = compLookup[ 'D&A' ]
compLookup[ 'A|D' ] = compLookup[ 'D|A' ]
compLookup[ 'M+D' ] = compLookup[ 'D+M' ]
compLookup[ 'M&D' ] = compLookup[ 'D&M' ]
compLookup[ 'M|D' ] = compLookup[ 'D|M' ]


jumpLookup = {
		
	'NULL' : [],
	'JGT'  : [],
	'JEQ'  : [],
	'JLT'  : [],
	'JGE'  : [],
	'JLE'  : [],
	'JNE'  : [],
	'JMP'  : []
}


def aType ( inst )

	new_inst = []

	x = int( inst[ 1 : ] )

	i0 = 'MOV {} r0 {}'.format( regs[ 'A' ], x )

	new_inst.append( i0 )

	return new_inst


def translateComp ( comp, dest, destIsDirect ):

	new_inst = compLookup[ comp ]

	# Replace rA/rD/rT with appropriate register
	#  Note, assuming instructions in uppercase thus won't collide in search/replace
	for curName, newName in regs:

		for i in range( len( new_inst ) ):

			new_inst[ i ] = new_inst[ i ].replace( curName, newName )

	# Place r4/rDst
	if destIsDirect:

		new_inst[ i ] = new_inst[ i ].replace( '{}', dest )

	else:

		new_inst[ i ] = new_inst[ i ].replace( '{}', 'r4' )

	return new_inst


def cType ( inst )

	# Decode
	dest, comp, jump = [ None ] * 3

	if '=' in inst and ';' in inst:
		dest, comp, jump = re.split( '=|;', inst )

	elif '=' in inst:
		dest, comp = re.split( '=', inst )

	elif ';' in inst:
		comp, jump = re.split( ';', inst )


	# Convert comp
	destIsDirect = dest and dest in 'AD'

	new_inst = translateComp( comp, dest, destIsDirect )


	# Convert rest of instruction

	# dst = cmp
	if ( dest and comp and not jump ):

		if not destIsDirect:  # M

			i0 = 'STO r4 {}'.format( regs[ 'A' ] )
			
			new_inst.append( i0 )

	# cmp ; jmp
	elif ( not dest and comp and jump ):

		i0 = '{} r0 {}'.format( jump, regs[ 'A' ] )

		...

		new_inst.append( i0 )

	# dst = cmp ; jmp
	elif ( dest and comp and jump ):

		#

	else:

		raise Exception( 'Error: unkown instruction {}'.format( instr ) )

