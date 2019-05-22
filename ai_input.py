#from tictactoe import game, util, user_input, ai_input, randomized_input
from util import checkforwinner, checkfortie, getvalidInputs
from random import *
import json

class AIPlayer:
    def __init__(self, sign, randomizer_factor=0.9, learning_rate=0.3, discount_factor=0.9):
        self.sign = sign
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.randomizer_factor = randomizer_factor

# setter of qvaules? set by reference?
    def setQValues(self, q_values):
        self.q_values = q_values

    def getInput(self, game_state):
        move = self.getAIInput(game_state)
        self.Q_learn(move, game_state)
        for m in getvalidInputs(game_state):
            self.Q_learn(m, game_state)
        return move

    def getAIInput(self, game_state):
        while True:
            ai_input = self.generateInput(game_state)
            if validateInput(ai_input, game_state):
                return ai_input

    def Q_learn(self, move, game_state):
        game_state_key = self.make_key(game_state)
        next_game_state = apply_move(game_state, move, self.sign)
        next_state_key = self.make_key(next_game_state)
        reward = self.getReward(next_game_state)
        if self.q_values.get(game_state_key) is None:
            self.filldictentry(game_state)

        if self.q_values.get(next_state_key) is None and reward == 0.0:
            reward = self.discount_factor * 0.5
        elif reward == 0.0:
            reward = self.discount_factor * max(self.q_values[next_state_key].values()) * -1

        q_change = self.learning_rate * (reward - self.q_values[game_state_key][(move.get('x'), move.get('y'))])
        self.q_values[game_state_key][(move.get('x'), move.get('y'))] += q_change

    def make_key(self, game_state):
        key = ""
        help_game_state = [item for sublist in game_state for item in sublist]
        for index in help_game_state:
            if not index:
                index = "0"
            key += index

        return key

    def getReward(self, game_state):
        if checkforwinner(game_state) is not False:
            if checkforwinner(game_state) == self.sign:
                return 1.0
            else:
                return -1.0
        elif checkfortie(game_state):
            return 0.5
        else:
            return 0.0

    def generateInput(self, game_state):
        if self.q_values.get(self.make_key(game_state)) is None:
            self.filldictentry(game_state)

        q_vals = self.q_values[self.make_key(game_state)]

        if randint(0, 100) < self.randomizer_factor*100:
            return random_move(game_state)
        else:
            maximum = max(list(q_vals.values()))
            _list = []
            for move in q_vals:
                if q_vals[move] == maximum:
                    _list.append(move)

            randvalue = randint(0, len(_list)-1)
            move = _list[randvalue]
            x, y = move
            return {'x': x, 'y': y}

    def filldictentry(self, game_state):
        moves = [(x, y) for x in range(3) for y in range(3) if not game_state[x][y]]
        self.q_values[self.make_key(game_state)] = {move: 0.5 for move in moves}


def apply_move(game_state, move, sign):
    new_game_state = json.loads(json.dumps(game_state))
    new_game_state[move['x']][move['y']] = sign
    return new_game_state


def random_move(game_state):
    while True:
        x = randint(0, 2)
        y = randint(0, 2)
        if game_state[x][y] is False:
            return {'x': x, 'y': y}


def validateInput(user_input, game_state):
    if user_input['x'] > 2 or user_input['x'] < 0 or user_input['y'] > 2 or user_input['y'] < 0 or game_state[user_input['x']][user_input['y']] is not False:
        return False
    else:
        return True
