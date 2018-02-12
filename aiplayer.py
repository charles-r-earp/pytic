import sys
import numpy as np
import torch
from torch.autograd import Variable

class AIPlayer():
	
	def __init__(self, load=True):
		from perfectplayer import PerfectPlayer
		self.perfect = PerfectPlayer()
		self.fname = 'aiplayer.pth'
		if load:
			try:
				self.model = torch.load(self.fname)
				loaded = True
			except:
				loaded = False
		else:
			loaded = False
		if loaded:
			print('AIPlayer: loaded model.')
		else:
			self.model = torch.nn.Sequential(
				torch.nn.Linear(27, 36),
				torch.nn.Tanh(),
				torch.nn.Linear(36, 36),
				torch.nn.Tanh(),
				torch.nn.Linear(36, 1),
				torch.nn.Tanh()
			)
		
	def train(self):
		boards = [board for key, (board, value) in self.perfect.state_values.items()]
		values = [value for key, (board, value) in self.perfect.state_values.items()]
		states = [torch.from_numpy(b.marks.flatten()).type(torch.FloatTensor).view(1, 27) for b in boards]
		states = torch.cat(states)
		values = [torch.FloatTensor([[v]]) for v in values]
		values = torch.cat(values)
		import torch.optim as optim
		import torch.nn.functional as F
		optimizer = optim.RMSprop(self.model.parameters())
		truth = Variable(values, requires_grad=False)
		epoch = 1
		while True:
			pred = self.model(Variable(states))
			# Compute Huber loss
			loss = F.smooth_l1_loss(pred, truth)
			# Optimize the model
			optimizer.zero_grad()
			loss.backward()
			for param in self.model.parameters():
				param.grad.data.clamp_(-1, 1)
			optimizer.step()
			if not epoch % 100:
				info = 'epoch: {} loss: {:.5f}'.format(epoch, float(loss[0]))
				print(info, end='\r', flush=True)
				torch.save(self.model, self.fname)
			epoch += 1
		
	def evaluate(self, board):
		state = torch.from_numpy(board.marks.flatten()).type(torch.FloatTensor).view(1, 27)
		state = Variable(state, requires_grad=False)
		value = self.model(state)
		return float(value[0])
	
	def move(self, board):
		moves = board.legal_moves()
		np.random.shuffle(moves)
		q = []
		for col, row in moves:
			next_board = board.mark(col, row)
			q += [self.evaluate(next_board)]
		u = np.argmax(q) if board.active() == 1 else np.argmin(q)
		return moves[u]
		
def main(argv):
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-train', default=False)
	ns = parser.parse_args(argv[1:])
	if ns.train:
		AIPlayer().train()
	else:
		from ticgame import TicGame
		while True:
			ai_wins = 0
			ties = 0
			perfect_wins = 0
			ai = AIPlayer(load=True)
			from perfectplayer import PerfectPlayer
			perfect = PerfectPlayer()
			for _ in range(500):
				result = TicGame(mode='quiet').play([ai, perfect])
				if result == 0:
					ties += 1
				elif result == 1:
					ai_wins += 1
				else:
					perfect_wins += 1
				result = TicGame(mode='quiet').play([perfect, ai])
				if result == 0:
					ties += 1
				elif result == 1:
					perfect_wins += 1
				else:
					air_wins += 1
				total = ai_wins + ties + perfect_wins
				info = 'ai: {:.0f}% tie: {:.0f}% perfect: {:.0f}% out of {} games.'
				info = info.format(ai_wins/total*100, ties/total*100, perfect_wins/total*100, total)
				print(info, end='\r', flush=True)
			print(info)
				
		
if __name__ == '__main__':
	main(sys.argv)