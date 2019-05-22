# Projektarbeit

This project includes TicTacToe implemented in Python and the training of an AI with to use of Reinforcement Learning - to be specific: Q Learning. 

Author: Leonhard Leopold, SWD17

Stauts: Version 2.0 
The Ai for the TicTacToe works perfectly after only a short time in training. 
Connect4 is implemented as well. The game and training works, but perfecting the game takes a lot of time.

Possible Future Tasks: Optimizing connect4 to be faster

How to use it:
- Download the code and install python3 preferable a 64bit version.
- In the command line, type: py tictactoe.py or connect4.py to start
- Afterwards you have the option to choose between 3 diffrent modes: 
  - 1. Human vs Human 
  - 2. Human vs AI
  - 3. AI training (AI vs AI)


On the command line the user has different options to play the games:

TicTacToe:

-m : mode [1,2,3] 1 = Human vs Human, 2 = Human vs AI, 3 = AI vs AI

-x : type of first player [r,a,h,t] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor

-o : type of second player [r,a,h,t] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor

-t : testing - no argument needed - both players are AI's without randomizer factor



Connect4:

-m : mode [1,2,3] 1 = Human vs Human, 2 = Human vs AI, 3 = AI vs AI

-t : multithreading [number of threads used]

-p : multiprocessing [number of processes used]

-d : default - no multithreading or multiprocessing used

-x : type of first player [r,a,h] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor

-o : type of second player [r,a,h] r = Randomized Input, a = AI, h = Human, t = AI without randomizer factor

--test : testing - no argument needed - both players are AI's without randomizer factor
