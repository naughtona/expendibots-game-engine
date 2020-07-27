"""
	This program is written by and the property of
	Andrew Naughton of University of Melbourne, 
	with code attributions made where applicable.
	Last Modified: 27/07/2020
"""



from utils.game_rep import *




# returns the resulting board after a boom move at position i
def make_boom(i, board, visited):

    board = put(board, i, ' ')

    visited[i] = 1

    for j in list(map(lambda d: i + d, all_directions)):
        if (i % 8 == 0 and j % 8 == 7) or (i % 8 == 7 and j % 8 == 0) or ((j < 0) or (j > 63)):
            continue

        try: 
            if visited[j]: continue

        except KeyError:
            if not board[j].isspace():
                board = make_boom(j,board,visited)

    return board





# returns the resulting board after moving according to 'move'
def make_move(move, board):

    n, i, j = move

    p, q = board[i], board[j]

    try: 
        new_p = map_l_to_n[p] - n
        board = put(board, i, map_n_to_l[new_p])

    except: 
        board = put(board, i, ' ')

    if not q.isspace(): 
        new_q = n + map_l_to_n[q]
    else: 
        new_q = n

    board = put(board, j, map_n_to_l[new_q])

    return board




# takes a move (move or boom) and returns a formatted tuple that complies with referee
def format_move(move):

    if isinstance(move, tuple) and len(move) == 3:
        n, i, j = move

        return ('MOVE', n, map_i_to_c(i), map_i_to_c(j))

    elif isinstance(move, int):
        i = move

        return ('BOOM', map_i_to_c(i))





# takes a formatted tuple and converts it to suit my game representation
def parse_formatted_move(move):

    if move[0] == 'MOVE':
        n, c, d = move[1:]

        return (n,map_c_to_i(c),map_c_to_i(d))

    elif move[0] == 'BOOM':
        c = move[1]

        return map_c_to_i(c)






# takes a board and prints it in a pretty and readable way (for debugging purposes)
def pretty_print(board):

    indices = [i for i in range(0,64,8)]

    parts = [board[i:j] for i,j in zip(indices, indices[1:]+[None])]

    print('\n'.join(parts))






# f_is_upper is a bool that tells us if we are the uppercase team
# takes a board and returns a tuple with how many pieces each team have
def check_lives(board, f_is_upper):

    is_friendly = lambda p: p.isupper() if f_is_upper else p.islower()

    f_pieces = e_pieces = 0

    for match in re.findall(regex_any_case, board):
        if is_friendly(match): # friendly piece
            f_pieces += map_l_to_n[match.upper()]
        else: # enemy piece
            e_pieces += map_l_to_n[match.upper()]

    return (f_pieces, e_pieces)





# finds the set of white or black pieces belonging to a cluster, given a starting position i
# returns the set, along with a boolean for uppercase and lowercase
def find_cluster(i, board, visited, uppercase, lowercase):

    p = board[i]

    visited[i] = map_l_to_n[p.upper()]

    for j in list(map(lambda d: i + d, all_directions)):
        if (i % 8 == 0 and j % 8 == 7) or (i % 8 == 7 and j % 8 == 0) or ((j < 0) or (j > 63)):
            continue

        try: 
            if visited[j]: 
                continue
        except KeyError:
            q = board[j]
            if q.isupper():
                visited, uppercase, lowercase = find_cluster(j,board,visited,True,lowercase)
            if q.islower():
                visited, uppercase, lowercase = find_cluster(j,board,visited,uppercase,True)

    # for example, if uppercase and lowercase are both true, the cluster is mixed
    return visited, uppercase, lowercase






# returns minimum optimistic distance between an enemy-cluster and any member of friendly team
def min_manhatten(board, e_cluster,f_is_upper):

    regex = regex_uppercase if f_is_upper else regex_lowercase

    min_d = 13

    for i in e_cluster:
        e_x, e_y = map_i_to_c(i)

        for match in re.finditer(regex,board):
            index = match.start(0)

            p = board[index]
            n = map_l_to_n[p.upper()]

            f_x, f_y = map_i_to_c(index)

            d_x = max(abs(e_x - f_x) - 1, 0)
            d_y = max(abs(e_y - f_y) - 1, 0)
            d_x = (d_x//n) + min((d_x%n),1)
            d_y = (d_y//n) + min((d_y%n),1)

            min_d = min(d_x+d_y, min_d)
            
    return min_d







# returns a tuple containing:
# # of friendly clusters, # of friendlies safe, # enemies free, total min optmistic distance
def board_stats(board, f_is_upper):

    is_friendly = lambda upper,lower: upper and not lower if f_is_upper else lower and not upper
    is_enemy = lambda upper,lower: lower and not upper if f_is_upper else upper and not lower

    f_clusters = f_safe = e_free = dist = 0
    exploded = set()

    for i, p in enumerate(board):
        if p.isspace() or i in exploded: 
            continue

        uppercase = p.isupper()

        cluster_d, upper, lower = find_cluster(i,board,{},uppercase, not uppercase)

        cluster = set(cluster_d.keys())

        n = sum(cluster_d.values())

        exploded = exploded | cluster

        if is_friendly(upper,lower): # friendly cluster
            f_clusters += 1
            f_safe += n
        elif is_enemy(upper,lower): # enemy cluster
            e_free += n
            dist += min_manhatten(board, cluster,f_is_upper)
            
    return (f_clusters, f_safe, e_free, dist)