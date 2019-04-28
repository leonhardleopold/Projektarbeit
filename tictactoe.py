#from tictactoe import game, util, user_input, ai_input, randomized_input
import sys
sys.path.append('tictactoe')
from game import Game
from user_input import HumanPlayer
from ai_input import AIPlayer
from random import randint
import pickle as pickle
import json
from util import estimatetime



while True:
    q_values = pickle.load(open("tictactoe/trainingdata.p", "rb"))

    mode = int(input("Please enter the mode: \n[1 = player vs player]\n[2 = player vs ai\n[3 = ai vs ai]\n:"))
    if mode == 1:
        game = Game(HumanPlayer("x"), HumanPlayer("o"), {}, True)
        game.play()
    elif mode == 2:
        if randint(0, 1) == 1:
            game = Game(AIPlayer("x", randomizer_factor=0.0), HumanPlayer("o"), q_values, True)
        else:
            game = Game(HumanPlayer("x"), AIPlayer("o", randomizer_factor=0.0), q_values, True)
        game.play()

    elif mode == 3 or mode == 4 or mode == 5:
        if mode == 3:
            game = Game(AIPlayer("x", randomizer_factor=0.9), AIPlayer("o", randomizer_factor=0.9), q_values)
        elif mode == 4:
            game = Game(AIPlayer("x", randomizer_factor=0.0, learning_rate=0.5, discount_factor=0.5), AIPlayer("o", randomizer_factor=0.0, learning_rate=0.5, discount_factor=0.5), q_values)
        elif mode == 5:
            game = Game(AIPlayer("x", randomizer_factor=0.0, learning_rate=0.5, discount_factor=0.5), AIPlayer("o", randomizer_factor=1.0, learning_rate=0.5, discount_factor=0.5), q_values)

        episodes = int(input("Please enter the number of games the ai should play against it other:"))
        if estimatetime(episodes, q_values):
            for _ in range(episodes):
                game.play()

            stats = game.stats
            print(episodes, " games played! \nPlayer x won ", stats[1], "times - ", "{:3.2f}".format(stats[1]/episodes*100), "%\n",
                  "Player o won ", stats[2], "times - ", "{:3.2f}".format(stats[2]/episodes*100), "%\n",
                  "There were ", stats[0], "ties - ", "{:3.2f}".format(stats[0]/episodes*100), "%")

    else:
        continue

    pickle.dump(game.q_values, open("tictactoe/trainingdata.p", "wb"))
    json_q_values = {}
    for gamestate in sorted(q_values):
        help_vals = {}
        for item in q_values.get(gamestate):
            item1, item2 = item
            help_vals["("+str(item1)+", "+str(item2)+")"]=q_values[gamestate][item]
        json_q_values[""+gamestate] = help_vals

    json.dump(json_q_values, open("tictactoe/trainingdata.json", "w"), ensure_ascii=False, sort_keys=True, indent=4)
    control = input("Enter [retry] to play another game or enter [quit] to exit: ")
    if control == "quit" or control == "q":
        break




