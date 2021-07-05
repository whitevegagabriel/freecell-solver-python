from collections import deque
from copy import copy, deepcopy

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
    'foundation' : [13, 13, 13, 12],
    'free' : set(),
    'cascades' : [[],
        [],
        [],
        [],
        [],
        [],
        [],
        [(13, 3)]]
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

def eligible_cascades(game, card):
    cascade_nums = []
    for i in range(8):
        top_card = peek_top_cascade_el(game, i)
        if top_card and card:
            # check if new card is preceding rank and of opposite color suit
            if top_card[0] - 1 == card[0] and (top_card[1] + card[1]) % 2 != 0:
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
        if game_base['foundation'][card[1]] + 1 == card[1]:
            game_base['foundation'][card[1]] += 1
            games.append(game_base)
    return games

def next_games_cascades(game):
    games = []
    for i in range(8):
        card_to_move = peek_top_cascade_el(game, i)
        cascade_nums = eligible_cascades(game, card_to_move)
        new_game_base = del_top_cascade_el(game, i)
        games += add_card_to_cascades(new_game_base, cascade_nums, card_to_move)
        games += add_card_to_foundation(new_game_base, card_to_move)
        if card_to_move and free_cell_available(game):
            new_game = add_free_cell_el(new_game_base, card_to_move)
            games.append(new_game)
    return games

def next_games_free(game):
    games = []
    for card_to_move in game['free']:
        cascade_nums = eligible_cascades(game, card_to_move)
        new_game_base = deepcopy(game)['free'].remove(card_to_move)
        games += add_card_to_cascades(new_game_base, cascade_nums, card_to_move)
        games += add_card_to_foundation(new_game_base, card_to_move)
    return games

def next_games(game):
    games = []
    games += next_games_cascades(game)
    games += next_games_free(game)
    return games

#TODO: implement
def games_dict_as_list(games_dict):
    games_list = []
    return games_list

def find_solution_steps(initial_game):
    games_set = {str(initial_game)}
    games_dict = {str(initial_game) : None}
    games_queue = deque()
    games_queue.append(initial_game)

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
    return []

solution = find_solution_steps(initial_game)

for step in solution:
    print(step)