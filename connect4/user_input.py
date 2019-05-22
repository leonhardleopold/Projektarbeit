try:
    from connect4.util import groundmove
except:
    from util import groundmove

class HumanPlayer:
    def __init__(self, sign, ready=None):
        self.sign = sign
        self.graphical_move = None
        self.ready = ready

    def setQValues(self, q_values):
        pass

    def getInput(self, game_state, qvalues):
        user_input = self.graphical_move
        self.graphical_move = None
        return user_input
        #return getUserInput(self, game_state)
        #print("getuserinput")

    def setGraphicInput(self, move):
        self.graphical_move = move

    def getGraphicalInput(self, game_state, window):
        while True:
            window.update()
            if self.graphical_move is not None:
                #print(self.graphical_move)
                if validateInput({'x': self.graphical_move[0], 'y': self.graphical_move[1]}, game_state):
                    self.graphical_move = groundmove({'x': self.graphical_move[0], 'y': self.graphical_move[1]}, game_state)
                    self.ready.set()
                    break
                else:
                    self.graphical_move = None


def getUserInput(player, game_state):
    print("It is the turn of player:", player.sign)
    while True:
        try:
            x = int(input("In which column do you want to make your sign? [1, 2, 3, 4, 5, 6 or 7]:"))-1
            y = 6
            user_input = {'x': x, 'y': y}
        except ValueError:
            print("Unexpected input! Please try again!")
        else:
            if validateInput(user_input, game_state):
                return groundmove(user_input, game_state)


def validateInput(user_input, game_state):
    if user_input['x'] > 6 or user_input['x'] < 0 or user_input['y'] > 5 or user_input['y'] < 0:
        print("Unexpected input! Please try again!")
        return False
    if game_state[user_input['x']][user_input['y']] is not False:
        print("There is already a sign set for row", user_input['x']+1, "and column", user_input['y']+1, "\nPlease try again!")
        return False

    return True
