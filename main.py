import inquirer
from classes.game import Game
from classes.game_board import GameBoard

def main():
    player_count_question = [
        inquirer.List(
            "player_count",
            message="Specify the number of players",
            choices=[1,2,3,4,5,6],
        )
    ]

    player_count = inquirer.prompt(player_count_question)["player_count"]

    Game(player_count, GameBoard())

if __name__ == "__main__":
    main()