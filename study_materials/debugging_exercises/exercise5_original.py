#This program simulates a game of rock, paper, scissors between two players. This is done using the following steps:
# Randomly generate a choice for each player using the random.choice() function, which selects a random item from a given list.
# Work out which player won the game or if it was a draw.
# Print the winner to the screen. If the match is a draw, then "The winner is Neither" should be printed.

#This program has 3 errors.
import random

player_1 = random.choice(["Rock","Paper","Scissors"])
print("Player 1 has chosen "+player_1)
player_2 = random.choice(["Rock","Paper","Scissors"])
print("Player 2 has chosen "+player_2)

if player_1 == player_2:
    winner = "Neither"
elif player_1 == "Rock" and player_2 == "Scissors":
    winner = "Player 1"
elif player_1 =="Paper" or player_2 == "Rock":
    winner = "Player 1"
elif player_1 == "Scissors" or player_2 == "Paper":
    winner = "Player 1"
elif:
    winner = "Player 2"
    print("The winner is "+winner)

#Errors:
# 2 logical errors on the if statement conditions on lines 18, and 20; should be "and" rather than "or"
# Syntax error on line 22; should be "else" rather than "elif"
# The print statement on line 24 should not be indented