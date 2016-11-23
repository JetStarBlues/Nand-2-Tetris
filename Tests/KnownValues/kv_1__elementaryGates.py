'''
	Comparison data as seen here,
	 http://www.nand2tetris.org/
'''

'''------------------------- Elementary gates -------------------------'''

k_and = [ 
	# [ a, b, out ]
	[ 0, 0, 0 ],
	[ 0, 1, 0 ],
	[ 1, 0, 0 ],
	[ 1, 1, 1 ]
]

k_and16 = [
	# [ a, b, out ]
	[ '0000000000000000', '0000000000000000', '0000000000000000' ],
	[ '0000000000000000', '1111111111111111', '0000000000000000' ],
	[ '1111111111111111', '1111111111111111', '1111111111111111' ],
	[ '1010101010101010', '0101010101010101', '0000000000000000' ],
	[ '0011110011000011', '0000111111110000', '0000110011000000' ],
	[ '0001001000110100', '1001100001110110', '0001000000110100' ],
]

k_not = [
	# [ in, out ]
	[ 0, 1 ],
	[ 1, 0 ],
]

k_not16 = [
	# [ in, out ]
	[ '0000000000000000', '1111111111111111' ],
	[ '1111111111111111', '0000000000000000' ],
	[ '1010101010101010', '0101010101010101' ],
	[ '0011110011000011', '1100001100111100' ],
	[ '0001001000110100', '1110110111001011' ],
]

k_or = [
	# [ a, b, out ]
	[ 0, 0, 0 ],
	[ 0, 1, 1 ],
	[ 1, 0, 1 ],
	[ 1, 1, 1 ],
]

k_or16 = [
	# [ a, b, out ]
	[ '0000000000000000', '0000000000000000', '0000000000000000' ],
	[ '0000000000000000', '1111111111111111', '1111111111111111' ],
	[ '1111111111111111', '1111111111111111', '1111111111111111' ],
	[ '1010101010101010', '0101010101010101', '1111111111111111' ],
	[ '0011110011000011', '0000111111110000', '0011111111110011' ],
	[ '0001001000110100', '1001100001110110', '1001101001110110' ],
]

k_xor = [
	# [ a, b, out ]
	[ 0, 0, 0 ],
	[ 0, 1, 1 ],
	[ 1, 0, 1 ],
	[ 1, 1, 0 ],
]

k_decoder1to2 = [
	# [ d, out ]
	[ 0, '01' ],
	[ 1, '10' ]
]

k_decoder2to4 = [
	# [ d1, d0, out ]
	[ 0, 0, '0001' ],
	[ 0, 1, '0010' ],
	[ 1, 0, '0100' ],
	[ 1, 1, '1000' ]
]

k_decoder3to8 = [
	# [ d2, d1, d0, out ]
	[  0, 0, 0, '00000001' ],
	[  0, 0, 1, '00000010' ],
	[  0, 1, 0, '00000100' ],
	[  0, 1, 1, '00001000' ],
	[  1, 0, 0, '00010000' ],
	[  1, 0, 1, '00100000' ],
	[  1, 1, 0, '01000000' ],
	[  1, 1, 1, '10000000' ]
]

k_encoder2to1 = [
	# [ d1, d0, out ]
	[ 0, 1, 0 ],
	[ 1, 0, 1 ]
]

k_encoder4to2 = [
	# [ d3, d2, d1, d0, out ]
	[ 0, 0, 0, 1, '00' ],
	[ 0, 0, 1, 0, '01' ],
	[ 0, 1, 0, 0, '10' ],
	[ 1, 0, 0, 0, '11' ]
]

k_encoder8to3 = [
	# [ d7, d6, d5, d4, d3, d2, d1, d0, out ]
	[ 0, 0, 0, 0, 0, 0, 0, 1, '000' ],
	[ 0, 0, 0, 0, 0, 0, 1, 0, '001' ],
	[ 0, 0, 0, 0, 0, 1, 0, 0, '010' ],
	[ 0, 0, 0, 0, 1, 0, 0, 0, '011' ],
	[ 0, 0, 0, 1, 0, 0, 0, 0, '100' ],
	[ 0, 0, 1, 0, 0, 0, 0, 0, '101' ],
	[ 0, 1, 0, 0, 0, 0, 0, 0, '110' ],
	[ 1, 0, 0, 0, 0, 0, 0, 0, '111' ]
]

k_dMux = [
	# [ in, sel, out ]
	[ 0, 0, '00' ],
	[ 0, 1, '00' ],
	[ 1, 0, '01' ],
	[ 1, 1, '10' ],
]

k_dMux1to4 = [
	# [ in, s1, s0, out ]
	[ 0, 0, 0, '0000' ],
	[ 0, 0, 1, '0000' ],
	[ 0, 1, 0, '0000' ],
	[ 0, 1, 1, '0000' ],
	[ 1, 0, 0, '0001' ],
	[ 1, 0, 1, '0010' ],
	[ 1, 1, 0, '0100' ],
	[ 1, 1, 1, '1000' ],
]

k_dMux1to8 = [
	# [ in, s2, s1, s0, out ]
	[ 0, 0, 0, 0, '00000000' ],
	[ 0, 0, 0, 1, '00000000' ],
	[ 0, 0, 1, 0, '00000000' ],
	[ 0, 0, 1, 1, '00000000' ],
	[ 0, 1, 0, 0, '00000000' ],
	[ 0, 1, 0, 1, '00000000' ],
	[ 0, 1, 1, 0, '00000000' ],
	[ 0, 1, 1, 1, '00000000' ],
	[ 1, 0, 0, 0, '00000001' ],
	[ 1, 0, 0, 1, '00000010' ],
	[ 1, 0, 1, 0, '00000100' ],
	[ 1, 0, 1, 1, '00001000' ],
	[ 1, 1, 0, 0, '00010000' ],
	[ 1, 1, 0, 1, '00100000' ],
	[ 1, 1, 1, 0, '01000000' ],
	[ 1, 1, 1, 1, '10000000' ],
]

k_mux = [
	# [ d1, d0, sel, out ]
	[ 0, 0, 0, 0 ],
	[ 0, 1, 0, 1 ],
	[ 1, 0, 0, 0 ],
	[ 1, 1, 0, 1 ],
	[ 0, 0, 1, 0 ],
	[ 1, 0, 1, 1 ],
	[ 0, 1, 1, 0 ],
	[ 1, 1, 1, 1 ],
]

k_mux16 = [
	# [ d1, d0, sel, out ]
	[ '0000000000000000', '0000000000000000', 1, '0000000000000000' ],
	[ '0000000000000000', '0001001000110100', 1, '0000000000000000' ],
	[ '1001100001110110', '0000000000000000', 1, '1001100001110110' ],
	[ '1010101010101010', '0101010101010101', 1, '1010101010101010' ],
	[ '0000000000000000', '0000000000000000', 0, '0000000000000000' ],
	[ '0000000000000000', '0001001000110100', 0, '0001001000110100' ],
	[ '1001100001110110', '0000000000000000', 0, '0000000000000000' ],
	[ '1010101010101010', '0101010101010101', 0, '0101010101010101' ]
]

k_muxN4to1 = [
	# [ d3, d2, d1, d0, s1, s0, out ]
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 0, 0, '0000000000000000' ],
	[ '0001001000110100', '1001100001110110', '1010101010101010', '0101010101010101', 0, 0, '0101010101010101' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 0, 1, '0000000000000000' ],
	[ '0001001000110100', '1001100001110110', '1010101010101010', '0101010101010101', 0, 1, '1010101010101010' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 1, 0, '0000000000000000' ],
	[ '0001001000110100', '1001100001110110', '1010101010101010', '0101010101010101', 1, 0, '1001100001110110' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 1, 1, '0000000000000000' ],
	[ '0001001000110100', '1001100001110110', '1010101010101010', '0101010101010101', 1, 1, '0001001000110100' ],
]

k_muxN8to1 = [
	# [ d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0, out ]
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 0, 0, 0, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 0, 0, 1, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 0, 1, 0, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 0, 1, 1, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 1, 0, 0, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 1, 0, 1, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 1, 1, 0, '0000000000000000' ],
	[ '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', '0000000000000000', 1, 1, 1, '0000000000000000' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 0, 0, 0, '1000100110101011' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 0, 0, 1, '0111100010011010' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 0, 1, 0, '0110011110001001' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 0, 1, 1, '0101011001111000' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 1, 0, 0, '0100010101100111' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 1, 0, 1, '0011010001010110' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 1, 1, 0, '0010001101000101' ],
	[ '0001001000110100', '0010001101000101', '0011010001010110', '0100010101100111', '0101011001111000', '0110011110001001', '0111100010011010', '1000100110101011', 1, 1, 1, '0001001000110100' ],
]

k_or8to1 = [
	# [ in, out ]
	[ '00000000', 0 ],
	[ '11111111', 1 ],
	[ '00010000', 1 ],
	[ '00000001', 1 ],
	[ '00100110', 1 ],
]
