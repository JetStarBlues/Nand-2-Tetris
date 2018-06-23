// --- Custom splash screen ----
//  Designed for the Hack computer
//   by @github/jetstarblues


// === Setup ===

@i
M = 0 		// @i = 0

@rect_idx
M = 1 		// @rect_idx = 1

@11
D = A
@n_rects
M = D 		// @n_rects = 11


// rect1
	// start position
	@SCREEN		// @16384
	D = A
	@a_rect1
	M = D 		// @a_rect1 = 16384
	@1549		// 16 * ( 32 * 3 ) + 13
	D = A
	@a_rect1
	M = D + M 	// @a_rect1 += 1549

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
	@1550		// 16 * ( 32 * 3 ) + 14
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
	@2574		// 16 * ( 32 * 5 ) + 14
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
	@4110		// 16 * ( 32 * 8 ) + 14
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
	@1551		// 16 * ( 32 * 3 ) + 15
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
	@3088		// 16 * ( 32 * 6 ) + 16
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
	@3089		// 16 * ( 32 * 6 ) + 17
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
	@4113		// 16 * ( 32 * 8 ) + 17
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
	@5649		// 16 * ( 32 * 11 ) + 17
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
	@3090		// 16 * ( 32 * 6 ) + 18
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

	@addr
	A = M 		
	M = -1		// RAM[ @addr ] = -1

	@32
	D = A
	@addr
	M = D + M 	// @addr += 32

	@i
	M = M + 1 	// @i += 1

	@LOOP_rect
	0 ; JMP


(SETUP_rect1)

	@rect_idx
	M = M + 1

	@i
	M = 0

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
