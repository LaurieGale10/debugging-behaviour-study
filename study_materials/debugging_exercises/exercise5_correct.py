import random

player_1 = random.choice(["Rock","Paper","Scissors"])
print("Player 1 has chosen "+player_1)
player_2 = random.choice(["Rock","Paper","Scissors"])
print("Player 2 has chosen "+player_2)

if player_1 == player_2:
    winner = "Neither"
elif player_1 == "Rock" and player_2 == "Scissors":
    winner = "Player 1"
elif player_1 =="Paper" and player_2 == "Rock":
    winner = "Player 1"
elif player_1 == "Scissors" and player_2 == "Paper":
    winner = "Player 1"
else:
    winner = "Player 2"
print("The winner is "+winner)