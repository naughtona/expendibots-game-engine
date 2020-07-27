"""
	This program is written by and the property of
	Andrew Naughton of University of Melbourne, 
	with code attributions made where applicable.
	Last Modified: 27/07/2020
"""



import re




# board/state representation
# team to move is always the uppercase team (rotates)
# white is always first team to move (per game rules)
initial = (
	'aa aa aa'  #  0  - 7
	'aa aa aa'  #  8  - 15
	'        '  #  16 - 23
	'        '  #  24 - 31
	'        '  #  32 - 39
	'        '  #  40 - 47
	'AA AA AA'  #  48 - 55
	'AA AA AA'  #  56 - 63
)




# directional mapping
NW, N, NE, W, E, SW, S, SE = -9, -8, -7, -1, 1, 7, 8, 9

cardinal_directions = (N, W, E, S)

all_directions = (NW, N, NE, W, E, SW, S, SE)




# A/a == stack size of 1
# ...
# L/l == stack size of 12
mobility = {
	'A': [i for i in range(1,2)],
	'B': [i for i in range(1,3)],
	'C': [i for i in range(1,4)],
	'D': [i for i in range(1,5)],
	'E': [i for i in range(1,6)],
	'F': [i for i in range(1,7)],
	'G': [i for i in range(1,8)],
	'H': [i for i in range(1,9)],
	'I': [i for i in range(1,10)],
	'J': [i for i in range(1,11)],
	'K': [i for i in range(1,12)],
	'L': [i for i in range(1,13)]
}




# mapping stack size number n to letter l
map_n_to_l = {
	1:  'A',
	2:  'B',
	3:  'C',
	4:  'D',
	5:  'E',
	6:  'F',
	7:  'G',
	8:  'H',
	9:  'I',
	10: 'J',
	11: 'K',
	12: 'L'
}




# mapping letter l to stack size number n
map_l_to_n = {
	'A': 1,
	'B': 2,
	'C': 3,
	'D': 4,
	'E': 5,
	'F': 6,
	'G': 7,
	'H': 8,
	'I': 9,
	'J': 10,
	'K': 11,
	'L': 12
}




# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e7



# regex
regex_gameover = re.compile(r'([A-L].*[a-l])|([a-l].*[A-L])')
regex_any_case = re.compile(r'[A-L]|[a-l]')
regex_uppercase = re.compile(r'[A-L]')
regex_lowercase = re.compile(r'[a-l]')




# put new piece on board
put = lambda board, i, p: board[:i] + p + board[i+1:]




# map index/coordinate to coordinate/index
map_c_to_i = lambda c: c[0] + (7-c[1])*8
map_i_to_c = lambda i: (i%8,7-(i//8))