class HumanPlayer:
    def __init__(self, sign, ready=None):
        self.sign = sign
        self.graphical_move = None
        self.ready = ready

    def setQValues(self, q_values):
        pass

    def getInput(self, game_state):
        user_input = self.graphical_move
        self.graphical_move = None
        return user_input
        #if you want to use the command line
        #return getUserInput(self, game_state)


    def setGraphicInput(self, move):
        self.graphical_move = move

    def getGraphicalInput(self, game_state, window):
        while True:
            window.update()
            if self.graphical_move is not None:
                if validateInput({'x': self.graphical_move[0], 'y': self.graphical_move[1]}, game_state):
                    self.ready.set()
                    break
                else:
                    self.graphical_move = None


def getUserInput(player, game_state):
    print(game_state[0], "\n", game_state[1], "\n", game_state[2])
    print("It is the turn of player:", player.sign)
    while True:
        try:
            x = int(input("In which row do you want to make your sign? [1, 2, or 3]:"))-1
            y = int(input("In which column do you want to make your sign? [1, 2, or 3]:"))-1
            user_input = {'x': x, 'y': y}
        except ValueError:
            print("Unexpected input! Please try again!")
        else:
            if validateInput(user_input, game_state):
                return user_input


def validateInput(user_input, game_state):
    if user_input['x'] > 2 or user_input['x'] < 0 or user_input['y'] > 2 or user_input['y'] < 0:
        print("Unexpected input! Please try again!")
        return False
    if game_state[user_input['x']][user_input['y']] is not False:
        print("There is already a sign set for row", user_input['x']+1, "and column", user_input['y']+1, "\nPlease try again!")
        return False

    return True
