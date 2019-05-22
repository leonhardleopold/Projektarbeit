import pickle
import json

def checkforwinner(game_field, move=None, sign=None):
    if sum(item is not False for item in [item for sublist in game_field for item in sublist]) < 7:
        return False

    if move is None:
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
    else:
		# only check if the move results in a win 
        x = move['x']
        y = move['y']
        streaks = dict()
        streaks['horizontal_left'] = [0, True]
        streaks['horizontal_right'] = [0, True]
        streaks['vertical_left'] = [0, True]
        streaks['vertical_right'] = [0, True]
        streaks['dia_rising_left'] = [0, True]
        streaks['dia_rising_right'] = [0, True]
        streaks['dia_falling_left'] = [0, True]
        streaks['dia_falling_right'] = [0, True]

        for i in range(1,4):
            if x+i <= 6:
                if sign == game_field[x + i][y] and streaks['horizontal_left'][1]:
                    streaks['horizontal_left'][0] += 1
                else:
                    streaks['horizontal_left'][1] = False
            if x-i >= 0:
                if sign == game_field[x - i][y] and streaks['horizontal_right'][1]:
                    streaks['horizontal_right'][0] += 1
                else:
                    streaks['horizontal_right'][1] = False
            if y+i <= 5:
                if sign == game_field[x][y + i] and streaks['vertical_left'][1]:
                    streaks['vertical_left'][0] += 1
                else:
                    streaks['vertical_left'][1] = False
            if y - i >= 0:
                if sign == game_field[x][y - i] and streaks['vertical_right'][1]:
                    streaks['vertical_right'][0] += 1
                else:
                    streaks['vertical_right'][1] = False
            if y + i <= 5 and x + i <= 6:
                if sign == game_field[x + i][y + i] and streaks['dia_rising_left'][1]:
                    streaks['dia_rising_left'][0] += 1
                else:
                    streaks['dia_rising_left'][1] = False
            if y - i >= 0 and x - i >= 0:
                if sign == game_field[x - i][y - i] and streaks['dia_rising_right'][1]:
                    streaks['dia_rising_right'][0] += 1
                else:
                    streaks['dia_rising_right'][1] = False
            if y + i <= 5 and x - i >= 0:
                if sign == game_field[x - i][y + i] and streaks['dia_falling_left'][1]:
                    streaks['dia_falling_left'][0] += 1
                else:
                    streaks['dia_falling_left'][1] = False
            if y - i >= 0 and x + i <= 6:
                if sign == game_field[x + i][y - i] and streaks['dia_falling_right'][1]:
                    streaks['dia_falling_right'][0] += 1
                else:
                    streaks['dia_falling_right'][1] = False

        if (streaks['horizontal_left'][0] + streaks['horizontal_right'][0]) >= 3:
            return sign
        if (streaks['vertical_left'][0] + streaks['vertical_right'][0]) >= 3:
            return sign
        if (streaks['dia_rising_left'][0] + streaks['dia_rising_right'][0]) >= 3:
            return sign
        if (streaks['dia_falling_left'][0] + streaks['dia_falling_right'][0]) >= 3:
            return sign

        return False


def checkfortie(game_field):
    return sum(item is not False for item in [item for sublist in game_field for item in sublist]) == 42


def groundmove(move, game_state):
    x = move['x']
    y = move['y']
    for i in range(0, y):
        if game_state[int(x)][i] is False:
            return {'x': x, 'y': i}
    return move


def loop_game(episodes,game=None):
    try:
        from connect4.ai_input import AIPlayer
    except:
        from ai_input import AIPlayer
    try:
        from connect4.game import Game
    except:
        from game import Game

    if game is None:
        game = Game(AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=True), AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=True))
    for i in range(episodes):
        game.play()
        if (i + 1) % int(10000) == 0:
            print((i + 1), "games played")
    return game.stats


def estimatetime(episodes, ask=True, method="default", threads_or_processes=None, test_games=250):
    import time
    import datetime
    try:
        from connect4.multi_threading import playgames_multithread
    except:
        from multi_threading import playgames_multithread
    try:
        from connect4.multi_processing import playgames_multiprocess
    except:
        from multi_processing import playgames_multiprocess

    start_time = time.time()
    if method == "multithreading":
        if threads_or_processes:
            threads_or_processes = 20
        playgames_multithread(test_games, threads_or_processes)
    elif method == "multiprocessing":
        if threads_or_processes:
            threads_or_processes = 8
        playgames_multiprocess(test_games, threads_or_processes)
    elif method == "default":
        loop_game(test_games)
    else:
        if threads_or_processes:
            threads_or_processes = 8
        playgames_multiprocess(test_games, threads_or_processes)

    end_time = time.time()
    time_in_sec = end_time-start_time
    time_for_episodes = time_in_sec/test_games*episodes
    formated_time = str(datetime.timedelta(seconds=time_for_episodes))
    if ask:
        print("Estimated time: "+formated_time)
        while True:
            confirm = input("Do you want to continue? [y/n]").lower()
            if confirm == "y" or confirm == "yes" or confirm == "y" or confirm == "ja":
                return True
            if confirm == "n" or confirm == "no" or confirm == "nein":
                return False
    else:
        return formated_time


def get_qvalues(gamestate):
    try:
        return pickle.load(open("connect4/qvalues/" + filename_of_gamestate(gamestate) + ".p", "rb"))
    except:
        try:
            return pickle.load(open("qvalues/" + filename_of_gamestate(gamestate) + ".p", "rb"))
        except:
            return {}


def set_qvalues(filename, qvalues):
    try:
        pickle.dump(qvalues, open("connect4/qvalues/" + filename + ".p", "wb"),  protocol=2)
    except:
        try:
            pickle.dump(qvalues, open("qvalues/" + filename + ".p", "wb"),  protocol=2)
        except:
            print("Error storing quality values")


def filename_of_gamestate(gamestate):
    if gamestate is None:
        return False
    filename = ""
    for i in range(7):
        for j in range(2):
            if gamestate[i][j] is False:
                filename += "0"
            else:
                filename += gamestate[i][j]
    return filename


def apply_move(game_state, move, sign):
    #faster alternative to deep copy
    new_game_state = json.loads(json.dumps(game_state))
    new_game_state[int(move['x'])][int(move['y'])] = sign
    return new_game_state



def getvalidInputs(game_state):
    validmoves = []
    for i in range(7):
        if game_state[i][5] is False:
            validmoves.append({'x': i, 'y': 5})
    return validmoves