import numpy as np

class TicBoard:
	
	def __init__(self, marks=None):
		if marks is None:
			marks = np.zeros([3, 3, 3])
			marks[:, :, 0] = 1
		self.marks = np.array(marks)
		
	def __str__(self):
		s = ''
		for col in range(3):
			for row in range(3):
				if self.marks[col, row, 0]:
					s += '_'
				elif self.marks[col, row, 1]:
					s += 'X'
				elif self.marks[col, row, 2]:
					s += 'O'
		return s
		
	def tie(self):
		return not len(self.legal_moves())
	
	def win(self, i):
		for u in range(3):
			if self.marks[u, :, i].all():
				return True
			elif self.marks[:, u, i].all():
				return True
		u = list(range(3))
		v = list(2-w for w in u)
		if self.marks[u, v, i].all():
			return True
		elif self.marks[v, u, i].all():
			return True
		return False
					
	def active(self):
		return 2 - np.count_nonzero(self.marks[:, :, 0])%2
	
	def legal(self, col, row):
		return self.marks[col, row, 0]
	
	def legal_moves(self):
		moves = []
		for i in range(3):
			for u in range(3):
				if(self.legal(i, u)):
					moves += [(i, u)]
		return moves
	
	def mark(self, col, row):
		assert self.legal(col, row)
		board = TicBoard(self.marks)
		i = self.active()
		board.marks[col, row, 0] = 0
		board.marks[col, row, i] = 1
		return board
					
	