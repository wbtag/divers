import inquirer
from classes.game import Game
from classes.game_board import GameBoard

playerCountQuestion = [
    inquirer.List(
        "playerCount",
        message="Specify the number of players",
        choices=[1,2,3,4],
    )
]

playerCount = inquirer.prompt(playerCountQuestion)["playerCount"]

Game(playerCount, GameBoard())
