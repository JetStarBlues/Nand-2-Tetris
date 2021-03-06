// --- Custom splash screen ----
//  Designed for the Hack computer
//   by @github/jetstarblues


// === Setup ===

// colors

	@0 		// '0000000000000000'
	D = A
	@color0
	M = D
	@4369 	// '0001000100010001'
	D = A
	@color1
	M = D
	@8738 	// '0010001000100010'
	D = A
	@color2
	M = D
	@13107 	// '0011001100110011'
	D = A
	@color3
	M = D
	@17476
	D = A
	@color4
	M = D
	@21845
	D = A
	@color5
	M = D
	@26214
	D = A
	@color6
	M = D
	@30583
	D = A
	@color7
	M = D
	@34952
	D = A
	@color8
	M = D
	@39321
	D = A
	@color9
	M = D
	@43690
	D = A
	@color10
	M = D
	@48059
	D = A
	@color11
	M = D
	@52428
	D = A
	@color12
	M = D
	@56797
	D = A
	@color13
	M = D
	@61166
	D = A
	@color14
	M = D
	@65535
	D = A
	@color15
	M = D


// program variables

	@i
	M = 0 		// @i = 0

	@addr
	M = 0 		// @addr = 0

	@addr1
	M = 0 		// @addr1 = 0

	@addr2
	M = 0 		// @addr2 = 0

	@addr3
	M = 0 		// @addr3 = 0

	@color
	M = 0 		// @color = 0

	@rect_idx
	M = 1 		// @rect_idx = 1

	@11
	D = A
	@n_rects
	M = D 		// @n_rects = 11


// rect1
	// start position
	@SCREEN	
	D = A
	@a_rect1
	M = D 		// @a_rect1 = @SCREEN
	@6196		// ( 16 * ( 32 * 3 ) + 13 ) * 4
	D = A
	@a_rect1
	M = D + M 	// @a_rect1 += 6196

	// height
	@96			// 16 * 6
	D = A
	@h_rect1
	M = D 		// @h_rect1 = 96


// rect2
	// start position
	@SCREEN
	D = A
	@a_rect2
	M = D
	@6200		// ( 16 * ( 32 * 3 ) + 14 ) * 4
	D = A
	@a_rect2
	M = D + M

	// height
	@16			// 16 * 1
	D = A
	@h_rect2
	M = D


// rect3
	// start position
	@SCREEN
	D = A
	@a_rect3
	M = D
	@10296		// ( 16 * ( 32 * 5 ) + 14 ) * 4
	D = A
	@a_rect3
	M = D + M

	// height
	@32			// 16 * 2
	D = A
	@h_rect3
	M = D


// rect4
	// start position
	@SCREEN
	D = A
	@a_rect4
	M = D
	@16440		// ( 16 * ( 32 * 8 ) + 14 ) * 4
	D = A
	@a_rect4
	M = D + M

	// height
	@16			// 16 * 1
	D = A
	@h_rect4
	M = D


// rect5
	// start position
	@SCREEN
	D = A
	@a_rect5
	M = D
	@6204		// ( 16 * ( 32 * 3 ) + 15 ) * 4
	D = A
	@a_rect5
	M = D + M

	// height
	@96			// 16 * 6
	D = A
	@h_rect5
	M = D


// rect6
	// start position
	@SCREEN
	D = A
	@a_rect6
	M = D
	@12352		// ( 16 * ( 32 * 6 ) + 16 ) * 4
	D = A
	@a_rect6
	M = D + M

	// height
	@96			// 16 * 6
	D = A
	@h_rect6
	M = D


// rect7
	// start position
	@SCREEN
	D = A
	@a_rect7
	M = D
	@12356		// ( 16 * ( 32 * 6 ) + 17 ) * 4
	D = A
	@a_rect7
	M = D + M

	// height
	@16			// 16 * 1
	D = A
	@h_rect7
	M = D


// rect8
	// start position
	@SCREEN
	D = A
	@a_rect8
	M = D
	@16452		// ( 16 * ( 32 * 8 ) + 17 ) * 4
	D = A
	@a_rect8
	M = D + M

	// height
	@32			// 16 * 2
	D = A
	@h_rect8
	M = D


// rect9
	// start position
	@SCREEN
	D = A
	@a_rect9
	M = D
	@22596		// ( 16 * ( 32 * 11 ) + 17 ) * 4
	D = A
	@a_rect9
	M = D + M

	// height
	@16			// 16 * 1
	D = A
	@h_rect9
	M = D


// rect10
	// start position
	@SCREEN
	D = A
	@a_rect10
	M = D
	@12360		// ( 16 * ( 32 * 6 ) + 18 ) * 4
	D = A
	@a_rect10
	M = D + M

	// height
	@96			// 16 * 6
	D = A
	@h_rect10
	M = D



// === Main loop ===

(SETUP_rect)

	// if rect_idx == n_rects, goto END
	@n_rects
	D = M
	@rect_idx
	D = D - M
	@END
	D ; JEQ

	// if rect_idx == 10, goto SETUP_rect10
	@10
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect10
	D ; JEQ

	// if rect_idx == 9, goto SETUP_rect9
	@9
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect9
	D ; JEQ
	
	// if rect_idx == 8, goto SETUP_rect8
	@8
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect8
	D ; JEQ
	
	// if rect_idx == 7, goto SETUP_rect7
	@7
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect7
	D ; JEQ
	
	// if rect_idx == 6, goto SETUP_rect6
	@6
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect6
	D ; JEQ
	
	// if rect_idx == 5, goto SETUP_rect5
	@5
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect5
	D ; JEQ
	
	// if rect_idx == 4, goto SETUP_rect4
	@4
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect4
	D ; JEQ

	// if rect_idx == 3, goto SETUP_rect3
	@3
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect3
	D ; JEQ

	// if rect_idx == 2, goto SETUP_rect2
	@2
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect2
	D ; JEQ

	// if rect_idx == 1, goto SETUP_rect1
	@1
	D = A
	@rect_idx
	D = D - M
	@SETUP_rect1
	D ; JEQ	


(LOOP_rect)

	@i
	D = M
	@h
	D = D - M
	@SETUP_rect
	D ; JEQ 	// if i == h, goto next rect

	// @addr
	// A = M 		
	// M = -1	// RAM[ @addr ] = -1

	@ addr
	D = M
	@ addr1
	MD = D + 1 	// @addr1 = @addr  + 1
	@ addr2
	MD = D + 1 	// @addr2 = @addr1 + 1
	@ addr3
	MD = D + 1 	// @addr3 = @addr2 + 1

	@color
	D = M

	@addr
	A = M
	M = D 		// RAM[ @addr  ] = color
	@addr1
	A = M
	M = D 		// RAM[ @addr1 ] = color
	@addr2
	A = M
	M = D 		// RAM[ @addr2 ] = color
	@addr3
	A = M
	M = D 		// RAM[ @addr3 ] = color

	@128
	D = A
	@addr
	M = D + M 	// @addr += 32 * 4

	@i
	M = M + 1 	// @i += 1

	@LOOP_rect
	0 ; JMP


(SETUP_rect1)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color3
	D = M
	@color
	M = D

	@a_rect1
	D = M
	@addr
	M = D

	@h_rect1
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect2)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color6
	D = M
	@color
	M = D

	@a_rect2
	D = M
	@addr
	M = D

	@h_rect2
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect3)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color7
	D = M
	@color
	M = D

	@a_rect3
	D = M
	@addr
	M = D

	@h_rect3
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect4)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color8
	D = M
	@color
	M = D

	@a_rect4
	D = M
	@addr
	M = D

	@h_rect4
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect5)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color9
	D = M
	@color
	M = D

	@a_rect5
	D = M
	@addr
	M = D

	@h_rect5
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect6)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color10
	D = M
	@color
	M = D

	@a_rect6
	D = M
	@addr
	M = D

	@h_rect6
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect7)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color11
	D = M
	@color
	M = D

	@a_rect7
	D = M
	@addr
	M = D

	@h_rect7
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect8)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color12
	D = M
	@color
	M = D

	@a_rect8
	D = M
	@addr
	M = D

	@h_rect8
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect9)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color13
	D = M
	@color
	M = D

	@a_rect9
	D = M
	@addr
	M = D

	@h_rect9
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP


(SETUP_rect10)

	@rect_idx
	M = M + 1

	@i
	M = 0

	@color14
	D = M
	@color
	M = D

	@a_rect10
	D = M
	@addr
	M = D

	@h_rect10
	D = M
	@h
	M = D

	@LOOP_rect
	0 ; JMP



// === End loop ===

(END)
	@END
	0 ; JMP
