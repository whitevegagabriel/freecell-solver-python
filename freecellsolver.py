from collections import deque

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
        [[13, 3]]]
}

#TODO: implement
def peek_top_cascade_el(game, cascade_num):
    top_cascade_el = []
    return top_cascade_el

#TODO: implement
def del_top_cascade_el(game, cascade_num):
    return game

#TODO: implement
def put_top_cascade_el(game, cascade_num, el):
    return game

#TODO: implement
def eligible_cascades(game, card):
    cascade_nums = []
    return cascade_nums

#TODO: implement
def free_cell_available(game):
    available = False
    return available

#TODO: implement
def put_free_cell_el(game, el):
    return game

def add_card_to_cascades(game_base, cascade_nums, card):
    games = []
    for cascade_num in cascade_nums:
        new_game = put_top_cascade_el(game_base.copy(), cascade_num, card.copy())
        games.append(new_game)
    return games

def add_card_to_foundation(game_base, card):
    games = []
    game_base = game_base.copy()
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
        if free_cell_available(game):
            new_game = put_free_cell_el(new_game_base, card_to_move)
            games.append(new_game)
    return games

def next_games_free(game):
    games = []
    for card_to_move in game['free']:
        cascade_nums = eligible_cascades(game, card_to_move)
        new_game_base = game.copy()['free'].remove(card_to_move)
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