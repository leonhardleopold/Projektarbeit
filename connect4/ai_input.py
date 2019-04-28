#from tictactoe import game, util, user_input, ai_input, randomized_input
from util import checkforwinner, checkfortie, groundmove
from random import *


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
        return move

    def getAIInput(self, game_state):
        while True:
            ai_input = self.generateInput(game_state)
            if validateInput(ai_input, game_state):
                return ai_input

    def Q_learn(self, move, game_state):

        game_state_key = self.make_key(game_state)
        next_game_state = apply_move(game_state, move, self.sign)
        next_state_key = self.make_key(next_game_state, sign="other")
        reward = self.getReward(next_game_state)

        if self.q_values.get(game_state_key) is None:
            self.filldictentry(game_state, self.sign)

        if self.q_values.get(next_state_key) is None:
            self.filldictentry(next_game_state, "other")

        if reward == 0.0:
            if self.sign == "x":
                reward = self.discount_factor * min(self.q_values[next_state_key].values())
            elif self.sign == "o":
                reward = self.discount_factor * max(self.q_values[next_state_key].values())

        #newvalue = (1 - self.learning_rate) * self.q_values[game_state_key][(move.get('x'), move.get('y'))] + self.learning_rate * (reward + self.discount_factor * max(self.q_values[next_state_key].values()))
        #q_change = self.learning_rate * (reward - self.q_values[game_state_key][(move.get('x'), move.get('y'))])
        q_change = self.q_values[game_state_key][move.get('x')] + self.learning_rate * (reward - self.q_values[game_state_key][move.get('x')])
        #print("reward", reward, "old value", self.q_values[game_state_key][(move.get('x'), move.get('y'))], "q_change", q_change)
       # print(game_state, reward, q_change, self.q_values[game_state_key][(move.get('x'), move.get('y'))], (self.q_values[game_state_key][(move.get('x'), move.get('y'))] + q_change))
        self.q_values[game_state_key][move.get('x')] = float("{:5.3f}".format(q_change))

    def make_key(self, game_state, sign=None):
        if sign == "other":
            if self.sign == "x":
                keysign = "o"
            elif self.sign == "o":
                keysign = "x"
        elif sign == None:
            keysign = self.sign
        else:
            keysign = sign

        key = ""

        for i in game_state:
            for j in i:
                if j is False:
                    break
                else:
                    key += j
            key += ";"


#        help_game_state = [item for sublist in game_state for item in sublist]
#        for index in help_game_state:
#            if not index:
#                index = "0"
#            key += index
        return key+keysign

    def getReward(self, game_state):
        if checkforwinner(game_state) is not False:
            # if checkforwinner(game_state) == self.sign:
            if checkforwinner(game_state) == "x":
                return 1.0
            # else:
            elif checkforwinner(game_state) == "o":
                return -1.0
        elif checkfortie(game_state):
            # return 0.5
            if self.sign == "x":
                return 0.5
            else:
                # else:
                return -0.5
            # return 0.5
        else:
            return 0.0

    def generateInput(self, game_state):
        if self.q_values.get(self.make_key(game_state)) is None:
            self.filldictentry(game_state, self.sign)

        q_vals = self.q_values[self.make_key(game_state)]

        if randint(0, 100) < self.randomizer_factor*100:
            return random_move(game_state)
        else:
            #x min, o min, x = 1.0, o = -1.0 => 100% o
            #x max, o max, x = 1.0, o = -1.0 => 100% x
            #x min, o max, x = 1.0, o = -1.0 => 50% x, 50% ties => 4% x, 68% o, 27% ties -> really bad
            #x max, o min, x = 1.0, o = -1.0 => 100% o --> preeeety good (but not perfect)

            #
            if self.sign == "x":
                #maximum = max(q_vals, key=q_vals.get)
                maximum = max(list(q_vals.values()))
            elif self.sign == "o":
                #maximum = min(q_vals, key=q_vals.get)
                maximum = min(list(q_vals.values()))

            _list = []
            for move in q_vals:
                if q_vals[move] == maximum:
                    _list.append(move)

            randvalue = randint(0, len(_list)-1)
            move = _list[randvalue]

            return groundmove({'x': move, 'y': 6}, game_state)

    def filldictentry(self, game_state, sign):
        moves = []
        for i in range(7):
            for j in range(6):
                if game_state[i][j] is False:
                    moves.append(i)
                    break

        self.q_values[self.make_key(game_state, sign=sign)] = {move: 1.0 for move in moves}


def apply_move(game_state, move, sign):
    new_game_state = game_state
    new_game_state[move['x']][move['y']] = sign
    return new_game_state


def random_move(game_state):
    while True:
        x = randint(0, 6)
        if not game_state[x][5]:
            return groundmove( {'x': x, 'y': 5}, game_state)


def validateInput(user_input, game_state, user=False):

    if user_input['x'] > 6 or user_input['x'] < 0 or user_input['y'] > 5 or user_input['y'] < 0 or game_state[user_input['x']][user_input['y']] is not False:
        return False
    else:
        return True
