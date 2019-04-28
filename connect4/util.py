def checkforwinner(game_field):
    for x in range(0, 4):

        #horizontal
        for y in range(0, 6):
            if game_field[x][y] is not False and game_field[x][y] == game_field[x+1][y] and game_field[x][y] == \
                    game_field[x+2][y] and game_field[x][y] == game_field[x+3][y]:
                return game_field[x][y]
        # \
        for y in range(3, 6):
            if game_field[x][y] is not False and game_field[x][y] == game_field[x+1][y-1] and game_field[x][y] == \
                    game_field[x+2][y-2] and game_field[x][y] == game_field[x+3][y-3]:
                return game_field[x][y]
        # /
        for y in range(0, 3):
            if game_field[x][y] is not False and game_field[x][y] == game_field[x+1][y+1] and game_field[x][y] == \
                    game_field[x+2][y+2] and game_field[x][y] == game_field[x+3][y+3]:
                return game_field[x][y]

        # vertical
    for x in range(0, 7):
        for y in range(0, 3):
            if game_field[x][y] is not False and game_field[x][y] == game_field[x][y+1] and game_field[x][y] == \
                    game_field[x][y+2] and game_field[x][y] == game_field[x][y+3]:
                return game_field[x][y]

    return False


def checkfortie(game_state):
    for index in [item for sublist in game_state for item in sublist]:
        if not index:
            return False

    return True


def groundmove(move, game_state):
    x = move['x']
    y = move['y']
    for i in range(0, y):
        if game_state[x][i] is False:
            return {'x': x, 'y': i}
    return move


def estimatetime(episodes, q_values):
    from game import Game
    from ai_input import AIPlayer
    from user_input import HumanPlayer
    import time
    import datetime

    test_game = Game(AIPlayer("x"), AIPlayer("o"), q_values)
    start_time = time.time()
    for _ in range(100):
        test_game.play()
    end_time = time.time()
    time_in_sec = end_time-start_time
    time_for_episodes = time_in_sec/100*episodes
    formated_time = str(datetime.timedelta(seconds=time_for_episodes))
    print("Estimmated time: "+formated_time)
    while True:
        confirm = input("Do you want to continue? [y/n]").lower()
        if confirm == "y" or confirm == "yes" or confirm == "y" or confirm == "ja":
            return True
        if confirm == "n" or confirm == "no" or confirm == "nein":
            return False
