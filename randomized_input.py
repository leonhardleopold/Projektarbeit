from random import randint
from util import getvalidInputs


class RandomPlayer:
    def __init__(self, sign):
        self.sign = sign
        self.graphical_move = None

    def setQValues(self, q_values):
        pass

    def getInput(self, game_state):
        while True:
            random_input = getRandomInput(game_state)
            if validateInput(random_input, game_state):
                return random_input


def getRandomInput(game_state):
    validmoves = getvalidInputs(game_state)
    return validmoves[randint(0, (len(validmoves)-1))]


def validateInput(user_input, game_state):
    if user_input['x'] > 2 or user_input['x'] < 0 or user_input['y'] > 2 or user_input['y'] < 0:
        return False
    if game_state[user_input['x']][user_input['y']] is not False:
        return False

    return True
