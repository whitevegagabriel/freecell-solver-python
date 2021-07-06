from collections import deque
from copy import copy, deepcopy
import datetime
import time

class GameConstants:
    solution = {
        'foundation' : [13, 13, 13, 13],
        'free' : set(),
        'cascades' : [[],
         [],
         [],
         [],
         [],
         [],
         [],
         []]
    }
    solution_str = str(solution)

initial_game = {
    'foundation' : [7, 6, 6, 5],
    'free' : {(12, 3), (13, 0), (12, 1), (13, 2)},
    'cascades' : [[(11, 2), (10, 1), (9, 2), (8, 3), (7, 2)],
                  [(6, 3)],
                  [(13, 1), (12, 0), (11, 3), (10, 0), (9, 1), (8, 0), (7, 1)],
                  [(11, 0)],
                  [(10, 3), (9, 0), (8, 1)],
                  [],
                  [(13, 3)],
                  [(12, 2), (11, 1), (10, 2), (9, 3), (8, 2), (7, 3)]]
}

def peek_top_cascade_el(game, cascade_num):
    cascade = game['cascades'][cascade_num]
    top_cascade_el = []
    if cascade:
        top_cascade_el = cascade[-1]
    return copy(top_cascade_el)

def del_top_cascade_el(game, cascade_num):
    game = deepcopy(game)
    if game['cascades'][cascade_num]:
        game['cascades'][cascade_num].pop()
    return game

def put_top_cascade_el(game, cascade_num, el):
    game = deepcopy(game)
    game['cascades'][cascade_num].append(el)
    return game

def eligible_cascades(game, card, source_stack_num=-1):
    cascade_nums = []
    is_last_card = len(game['cascades'][source_stack_num]) == 0
    eligible_range = (j for j in range(0, 8) if j != source_stack_num)
    empty_stack_added = False
    for i in eligible_range:
        top_card = peek_top_cascade_el(game, i)
        if card:
            if not top_card:
                if (not is_last_card or source_stack_num == -1) and not empty_stack_added:
                    cascade_nums.append(i)
                    empty_stack_added = True
            # check if new card is preceding rank and of opposite color suit
            elif (top_card[0] - 1 == card[0] and (top_card[1] + card[1]) % 2 != 0):
                cascade_nums.append(i)
            
    return cascade_nums

def free_cell_available(game):
    if len(game['free']) < 4:
        return True
    return False

def add_free_cell_el(game, el):
    game = deepcopy(game)
    el = copy(el)
    game['free'].add(el)
    return game

def add_card_to_cascades(game_base, cascade_nums, card):
    games = []
    for cascade_num in cascade_nums:
        new_game = put_top_cascade_el(game_base, cascade_num, card)
        games.append(new_game)
    return games

def add_card_to_foundation(game_base, card):
    games = []
    game_base = deepcopy(game_base)
    if card and game_base:
        if game_base['foundation'][card[1]] + 1 == card[0]:
            game_base['foundation'][card[1]] += 1
            games.append(game_base)
    return games

def is_smallest_card(game, card):
    smallest_card_rank = min(game['foundation']) + 1
    if card:
        return smallest_card_rank == card[0]
    return False

def next_games(game):
    games = []
    # find next games in cascades
    for i in range(8):
        card_to_move = peek_top_cascade_el(game, i)
        new_game_base = del_top_cascade_el(game, i)
        if not is_smallest_card(game, card_to_move):
            cascade_nums = eligible_cascades(new_game_base, card_to_move, i)
            games += add_card_to_cascades(new_game_base, cascade_nums, card_to_move)
            if card_to_move and free_cell_available(game):
                new_game = add_free_cell_el(new_game_base, card_to_move)
                games.append(new_game)
                games += add_card_to_foundation(new_game_base, card_to_move)
        else:
            # if card is smallest, only next move is in foundation
            return add_card_to_foundation(new_game_base, card_to_move)
    # find next games in free cells
    for card_to_move in game['free']:
        cascade_nums = eligible_cascades(game, card_to_move)
        new_game_base = deepcopy(game)
        new_game_base['free'].remove(card_to_move)
        if not is_smallest_card(game, card_to_move):
            games += add_card_to_cascades(new_game_base, cascade_nums, card_to_move)
            games += add_card_to_foundation(new_game_base, card_to_move)
        else:
            # if card is smallest, only next move is in foundation
            return add_card_to_foundation(new_game_base, card_to_move)
    return games

def games_dict_as_list(games_dict):
    parent = GameConstants.solution_str
    games_list = []
    while parent != None:
        games_list.append(parent)
        parent = games_dict[parent]
    games_list.reverse()
    return games_list

def find_solution_steps(initial_game):
    games_set = {str(initial_game)}
    games_dict = {str(initial_game) : None}
    games_queue = deque()
    games_queue.append(initial_game)

    i = 0
    start = time.time()
    total = 0
    # loops until no games in queue
    while games_queue:
        game_to_process = games_queue.popleft()
        possible_next_games = next_games(game_to_process)
        # appends games to queue, set, and dict if not aready there
        game_to_process_str = str(game_to_process)
        for game in possible_next_games:
            game_str = str(game)
            if game_str not in games_set:
                games_set.add(game_str)
                games_dict[game_str] = game_to_process_str
                games_queue.append(game)
                if game_str == GameConstants.solution_str:
                    return games_dict_as_list(games_dict)
        i += 1
        if i % 1000 == 0:
            elapsed = time.time() - start
            total += elapsed
            print(f"Elapsed: {elapsed:f}    Average Time / 1000 R: {total*1000/i:f}    Average Added / Round: {len(games_set)/i:f}")
            start = time.time()
    return ['No solution found']

print(datetime.datetime.now())
solution = find_solution_steps(initial_game)
print(datetime.datetime.now())

for step in solution:
    print(step)