from collections import deque

class GameConstants:
    solution = [
        [None, None, None, None], # free cells
        [13, 13, 13, 13], # solution cells
        [[0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None],
        [0, None, None, None, None, None, None, None]] # columns
    ]

initial_game = [
    [None, None, None, None], # free cells
    [13, 13, 13, 12], # solution cells
    [[0, None, None, None, None, None, None, None],
     [0, None, None, None, None, None, None, None],
     [0, None, None, None, None, None, None, None],
     [0, None, None, None, None, None, None, None],
     [0, None, None, None, None, None, None, None],
     [0, None, None, None, None, None, None, None],
     [0, None, None, None, None, None, None, None],
     [1, [13, 3], None, None, None, None, None, None]] # columns
]

#TODO: implement
def next_games_stacks(game):
    games = []
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
    games_set = {initial_game}
    games_dict = {initial_game : None}
    games_queue = deque()
    games_queue.append(initial_game)

    # loops until no games in queue
    while games_queue:
        game_to_process = games_queue.popleft()
        possible_next_games = next_games(game_to_process)
        # appends games to queue, set, and dict if not aready there
        for game in possible_next_games:
            if game not in games_set:
                games_set.add(game)
                games_dict[game] = game_to_process
                games_queue.append(game)
                if game == GameConstants.solution:
                    return games_dict_as_list(games_dict)
    return None

solution = find_solution_steps(initial_game)
print(solution)