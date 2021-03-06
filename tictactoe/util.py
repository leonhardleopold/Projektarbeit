def checkforwinner(game_field):
    if sum(item is not False for item in [item for sublist in game_field for item in sublist]) < 5:
        return False

    for i in range(0, 3):
        if game_field[0][i] == game_field[1][i] and game_field[1][i] == game_field[2][i] and game_field[0][i] is not False:
            return game_field[0][i]
        if game_field[i][0] == game_field[i][1] and game_field[i][1] == game_field[i][2] and game_field[i][0] is not False:
            return game_field[i][0]

    if (game_field[0][0] == game_field[1][1] and game_field[1][1] == game_field[2][2] and game_field[1][1] is not False) or (game_field[2][0] == game_field[1][1] and game_field[1][1] == game_field[0][2]  and game_field[1][1] is not False):
        return game_field[1][1]

    return False


def checkfortie(game_field):
    return sum(item is not False for item in [item for sublist in game_field for item in sublist]) == 9


def estimatetime(episodes, q_values):
    from game import Game
    from ai_input import AIPlayer
    from user_input import HumanPlayer
    import time
    import datetime

    test_game = Game(AIPlayer("x"), AIPlayer("o"), q_values)
    start_time = time.time()
    for _ in range(1000):
        test_game.play()
    end_time = time.time()
    time_in_sec = end_time-start_time
    time_for_episodes = time_in_sec/1000*episodes
    formated_time = str(datetime.timedelta(seconds=time_for_episodes))
    print("Estimmated time: "+formated_time)
    while True:
        confirm = input("Do you want to continue? [y/n]").lower()
        if confirm == "y" or confirm == "yes" or confirm == "j" or confirm == "ja":
            return True
        if confirm == "n" or confirm == "no" or confirm == "nein":
            return False


def getvalidInputs(game_state):
    validmoves = []
    for i in range(3):
        for j in range(3):
            if game_state[i][j] is False:
                validmoves.append({'x': i, 'y': j})
    return validmoves