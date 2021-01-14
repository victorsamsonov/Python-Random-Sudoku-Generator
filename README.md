# Python-Random-Sudoku-Generator

I decided to challenge myself and test my python knowledge while at the same time learning a new library (pygame) in order to grow as a programmer/ CS students. I decided to go with a random sudoku generator since I would be able to show that I am able to organize my projects and am comfortable with using python. 

The project is Divided into 4 sections:

  Sudoku.py:
    A basic implementation of what is later on displayed in the Game.py file, which takes a default sudoku board, displays it on the console and completes it once the code is ran.
    The same is done with a randomly generated sudoku.
   Square.py:
    The Square.py class is later on used to setup Board.py. Each square has it's own styling defined in the class alongised with a value and a temporary value that the user is         able to change.
   Board.py:
    This class alows to display a 9 x 9 board, in which each element is formed by a square, containing its own values. The class also detects when a specific square is selected/       clicked by the user and updates the instance of the class whenver a change is made.
   Game.py
    It manages all the states of the game which primarily are the menu and its submenus, incluidng the game itself, which all takes place inside of a game handling function. This     class uses pygame in order to make it as interactive as possible for the user since it allows to take inputs from the user with ease.
   
