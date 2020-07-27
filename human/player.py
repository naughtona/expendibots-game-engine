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

	



	def action(self):

		print("\n" + "The following actions are available:" + "\n")
		
		available_actions = []

		for i, move in enumerate(self.pos.gen_moves()):
			formatted_move = format_move(move)

			if i > 0 and i % 3 == 0:
				print()

			print("{:3d}: {:32s}".format(i + 1, format(formatted_move)), end='')

			available_actions.append(formatted_move)
		
		print("\n")

		move_index = int(input("Please choose an action to take (enter the index): "))

		return available_actions[move_index - 1]


	

	
	# update method to keep internal representation of the state-of-play current
	def update(self, colour, action):

		# interpret and decode formatted 'action'
		move = parse_formatted_move(action)

		self.pos = self.pos.move(move) # update!