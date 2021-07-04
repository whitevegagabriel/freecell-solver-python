from collections import deque

class GameConstants:
    solution = [
        [], # free cells
        [13, 13, 13, 13], # solution cells
        [[],
         [],
         [],
         [],
         [],
         [],
         [],
         [],] # columns
    ]
    solution_str = str(solution)

initial_game = [
    [], # free cells
    [13, 13, 13, 12], # solution cells
    [[],
     [],
     [],
     [],
     [],
     [],
     [],
     [[13, 3]]] # columns
]

#TODO: implement
def peek_top_stack_el(game, stack_num):
    top_stack_el = []
    return top_stack_el

#TODO: implement
def del_top_stack_el(game, stack_num):
    return game

#TODO: implement
def put_top_stack_el(game, stack_num, el):
    return game

#TODO: implement
def eligible_stacks(game, stack_num):
    stack_nums = []
    return stack_nums

#TODO: implement
def free_cell_available(game):
    available = False
    return available

#TODO: implement
def put_free_cell_el(game, el):
    return game

def add_card_to_stacks(game_base, stack_nums, card):
    games = []
    for stack_num in stack_nums:
        new_game = put_top_stack_el(game_base, stack_num, card)
        games.append(new_game)
    return games

#TODO: implement
def add_card_to_solution(game_base, card):
    games = []
    return games

#TODO: implement
def next_games_stacks(game):
    games = []
    for i in range(8):
        stack_nums = eligible_stacks(game, i)
        card_to_move = peek_top_stack_el(game, i)
        new_game_base = del_top_stack_el(game, i)
        games += add_card_to_stacks(new_game_base, stack_nums, card_to_move)
        games += add_card_to_solution(new_game_base, card_to_move)
        if free_cell_available(game):
            new_game = put_free_cell_el(new_game_base, card_to_move)
            games.append(new_game)
    return games

#TODO: implement
def next_games_cells(game):
    games = []
    return games

def next_games(game):
    games = []
    games += next_games_stacks(game)
    games += next_games_cells(game)
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
    return None

solution = find_solution_steps(initial_game)

for step in solution:
    print(step)