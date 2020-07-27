"""
	COMP30024 Artificial Intelligence
	Project Part B: Playing the Game
	This program is written by and the property of
	Andrew Naughton of University of Melbourne, 
	with code attributions made where applicable.
	Last Modified: 27/07/2020
"""



import numpy as np
import time
from collections import OrderedDict



from utils.position import *
from utils.helpers import *
from utils.game_rep import *



from AI.tt_utils import *





# snippets of this class have been lifted from: https://github.com/VCHui/angelfish/blob/master/engines.py
# main Class that drives our game playing program called anonymous
class ExamplePlayer:

	def __init__(self, colour):

		self.pos = Position(initial,0,True,colour==colour)

		# configurable settings
		self.max_depth = 15
		self.secs = 0.5
		self.turns = 0

		# hardcoding of opening four moves
		self.opening_moves = [(1,60,52),(2,52,36),(2,36,20),(1,20,22)] if colour == 'white' \
			else [(1,4,12),(2,12,28),(2,28,44),(1,44,46)]
		
		# corners are important for trapping opponent early in game
		self.corner = [6,7,14,15] if colour == 'white' else [54,55,62,63]

		# bool to check if opening moves sequence still applicable (in tact)
		self.opening_in_tact = True
	




	# move ordering method to sort next moves by evaluation scores
	# generator method
	def sorted_gen_moves(self, pos):

		scoremoves = sorted(((pos.move(move).score, move) for move in pos.gen_moves()),key=lambda x: x[0])

		return (move for score, move in scoremoves)




	# alpha beta search in negamax framework
	def alphabeta(self, pos, depth, alpha, beta, ply):

		self.nodes += 1
		alpha_o = alpha

		entry = self.tt.get(pos) # default=None

		if entry is not None and entry.depth >= depth: # oh great time-savings from the tt!
			self.hits += 1
			alpha, beta = entry.narrowing(alpha,beta) # let's narrow our window accordingly!
			# note - entry.isexact() will never be True with MTD-f zero window searches
			# ...nevertheless retained for posterity
			if alpha >= beta or entry.isexact():
				return entry.score

		if pos.gameover() or depth <= 0: # return +ve or -ve score according to ply
			# negamax
			return -pos.score if ply%2 else pos.score

		bestmove, maxscore = None, -np.inf

		moves = (self.sorted_gen_moves(pos)) # next moves sorted by evaluation score
		for move in moves:
			nextpos = pos.move(move) # simulate board position if we take this move
			score = -self.alphabeta(nextpos, depth-1, -beta, -alpha,ply+1)

			if score >= maxscore:
				bestmove, maxscore = move, score

			alpha = max(alpha, score)

			if alpha >= beta: break # can prune!

		# update/create transposition table details (value) pertaining to this state (key)		
		self.tt[pos] = Entry(	
			depth, maxscore,bestmove, 
			(maxscore >= beta)-(maxscore <= alpha_o))

		return maxscore
	





	# this method has partly been lifted from: https://people.csail.mit.edu/plaat/mtdf.html
	# mtd-f takes a first guess f and a depth d and, by calling numerous zero window searches to...
	# ...alpha beta, it converges on the minimax value
	def mtdf(self, f, d):

		g = f
		upperbound = np.inf
		lowerbound = -np.inf

		while lowerbound < upperbound:
			if g == lowerbound:
				beta = g + 1
			else:
				beta = g
			g = self.alphabeta(self.pos, d, beta - 1, beta, 0) # ply starts at 0
			if g < beta:
				upperbound = g
			else: lowerbound = g

		return g






	# gets called when we are required to act
	# returns a well-formatted tuple representing our desired move
	def action(self): 

		""" alphabeta pruning with negamax, featuring:
		* mtd-f algorithm(zero-window search);
		* move ordering;
		* iterative deepening framework;
		* transposition table; and
		* an opening four-move strategy
		"""

		timestart= time.time()
		self.turns += 1
		self.nodes = 0

		# opening strategy
		if self.turns in [1,2,3,4] and self.opening_in_tact:
			move_to_take = self.opening_strategy()
			if move_to_take is not None: return move_to_take
			else: self.opening_in_tact = False


		# iterative deepening
		first_guess = 0 # standard very first guess
		for depth in range(1, self.max_depth):
			self.tt, self.hits = LRUCache(TABLE_SIZE), 0 # transposition table
			
			# first guess is the previous iteration's best score (a good estimate of true bound)
			first_guess = self.mtdf(first_guess, depth)

			# get best move sequence relating to alpha beta's best score
			pv = self.getpv(self.pos)

			timespent = time.time() - timestart
			
			# are we out of time or does the best move sequence end with a terminal state?
			if (timespent > self.secs) or (pv[-1] is None):
				break
			
		# format move for referee	
		move_to_take = format_move(pv[0])

		return move_to_take






	# pv-moves -- helps to cut-off search if best move sequence ends with game-over
	def getpv(self, pos):

		pv = OrderedDict()

		while True:
			if pos.gameover():
				pv[pos] = None
				break

			entry = self.tt.get(pos)

			if entry is None:
				break

			if entry.move is None:
				break

			if pos in pv:
				return list(pv.values()) + [entry.move,]

			pv[pos] = entry.move
			pos = pos.move(entry.move)

		return list(pv.values())
	




	# hardcoded opening strategy based on experience -- time-saver
	def opening_strategy(self):

		if self.turns < 4: # first three moves
			move_to_take = self.opening_moves[self.turns-1]

			if self.pos.is_open(move_to_take[2]) and self.pos.is_possible(*move_to_take[0:2]):
				# great - let's do it!
				return format_move(move_to_take) # format the move

			return None
		
		else: # fourth and final hardcoded move
			count = 0

			for square in self.corner: # check corner to see if there is much to trap
				if self.pos.is_vacant(square):
					count += 1
					# less than 3 occupied enemy squares in the corner signals 'don't bother'
					if count > 1: return None

			move_to_take = self.opening_moves[self.turns-1]

			if self.pos.is_open(move_to_take[2]) and self.pos.is_possible(*move_to_take[0:2]):
				# great - let's do it!
				return format_move(move_to_take) # format the move

			return None





	# update method to keep internal representation of the state-of-play current
	def update(self, colour, action):

		# interpret and decode formatted 'action'
		move = parse_formatted_move(action)

		self.pos = self.pos.move(move) # update!
