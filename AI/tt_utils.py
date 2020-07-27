"""
	This program is written by and the property of
	Andrew Naughton of University of Melbourne, 
	with code attributions made where applicable.
	Last Modified: 27/07/2020
"""



import typing
from collections import OrderedDict



from utils.position import *




# much of this class has been lifted from: https://github.com/VCHui/angelfish/blob/master/engines.py
# least recently used algorithm that helps cache items for transposition table
class LRUCache:

	'''Store items in the order the keys were last added'''

	def __init__(self, size):
		self.od = OrderedDict()

		self.size = size

	def get(self, key, default=None):
		try: self.od.move_to_end(key)

		except KeyError: return default

		return self.od[key]

	def __setitem__(self, key, value):
		try: del self.od[key]

		except KeyError:
			if len(self.od) == self.size:
				self.od.popitem(last=False)

		self.od[key] = value





# much of this class has been lifted from: https://github.com/VCHui/angelfish/blob/master/engines.py
# this is a transposition table entry
# 'Entry' is the key, representing a state
# 'depth', 'score', 'move', 'bound' are critical details concerning the state 
class Entry(typing.NamedTuple):

	"""
	depth   --  int
	score   --  score associated with board
	move    --  new Position
	bound   --  either -1 (fail high), 0 (is exact value), 1 (fail low)
	"""

	depth: int
	score: float
	move: Position
	bound: int
	

	BOUND_LOWER,BOUND_EXACT,BOUND_UPPER = 1,0,-1

	# relates to whether we failed high or low
	def narrowing(self,alpha,beta):
		# fail high result implies a lowerbound
		if self.bound == self.BOUND_LOWER: # was entry.score >= beta
			alpha = max(alpha,self.score)

		# fail low implies an upperbound
		elif self.bound == self.BOUND_UPPER: # was entry.score <= alpha
			beta = min(beta,self.score)

		return alpha,beta




	# Found an accurate minimax value - but will not occur with zero-window searches like ours
	def isexact(self):
		return self.bound == self.BOUND_EXACT
