from constants import * 
from square import Square 
from piece import *
from move import Move
import copy 

class Board:
	def __init__(self):
		self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
		self.last_move = None 
		self._create()
		self._add_pieces('white')
		self._add_pieces('black')

	def move(self, piece, move):
		initial = move.initial 
		final = move.final 
		# update the moves on the board
		self.squares[initial.row][initial.col].piece = None 
		self.squares[final.row][final.col].piece = piece 

		# pawn promotion 
		if isinstance(piece, Pawn):
			self.check_promotion(piece, final)

		# king castling 
		if isinstance(piece, King):
			if self.castling(initial, final):
				difference = final.col - initial.col 
				rook = piece.left_rook if (difference < 0) else piece.right_rook
				self.move(rook, rook.moves[-1])

		piece.move = True 
		# clear the valid moves after piece moved.
		piece.clear_moves()
		# set the last move 
		self.last_move = move

	def valid_move(self, piece, move):
		return move in piece.moves
	
	def check_promotion(self, piece, final):
		if final.row == 0 or final.row == 7:
			self.squares[final.row][final.col].piece = Queen(piece.color)	

	def castling(self, initial, final):
		return abs(initial.col - final.col) == 2

	def in_check(self, piece, move):
		temp_piece = copy.deepcopy(piece)
		temp_board = copy.deepcopy(self)
		temp_board.move(temp_piece, move)

		for row in range(ROWS):
			for col in range(COLS):
				if temp_board.squares[row][col].has_rival_piece(piece.color):
					p = temp_board.squares[row][col].piece
					temp_board.calc_moves(p, row , col, bool=False)

					for m in p.moves:
						if isinstance(m.final.piece, King):
							return True 
		return False

	## Calculate the possible moves of an specific piece.
	def calc_moves(self, piece, row, col, bool=True):

		def pawn_moves():
			steps = 1 if piece.moved else 2 

			## Vertical move
			start = row + piece.dir 
			end = row + (piece.dir * (1 + steps))
			for possible_move_row in range(start, end, piece.dir):
				if Square.in_range(possible_move_row):
					if self.squares[possible_move_row][col].is_empty():
						initial = Square(row, col)
						final = Square(possible_move_row, col) 
						move = Move(initial, final)

						if bool:
							if not self.in_check(piece, move):							
								piece.add_move(move)
						else:
							piece.add_move(move)
					else:
						break  # Pawn's blocked
				else:
					break  # Not in range ( not on the board. )

			## Diagnol move 
			possible_move_row = row + piece.dir 
			possible_move_cols = [col-1, col+1]
			for possible_move_col in possible_move_cols:
				if Square.in_range(possible_move_row, possible_move_col):
					if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
						initial = Square(row, col)
						final_piece = self.squares[possible_move_row][possible_move_col].piece
						final = Square(possible_move_row, possible_move_col, final_piece) 
						move = Move(initial, final)
						if bool:
							if not self.in_check(piece, move):							
								piece.add_move(move)
						else:
							piece.add_move(move)
					else:
						break  # Pawn's blocked


		def knight_moves():
			# For knights we have 8 possible moves.
			possible_moves = [
			(row-2, col+1),
            (row-1, col+2),
            (row+1, col+2),
            (row+2, col+1),
            (row+2, col-1),
            (row+1, col-2),
            (row-1, col-2),
            (row-2, col-1)
			]

			for possible_move in possible_moves:
				possible_move_row, possible_move_col = possible_move
	
				if Square.in_range(possible_move_row, possible_move_col):
					if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
						initial = Square(row, col)
						final_piece = self.squares[possible_move_row][possible_move_col].piece
						final = Square(possible_move_row, possible_move_col, final_piece)
						move = Move(initial, final)

						if bool:
							if not self.in_check(piece, move):							
								piece.add_move(move)
							else:
								break 
						else:
							piece.add_move(move)

		def straightline_moves(incrs):
			for incr in incrs:
				row_incr, col_incr = incr  
				possible_move_row = row + row_incr 
				possible_move_col = col + col_incr 

				while True:
					if Square.in_range(possible_move_row, possible_move_col):
						initial = Square(row, col)
						final_piece = self.squares[possible_move_row][possible_move_col].piece
						final = Square(possible_move_row, possible_move_col, final_piece)
						move = Move(initial, final)
	
						if self.squares[possible_move_row][possible_move_col].is_empty():
							if bool:
								if not self.in_check(piece, move):							
									piece.add_move(move)
							else:
								piece.add_move(move) 
	
						elif self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
							if bool:
								if not self.in_check(piece, move):							
									piece.add_move(move)
							else:
								piece.add_move(move)
							break 

						elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
							break

					else:
						break 

					# incrementing the increments(incrs).
					possible_move_row = possible_move_row + row_incr
					possible_move_col =  possible_move_col + col_incr

		def king_moves():
			adjacents = [
                (row-1, col+0),
                (row-1, col+1), 
                (row+0, col+1), 
                (row+1, col+1), 
                (row+1, col+0),
                (row+1, col-1), 
                (row+0, col-1), 
                (row-1, col-1)
            ]

			for possible_move in adjacents:
				possible_move_row, possible_move_col = possible_move

				if Square.in_range(possible_move_row, possible_move_col):
					if self.squares[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
						initial = Square(row, col)
						final = Square(possible_move_row, possible_move_col) 
						move = Move(initial, final)
						
						if bool:
							if not self.in_check(piece, move):							
								piece.add_move(move)
						else:
							piece.add_move(move)

			if not piece.moved:
				left_rook = self.squares[row][0].piece
				if isinstance(left_rook, Rook):
					if not left_rook.moved:
						for co in range(1, 4):
							if self.squares[row][co].has_piece():
								break
							if co == 3:
								piece.left_rook = left_rook
								# rook's move
								initial = Square(row, 0)
								final = Square(row, 3) 
								move = Move(initial, final)
								left_rook.add_move(move)

								initial = Square(row, col)
								final = Square(row, 2)
								move = Move(initial, final)
								left_rook.add_move(move)

				right_rook = self.squares[row][7].piece
				if isinstance(right_rook, Rook):
					if not right_rook.moved:
						for co in range(5, 7):
							if self.squares[row][co].has_piece():
								break
							if co == 6:
								piece.right_rook = right_rook
								# rook's move
								initial = Square(row, 7)
								final = Square(row, 5) 
								move = Move(initial, final)
								right_rook.add_move(move)

								initial = Square(row, col)
								final = Square(row, 6)
								move = Move(initial, final)
								right_rook.add_move(move)

				
		if isinstance(piece, Pawn):
			pawn_moves()

		elif isinstance(piece, Knight):
			knight_moves()

		elif isinstance(piece, Bishop):
			straightline_moves([
				(-1, 1),
				(-1, -1),
				(1, 1),
				(1, -1)
				])

		elif isinstance(piece, Rook):
			straightline_moves([
				(-1, 0),
                (0, 1), 
                (1, 0), 
                (0, -1) 
				])

		elif isinstance(piece, Queen):
			straightline_moves([
				(-1, 1), 
                (-1, -1),
                (1, 1),  
                (1, -1), 
                (-1, 0),
                (0, 1), 
                (1, 0), 
                (0, -1) 
				])

		elif isinstance(piece, King):
			king_moves()

	def _create(self):

		for row in range(ROWS):
			for col in range(COLS):
				self.squares[row][col] = Square(row, col)

	def _add_pieces(self, color):
		row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

		## Same as this
		#-------------------------------
		# if color == 'white':
		# 	row_pawn, row_other = (6, 7)
		# else:
		# 	row_pawn, row_other = (0, 1)
		#-------------------------------

		## All pawns
		for col in range(COLS):
			self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

		## Knights
		self.squares[row_other][1] = Square(row_other, 1, Knight(color))
		self.squares[row_other][6] = Square(row_other, 6, Knight(color))

		## Bishops
		self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
		self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

		## Rooks
		self.squares[row_other][0] = Square(row_other, 0, Rook(color))
		self.squares[row_other][7] = Square(row_other, 7, Rook(color))

		## Queen
		self.squares[row_other][3] = Square(row_other, 3, Queen(color))

		## King
		self.squares[row_other][4] = Square(row_other, 4, King(color))