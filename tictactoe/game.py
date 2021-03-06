#from . import util, user_input
import tkinter as gui
from tkinter import messagebox
from util import checkfortie, checkforwinner
from user_input import HumanPlayer
from threading import Event, Thread


class Game:
    def __init__(self, playerOne, playerTwo, q_values={}, create_gui=False):
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        self.q_values = q_values
        self.nextPlayer = playerOne
        self.playerOne.setQValues(self.q_values)
        self.playerTwo.setQValues(self.q_values)
        self.stats = [0, 0, 0]
        self.create_gui = create_gui
        self.game_field = [[False, False, False], [False, False, False], [False, False, False]]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.window = None
        self.text = None

    def clickbutton(self, button):
        if isinstance(self.nextPlayer, HumanPlayer):
            info = button.grid_info()
            move = (int(info["row"]), int(info["column"]))
            self.nextPlayer.setGraphicInput(move)
            #print(move)

    def play(self):
        if self.create_gui:
            self.window = gui.Tk()
            self.window.title("Tic Tac Toe")
            frame = gui.Frame(self.window, width=400, height=400)
            frame.pack()
            frame.focus()
            frame.grid()
            for i in range(3):
                for j in range(3):
                    self.buttons[i][j] = gui.Button(frame, height=5, width=10, text="", command=lambda i=i, j=j: self.clickbutton(self.buttons[i][j]))
                    self.buttons[i][j].config(font=("Courier", 15))
                    self.buttons[i][j].grid(row=i, column=j)
            if isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, HumanPlayer):
                self.text = gui.Label(frame, text="Lets play!")
                self.text.configure(font=("Courier", 15), width=10)
                self.text.grid(row=3)
            self.window.update()

        while True:
            if isinstance(self.nextPlayer, HumanPlayer) and self.create_gui:
                try:
                    ready = Event()
                    self.nextPlayer.ready = ready
                    thread = Thread(target=self.nextPlayer.getGraphicalInput(self.game_field,self.window))
                    thread.start()
                    ready.wait()
                    player_input = self.nextPlayer.getInput(self.game_field)
                    self.buttons[player_input[0]][player_input[1]].configure(text=self.nextPlayer.sign)
                    self.game_field[player_input[0]][player_input[1]] = self.nextPlayer.sign
                    self.window.update()
                except gui.TclError:
                    exit(0)

            else:
                player_input = self.nextPlayer.getInput(self.game_field)
                self.game_field[player_input['x']][player_input['y']] = self.nextPlayer.sign
                if self.create_gui:
                    self.buttons[player_input['x']][player_input['y']].configure(text=self.nextPlayer.sign)

            #print(self.game_field[0], "\n", self.game_field[1], "\n", self.game_field[2], "\n")
           # print(self.game_field)
            winner = checkforwinner(self.game_field) 
            if winner is not False:
                helptext = "Game Over! " + self.nextPlayer.sign + " has won."
                if self.create_gui:
                    messagebox.showinfo(helptext, helptext)
                    self.window.destroy()
                if self.nextPlayer == self.playerOne:
                #if winner == self.playerOne.sign:
                    self.stats[1] += 1
                else:
                    self.stats[2] += 1
                break

            if checkfortie(self.game_field):
                helptext = "It is a Tie! Nobody wins this time!"
                if self.create_gui:
                    messagebox.showinfo(helptext, helptext)
                    self.window.destroy()
                self.stats[0] += 1
                break

            self.switchplayer()

        self.clearboard()
        self.nextPlayer = self.playerOne

    def switchplayer(self):
        if self.nextPlayer == self.playerOne:
            self.nextPlayer = self.playerTwo
        else:
            self.nextPlayer = self.playerOne
        if isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, HumanPlayer) and self.create_gui:
            self.text.configure(text=self.nextPlayer.sign+"´s Turn!")

    def clearboard(self):
        self.game_field = [[False, False, False], [False, False, False], [False, False, False]]
