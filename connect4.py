#from tictactoe import game, util, user_input, ai_input, randomized_input
import sys
sys.path.append('connect4')
from connect4.game import Game
from connect4.user_input import HumanPlayer
from connect4.ai_input import AIPlayer
from random import randint
from connect4.util import estimatetime, loop_game
from connect4.multi_threading import playgames_multithread
from connect4.multi_processing import playgames_multiprocess
import time
import datetime
from parsearguments import parse
import sys
from connect4.randomized_input import RandomPlayer
args = {}
def connect4(args=None):
    createGui = False

    if __name__ == '__main__':
        if args is None:
            args = parse(sys.argv[1:], "connect4")

        method = args['method']
        if args['method'] == "unset":
            threads_or_processes = 8
        else:
            threads_or_processes = args[args['method']]

        if 'x' in args:
            createGui = False
            if args['x'] == "h":
                createGui = True
                playerOne = HumanPlayer("x")
            elif args['x'] == "r":
                playerOne = RandomPlayer("x")
            elif (args['x'] == "a" and args['o'] == 'h') or (args['x'] == "a" and args['o'] == 'r')  or args['x'] == "t":
                playerOne = AIPlayer("x", randomizer_factor=0.0)
            elif args['x'] == "a" and args['o'] == 'a':
                playerOne = AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=True)
            else:
                print("Error when selecting player type")
                playerOne = AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=False)
            if args['o'] == "h":
                createGui = True
                playerTwo = HumanPlayer("o")
            elif args['o'] == "r":
                playerTwo = RandomPlayer("o")
            elif (args['o'] == "a" and args['x'] == 'h') or (args['o'] == "a" and args['x'] == 'r') or args['o'] == "t":
                playerTwo = AIPlayer("o", randomizer_factor=0.0)
            elif args['o'] == "a" and args['x'] == 'a':
                playerTwo = AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=True)
            else:
                print("Error when selecting player type")
                playerTwo = AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=False)
            game = Game(playerOne, playerTwo, createGui)
            if createGui:
                game.play()
            else:
                episodes = int(input("Please enter the number of games the ai should play against it other:"))
                if estimatetime(episodes, ask=True, method="default"):
                    start_time = time.time()
                    loop_game(episodes, game)
                    end_time = time.time()
                    time_in_sec = end_time - start_time
                    formated_time = str(datetime.timedelta(seconds=time_in_sec))
                    stats = game.stats
                    print("Time taken: " + formated_time)
                    print(episodes, " games played! \nPlayer x won ", stats[1], "times - ",
                          "{:3.2f}".format(stats[1] / episodes * 100), "%\n",
                          "Player o won ", stats[2], "times - ", "{:3.2f}".format(stats[2] / episodes * 100), "%\n",
                          "There were ", stats[0], "ties - ", "{:3.2f}".format(stats[0] / episodes * 100), "%")

        else:
            if 'mode' in args and args['mode'] in (1, 2, 3, 4):
                mode = args['mode']
            elif 'test' in args:
                mode = 4
            else:
                mode = int(input("Please enter the mode: \n[1 = player vs player]\n[2 = player vs ai\n[3 = ai vs ai]\n:"))

            if mode == 1:
                game = Game(HumanPlayer("x"), HumanPlayer("o"), True)
                game.play()
                args['mode'] = 1
                createGui = True
            elif mode == 2:
                if randint(0, 1) == 1:
                    game = Game(AIPlayer("x", randomizer_factor=0.0), HumanPlayer("o"), True)
                else:
                    game = Game(HumanPlayer("x"), AIPlayer("o", randomizer_factor=0.0), True)
                game.play()
                createGui = True
                args['mode'] = 2
            elif mode == 3 or mode == 4:
                testing = False
                if mode == 4:
                    testing = True
                episodes = int(input("Please enter the number of games the ai should play against it other:"))
                if estimatetime(episodes, ask=True, method=method, threads_or_processes=threads_or_processes):
                    if __name__ == '__main__':
                        start_time = time.time()
                        if method == 'multithreading':
                            stats = playgames_multithread(episodes, args['multithreading'], testing=testing)
                        elif method == 'multiprocessing':
                            stats = playgames_multiprocess(episodes, args['multiprocessing'], testing=testing)
                        elif method == 'default':
                            if testing:
                                stats = loop_game(episodes, Game(AIPlayer("x", randomizer_factor=0.3, training=True), AIPlayer("o", randomizer_factor=0.0, training=True), False))
                            else:
                                stats = loop_game(episodes, Game(AIPlayer("x", randomizer_factor=0.3, learning_rate=0.75, training=True), AIPlayer("o", randomizer_factor=0.3, learning_rate=0.75, training=True), False))
                        else:
                            stats = playgames_multiprocess(episodes, processes=8, testing=testing)
                        end_time = time.time()
                        time_in_sec = end_time - start_time
                        formated_time = str(datetime.timedelta(seconds=time_in_sec))
                        print("Time taken: " + formated_time)
                        print(episodes, " games played! \nPlayer x won ", stats[1], "times - ",
                              "{:3.2f}".format(stats[1] / episodes * 100), "%\n",
                              "Player o won ", stats[2], "times - ", "{:3.2f}".format(stats[2] / episodes * 100), "%\n",
                              "There were ", stats[0], "ties - ", "{:3.2f}".format(stats[0] / episodes * 100), "%")
            else:
                connect4()
                if not createGui:
                    del args['mode']
        if not createGui:
            control = input("Enter [retry] to play another game or enter [quit] to exit: ")
            if control == "quit" or control == "q":
                exit(0)
            else:
                connect4()
                if not createGui:
                    del args['mode']
        else:
            connect4(args)

connect4()
