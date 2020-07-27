"""
	This program is written by and the property of
	Andrew Naughton of University of Melbourne, 
	with code attributions made where applicable.
	Last Modified: 27/07/2020
"""



import typing


from utils.game_rep import *
from utils.helpers import *




# snippets of this class have been lifted from: https://github.com/VCHui/angelfish/blob/master/engines.py
# contains methods relevant for the maintenance and operations of board positions
class Position(typing.NamedTuple):

	""" A state of an expendibots game
	board			--	a 120 char representation of the board
	score			-- 	score associated with board
	white_to_move 	-- 	True if white to move otherwise False -- alternating between positions
	my_colour		-- 	True if my colour is 'white' otherwise False -- static between positions
	"""
	
	board: str
	score: float
	white_to_move: bool
	my_colour: bool


	# generator function that yields possible actions from a board
	def gen_moves(self):

		for i, p in enumerate(self.board):
			if not p.isupper(): continue

			yield (i) # boom action!

			# stack size n
			n = map_l_to_n[p]

			for d in cardinal_directions:
				for j in list(map(lambda x: i + d*x, mobility[p])):
					# stay inside the board, and off enemy pieces
					if (j < 0) or (j > 63): break

					if ((d in [E,W]) and ((i//8) != (j//8))): continue

					if self.board[j].islower(): continue

					# model a move of stack size m
					for m in range(n):
						yield (m+1, i, j) # move action!





	# rotates the board by swapping the letter cases of board pieces
	def rotate(self):

		return Position(self.board.swapcase(),self.score, self.white_to_move, self.my_colour)






	# moves a piece allowing easy transitions between Positions
	# returns a new Position based on move
	def move(self, move):

		board = self.board

		if isinstance(move, tuple) and len(move) == 3: # Move action
			board = make_move(move,board)
		elif isinstance(move, int): # Boom action
			board = make_boom(move,board,{})

		# calculate score for new position
		score = self.eval_fn(board)

		# we rotate the returned position, so it's ready for the next player
		return Position(board,score,not self.white_to_move,self.my_colour).rotate()
	





	# returns a value suggesting how 'good' a board state is
	# always from the friendly team's perspective
	def eval_fn(self, board):

		# f_is_upper is a bool that tells us if we (friendly) are uppercase
		f_is_upper = self.white_to_move == self.my_colour

		f_pieces, e_pieces = check_lives(board, f_is_upper)
		
		# utility
		if f_pieces and not e_pieces:
			return 10000
		elif e_pieces and not f_pieces:
			return -10000
		elif not f_pieces and not e_pieces:
			return 0

		# interesting board statistics for evaluation
		f_clusters, f_safe, e_free, dist = board_stats(board, f_is_upper)
		f_at_risk = (f_pieces - f_safe) / f_pieces
		e_at_risk = (e_pieces - e_free) / e_pieces
		at_risk = f_at_risk - e_at_risk

		# coefficients
		C1, C2, C3, C4, C5, C6 = 10, 10, 20, 1, 1, 1

		if f_safe > 1 and e_free == 1: # nearly end game
			# tweak select coefficients to ensure we finish the game asap
			C1, C2, C4 = 20, 20, 0

		if f_safe > 0 and e_free == 0: # end game
			# finish the game - no extra points for having more than one friendly left
			return 100*(12 - e_pieces)

		score = C1*f_pieces - C2*e_pieces - C3*at_risk + C4*f_clusters - C5*e_free - C6*dist

		return score
	
    




	# return True if we are at terminal state
	def gameover(self):
		return not re.search(regex_gameover,self.board)
	




	# call pretty_print method
	def print(self):
		pretty_print(self.board)
	




	# returns True if position i is vacant
	def is_vacant(self,i):
		return self.board[i].isspace()




	# returns True if position i is open to the uppercase team (team to move)
	def is_open(self,i):
		return self.board[i].isspace() or self.board[i].isupper()
	



	# return True if moving n tokens from position i is possible
	def is_possible(self, n, i):
		return self.board[i].isupper() and n <= map_l_to_n[self.board[i]]