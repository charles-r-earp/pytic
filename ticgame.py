import sys, pygame
import numpy as np

class TicGame:
	
	def __init__(self, mode):
		self.mode = mode
	
	def update(self, board):
		if self.mode == 'text':
			pass
			#print(board)
	
	def play(self, players):
		assert len(players) > 0 and len(players) <= 2
		if len(players) == 1:
			players += players
		from ticboard import TicBoard
		board = TicBoard()
		playing = True
		self.update(board)
		result = 0
		while playing:
			i = board.active()
			col, row = players[i-1].move(board)
			assert board.legal(col, row)
			board = board.mark(col, row)
			self.update(board)
			if board.tie():
				if self.mode == 'text':
					print('Tie!')
				playing = False
				result = 0
			elif board.win(i):
				result = 1 if i == 1 else -1
				if self.mode == 'text':
					if i == 1:
						print('X wins!')
					else:
						print('O wins!')
				playing = False
		return result

class TicBoard2:
	
	def __init__(self, marks=np.zeros([3, 3, 2])):
		self.marks = marks
		self.playing = True
		self.winner = -1
		self.tie = False
		self.reset()
		
	def draw(self, surface):
		import pygame.gfxdraw
		white = 255, 255, 255
		surface.fill(white)
		# draw board lines
		black = 0, 0, 0
		w = 4
		x = self.rect.x + self.rect.width//3 - w//2
		y = self.rect.height
		pygame.draw.line(surface, black, (x, 0), (x, y), w)
		x = self.rect.x + 2*self.rect.width//3 - w//2
		pygame.draw.line(surface, black, (x, 0), (x, y), w)
		x = self.rect.width
		y = self.rect.height//3 - w//2
		pygame.draw.line(surface, black, (0, y), (x, y), w)
		y = 2*self.rect.height//3 - w//2
		pygame.draw.line(surface, black, (0, y), (x, y), w)
		# draw marks
		red = 255, 0, 0
		blue = 0, 0, 255
		inset = 12
		width = self.rect.width//3 - 2*inset
		height = self.rect.height//3 - 2*inset
		radius = min(width, height)//2
		w = 4
		for i in range(3):
			for u in range(3):
				x1 = i*self.rect.width//3 + inset
				x2 = x1 + width
				y1 = u*self.rect.width//3 + inset
				y2 = y1 + height
				if self.marks[i, u, 0]:
					pygame.gfxdraw.line(surface, x1, y1, x2, y2, blue)
					pygame.gfxdraw.line(surface, x1, y2, x2, y1, blue)
				if self.marks[i, u, 1]:
					x = (x1 + x2)//2
					y = (y1 + y2)//2
					pygame.gfxdraw.aacircle(surface, x, y, radius, red)
					
	def active_player_index(self):
		return np.count_nonzero(self.marks)%2
	
	def legal(self, col, row):
		i = self.active_player_index()
		return not (self.marks[col, row, 0] or self.marks[col, row, 1])
	
	def legal_moves(self):
		moves = []
		for i in range(3):
			for u in range(3):
				if(self.legal(i, u)):
					moves += [(i, u)]
		return moves
	
	def mark(self, col, row):
		if self.playing:
			i = self.active_player_index()
			if self.legal(col, row):
				self.marks[col, row, i] = 1
			else:
				moves = self.legal_moves()
				if len(moves):
					c = np.random.randint(0, len(moves))
					col, row = moves[c]
					self.marks[col, row, i] = 1
			if np.count_nonzero(self.marks) == 9:
				self.playing = False
				self.tie = True
			else:
				if np.count_nonzero(self.marks[col, :, i]) == 3:
					self.playing = False
					self.winner = i
				elif np.count_nonzero(self.marks[:, row, i]) == 3:
					self.playing = False
					self.winner = i
				elif np.count_nonzero([self.marks[0, 0, i], self.marks[1, 1, i], self.marks[2, 2, i]]) == 3:
					self.playing = False
					self.winner = i
				elif np.count_nonzero([self.marks[2, 0, i], self.marks[1, 1, i], self.marks[0, 2, i]]) == 3:
					self.playing = False
					self.winner = i
					
	def next_board(self, col, row):
		board = TicBoard(self.marks)
		board.mark(col, row)
		return board
	
	def reset(self):
		self.marks = np.zeros([3, 3, 2])
		self.playing = True
		self.winner = -1
		self.tie = False
	
	def mouse_click(self, pos):
		x, y = pos
		width = self.rect.width//3 
		height = self.rect.height//3
		col = x//width
		row = y//height
		self.mark(col, row)