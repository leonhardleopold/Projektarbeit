try:
    from connect4.util import checkforwinner, checkfortie, groundmove, filename_of_gamestate, get_qvalues, apply_move, getvalidInputs
except:
    from util import checkforwinner, checkfortie, groundmove, filename_of_gamestate, get_qvalues, apply_move, getvalidInputs

from random import *

class AIPlayer:
    def __init__(self, sign, randomizer_factor=0.3, learning_rate=0.75, discount_factor=0.9, training=False):
        self.sign = sign
        self.q_values = {}
        self.last_gamestate = [[False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False]]
        self.last_qvalues = {}
        self.training = training
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.randomizer_factor = randomizer_factor

    def getInput(self, game_state, qvalues):
        self.q_values = qvalues
        move = self.generateInput(game_state)
        for m in getvalidInputs(game_state):
            self.Q_learn(groundmove(m,game_state), game_state)
        return move

    def Q_learn(self, move, game_state):
        game_state_key = self.make_key(game_state)
        next_game_state = apply_move(game_state, move, self.sign)
        next_state_key = self.make_key(next_game_state)
        reward = self.getReward(next_game_state)
        if filename_of_gamestate(game_state) == filename_of_gamestate(next_game_state):
            q_values_after_move = self.q_values
        else:
            q_values_after_move = get_qvalues(next_game_state)

        if self.q_values.get(game_state_key) is None:
            self.filldictentry(game_state)

        if q_values_after_move.get(next_state_key) is None and reward == 0.0:
            reward = self.discount_factor * 0.5

        elif reward == 0.0:
            reward = self.discount_factor * max(q_values_after_move[next_state_key].values()) * -1

        q_change = self.q_values[game_state_key][str(move.get('x'))] + self.learning_rate * (
                    reward - self.q_values[game_state_key][str(move.get('x'))])
        self.q_values[game_state_key][move.get('x')] = float("{:5.3f}".format(q_change))

    def make_key(self, game_state):
        key = ""
        for i in game_state:
            for j in i:
                if j is False:
                    break
                else:
                    key += j
            key += ";"
        return key

    def getReward(self, game_state):
        winner = checkforwinner(game_state)
        if winner is not False:
            if winner == self.sign:
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

        # if a move will win you or your opponent the game, take it
        if self.training:
            for i in range(7):
                if validateInput({'x': i, 'y': 5}, game_state):
                    g_move = groundmove({'x': i, 'y': 5}, game_state)
                    if checkforwinner(game_state, g_move, self.sign) is not False:
                        return g_move

        q_vals = self.q_values[self.make_key(game_state)]

        if randint(0, 100) < self.randomizer_factor * 100:
            return random_move(game_state)
        else:
            maximum = max(list(q_vals.values()))
            _list = []
            for move in q_vals:
                if q_vals[move] == maximum:
                    _list.append(move)

            randvalue = randint(0, len(_list) - 1)
            move = _list[randvalue]
            return groundmove({'x': int(move), 'y': 6}, game_state)

    def filldictentry(self, game_state):
        moves = []
        for i in range(7):
            if game_state[i][5] is False:
                moves.append(str(i))

        self.q_values[self.make_key(game_state)] = {move: 0.5 for move in moves}



def random_move(game_state):
    while True:
        x = randint(0, 6)
        if not game_state[x][5]:
                return groundmove({'x': x, 'y': 5}, game_state)


def validateInput(user_input, game_state):
    if user_input['x'] > 6 or user_input['x'] < 0 or user_input['y'] > 5 or user_input['y'] < 0 or \
            game_state[user_input['x']][user_input['y']] is not False:
        return False
    else:
        return True


