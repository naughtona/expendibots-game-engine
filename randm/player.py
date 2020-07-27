"""
	This program is written by and the property of
	Andrew Naughton of University of Melbourne, 
	with code attributions made where applicable.
	Last Modified: 27/07/2020
"""



import random



from utils.game_rep import initial
from utils.helpers import format_move, parse_formatted_move
from utils.position import Position



class ExamplePlayer():

	def __init__(self, colour):

		self.pos = Position(initial, 0, True, colour == colour)

		response = input("Would you like to set a seed (for deterministic behaviour)? [yes/no]: ")

		if response == "yes":
			seed = int(input("Please enter a seed of your choice: "))
		else:
			seed = None
		
		random.seed(a=seed)

	


	def action(self):
		
		available_actions = []

		for move in self.pos.gen_moves():
			available_actions.append(move)
		
		move_to_take = available_actions[random.randint(0, len(available_actions) - 1)]

		return format_move(move_to_take)


	
	
	# update method to keep internal representation of the state-of-play current
	def update(self, colour, action):

		# interpret and decode formatted 'action'
		move = parse_formatted_move(action)

		self.pos = self.pos.move(move) # update!