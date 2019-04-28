from random import randint


class RandomPlayer:
    def __init__(self, sign, ready=None):
        self.sign = sign
        self.graphical_move = None

    def setQValues(self, q_values):
        pass

    def getInput(self, game_state):
        return getRandomInput(game_state)


def getRandomInput(game_state):
    validmoves = getvalidInputs(game_state)
    return validmoves[randint(0, (len(validmoves)-1))]


def getvalidInputs(game_state):
    validmoves = []
    for i in range(3):
        for j in range(3):
            if game_state[i][j] is not False:
                validmoves.extend({'x': i, 'y': j})
    return validmoves
