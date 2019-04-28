#from . import util, user_input
import tkinter as gui
from tkinter import messagebox
from user_input import HumanPlayer
from util import checkforwinner, checkfortie
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
        self.game_field = [[False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False]]
        self.buttons = [[None for _ in range(7)] for _ in range(6)]
        self.window = None
        self.text = None

    def clickbutton(self, button):
        if isinstance(self.nextPlayer, HumanPlayer):
            info = button.grid_info()
            move = (int(info["column"]), int(info["row"]))
            #print("gridinfo",move)
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
            if isinstance(self.nextPlayer, HumanPlayer):
                ready = Event()
                self.nextPlayer.ready = ready
                thread = Thread(target=self.nextPlayer.getGraphicalInput(self.game_field,self.window))
                thread.start()
                ready.wait()
                player_input = self.nextPlayer.getInput(self.game_field)
                self.buttons[player_input['y']][player_input['x']].configure(text=self.nextPlayer.sign)
                self.game_field[player_input['x']][player_input['y']] = self.nextPlayer.sign
                self.window.update()

            else:
                player_input = self.nextPlayer.getInput(self.game_field)
                self.game_field[player_input['x']][player_input['y']] = self.nextPlayer.sign
                if self.create_gui:
                    self.buttons[player_input['y']][player_input['x']].configure(text=self.nextPlayer.sign)

            #print(self.game_field[0], "\n", self.game_field[1], "\n", self.game_field[2], "\n")
           # print(self.game_field)
            if checkforwinner(self.game_field):
                helptext = "Game Over! " + self.nextPlayer.sign + " has won."
                if self.create_gui:
                    messagebox.showinfo(helptext, helptext)
                    self.window.destroy()
                if self.nextPlayer == self.playerOne:
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

    def switchplayer(self):
        if self.nextPlayer == self.playerOne:
            self.nextPlayer = self.playerTwo
        else:
            self.nextPlayer = self.playerOne
        if isinstance(self.playerOne, HumanPlayer) and isinstance(self.playerTwo, HumanPlayer):
            self.text.configure(text=self.nextPlayer.sign+"´s Turn!")

    def clearboard(self):
        self.game_field = [[False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False], [False, False, False, False, False, False]]

