import pygame 
from constants import *
from board import Board
from square import *
from dragger import Dragger
from config import Config 

class Game:

	def __init__(self):
		self.next_player = 'white'
		self.hovered_square = None
		self.config = Config()
		self.board = Board()
		self.dragger = Dragger()

	def show_bg(self, surface):
		for row in range(ROWS):
			for col in range(COLS):
				if (row + col) % 2 == 0:
					color = (234, 235, 200) # light color
				else:
					color = (119, 154, 88) # green color 

				rectangle = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
				pygame.draw.rect(surface, color, rectangle)


	def show_pieces(self, surface):
		for row in range(ROWS):
			for col in range(COLS):
				if self.board.squares[row][col].has_piece():
					piece = self.board.squares[row][col].piece

					if piece is not self.dragger.piece:
						piece.set_texture(size=80)
						img = pygame.image.load(piece.texture)
						img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
						piece.texture_rect = img.get_rect(center=img_center)
						surface.blit(img, piece.texture_rect)

	def show_moves(self, surface):
		if self.dragger.dragging:
			piece = self.dragger.piece 

			for move in piece.moves:
				# showing the possible moves by red color.
				color = "#C86464" if (move.final.row + move.final.col) % 2 == 0 else "#C84646"
				# specify the possible moves
				rectangle = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
				# draw the possible moves
				pygame.draw.rect(surface, color, rectangle)

	def show_last_move(self, surface):
		if self.board.last_move:
			initial = self.board.last_move.initial 
			final = self.board.last_move.final 
			for pos in [initial, final]:
				# showing the last move by yellow color.
				color = (244, 247, 117) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
				# specify the last move
				rectangle = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
				# draw the last move
				pygame.draw.rect(surface, color, rectangle)

	def show_hover(self, surface):
		if self.hovered_square:
			# showing the last move by yellow color.
			color = (180, 180, 180)
			# specify the last move
			rectangle = (self.hovered_square.col * SQSIZE, self.hovered_square.row * SQSIZE, SQSIZE, SQSIZE)
			# draw the last move
			pygame.draw.rect(surface, color, rectangle, width=4)

	def next_turn(self):
		self.next_player = 'white' if self.next_player == 'black' else 'black'

	def set_hover(self, row, col):
		self.hovered_square = self.board.squares[row][col]

	def play_sound(self, captured=False):
		if captured:
			self.config.capture_sound.play()
		else:
			self.config.move_sound.play()
	def reset(self):
		self.__init__()

