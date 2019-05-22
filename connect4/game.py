import tkinter as gui
from tkinter import messagebox
try:
    from connect4.ai_input import AIPlayer
except:
    from ai_input import AIPlayer
try:
    from connect4.user_input import HumanPlayer
except:
    from user_input import HumanPlayer
try:
    from connect4.util import checkforwinner, checkfortie, get_qvalues, set_qvalues, filename_of_gamestate, apply_move
except:
    from util import checkforwinner, checkfortie, get_qvalues, set_qvalues, filename_of_gamestate, apply_move
from threading import Event, Thread


class Game:
    def __init__(self, playerOne, playerTwo, create_gui=False):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.nextPlayer = playerOne
        self.stats = [0, 0, 0]
        self.create_gui = create_gui
        self.game_field = [[False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False]]
        self.buttons = [[None for _ in range(7)] for _ in range(6)]
        self.window = None
        self.text = None
        self.qvalues = get_qvalues(self.game_field)

    def clickbutton(self, button):
        if isinstance(self.nextPlayer, HumanPlayer):
            info = button.grid_info()
            move = (int(info["column"]), int(info["row"]))
            self.nextPlayer.setGraphicInput(move)

    def play(self):
        if self.create_gui:
            self.window = gui.Tk()
            self.window.title("Connect4")
            frame = gui.Frame(self.window, width=400, height=400)
            frame.pack()
            frame.focus()
            frame.grid()
            for i in range(6):
                for j in range(7):
                    self.buttons[i][j] = gui.Button(frame, height=5, width=10, text="", command=lambda i=i, j=j: self.clickbutton(self.buttons[5-i][j]))
                    self.buttons[i][j].config(font=("Courier", 15))
                    self.buttons[i][j].grid(row=5-i, column=j)
            if isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, HumanPlayer):
                self.text = gui.Label(frame, text="Lets play!")
                self.text.configure(font=("Courier", 15), width=10)
                self.text.grid(row=8)
            self.window.update()

        while True:
            if isinstance(self.nextPlayer, HumanPlayer) and self.create_gui:
                try:
                    ready = Event()
                    self.nextPlayer.ready = ready
                    thread = Thread(target=self.nextPlayer.getGraphicalInput(self.game_field,self.window))
                    thread.start()
                    ready.wait()
                    player_input = self.nextPlayer.getInput(self.game_field, None)
                    self.buttons[player_input['y']][player_input['x']].configure(text=self.nextPlayer.sign)
                    self.game_field[player_input['x']][player_input['y']] = self.nextPlayer.sign
                    self.window.update()
                except gui.TclError:
                    exit(0)
            elif isinstance(self.nextPlayer, AIPlayer):
                move = self.nextPlayer.getInput(self.game_field, self.qvalues)
                old_filename = filename_of_gamestate(self.game_field)
                self.game_field[move['x']][move['y']] = self.nextPlayer.sign
                new_filename = filename_of_gamestate(self.game_field)
                if old_filename != new_filename:
                    set_qvalues(old_filename, self.qvalues)
                    self.qvalues = get_qvalues(self.game_field)
                if self.create_gui:
                    self.buttons[move['y']][move['x']].configure(text=self.nextPlayer.sign)
            else:
                player_input = self.nextPlayer.getInput(self.game_field, None)
                self.game_field[player_input['x']][player_input['y']] = self.nextPlayer.sign
                if self.create_gui:
                    self.buttons[player_input['y']][player_input['x']].configure(text=self.nextPlayer.sign)

            winner = checkforwinner(self.game_field) 
            if checkforwinner(self.game_field):
                set_qvalues(filename_of_gamestate(self.game_field), self.qvalues)
                helptext = "Game Over! " + self.nextPlayer.sign + " has won."
                if self.create_gui:
                    messagebox.showinfo(helptext, helptext)
                    self.window.destroy()
                if winner == self.playerOne.sign:
                    self.stats[1] += 1
                else:
                    self.stats[2] += 1

                break

            if checkfortie(self.game_field):
                set_qvalues(filename_of_gamestate(self.game_field), self.qvalues)
                helptext = "It is a Tie! Nobody wins this time!"
                if self.create_gui:
                    messagebox.showinfo(helptext, helptext)
                    self.window.destroy()
                self.stats[0] += 1
                break

            self.switchplayer()

        self.clearboard()
        self.qvalues = get_qvalues(self.game_field)
        self.nextPlayer = self.playerOne

    def switchplayer(self):
        if self.nextPlayer == self.playerOne:
            self.nextPlayer = self.playerTwo
        else:
            self.nextPlayer = self.playerOne
        if isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, HumanPlayer) and self.create_gui:
            self.text.configure(text=self.nextPlayer.sign+"´s Turn!")

    def clearboard(self):
        self.game_field = [[False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False]]

