import numpy as np

class PerfectPlayer():
	
	def __init__(self):
		self.gamma = 0.9
		self.state_values = {}
		if not len(self.state_values):
			self.state_values = {}
			from ticboard import TicBoard
			board = TicBoard()
			self.evaluate(board)
		print('PerfectPlayer: {} states.'.format(len(self.state_values)))
		
	def move(self, board):
		q = []
		moves = board.legal_moves()
		np.random.shuffle(moves)
		for col, row in moves:
			next_board = board.mark(col, row)
			b, v = self.state_values[str(next_board)]
			q += [v]
		u = np.argmax(q) if board.active() == 1 else np.argmin(q)
		return moves[u]
		
	def evaluate(self, board):
		key = str(board)
		if key in self.state_values:
			board, value = self.state_values[key]
			return value
		i = board.active()
		value = None
		for col, row in board.legal_moves():
			next_board = board.mark(col, row)
			if next_board.tie():
				value = 0
				self.state_values[str(next_board)] = (next_board, value)
			elif next_board.win(i):
				value = 1 if i==1 else -1
				self.state_values[str(next_board)] = (next_board, value)
			elif i==1:
				v = self.evaluate(next_board)
				if value is None:
					value = v
				else:
					value = max(v, value)
			else:
				v = self.evaluate(next_board)
				if value is None:
					value = v
				else:
					value = min(v, value)
		self.state_values[key] = (board, value)
		return value * self.gamma

def main():
	perfect = PerfectPlayer()
	from ticgame import TicGame
	while True:
		TicGame().play([perfect])
	
if __name__ == '__main__':
	main()