"""Game classes"""
import time
import os
import random
from itertools import combinations
import inquirer
from classes.game_board import GameBoard
from classes.player import Player
from typing import Callable

class Game:
    """You just lost the Game."""

    def __init__(self, player_count: int, game_board: GameBoard):
        self.game_board = game_board
        self.players = []
        self.init_players(player_count)
        self.round = 0
        self.play_game()

    def init_players(self, player_count: int):
        """Initialise player instances."""
        for i in range(0,player_count):
            print(f"Enter player {i+1}'s name")
            name = input()
            player = Player(name)
            self.players.append(player)

    def play_game(self):
        """Start the game."""
        self.round += 1
        while self.round <= 3:
            print(f"Round {self.round}")
            os.system("cls" if os.name == "nt" else "clear")
            Round(self)
            self.round += 1
            self.game_board.clean()

            question = [
                inquirer.List(
                    "choice",
                    f"End of round {self.round-1}",
                    [f"Proceed to round {self.round}"],
                )
            ]

            decision = inquirer.prompt(question)["choice"]
        self.end_game()

    def end_game(self):
        """Handle the endgame."""
        player_scores = [(player.name, sum(player.inventory))  for player in self.players]
        if all(player[1] == 0 for player in player_scores):
            print("Everyone drowned, the depths win")
        else:
            player_scores.sort(key=lambda x: -x[1])
            print(f"{player_scores[0][0]} is the winner with {player_scores[0][1]} points")

class Round:
    """A game round."""
    def __init__(self, game: Game):
        self.game = game
        self.air = 25
        self.game_board = game.game_board
        self.play_round()
        self.boosting = False

    def play_round(self):
        """Play the round."""
        while self.air > 0 and not all(player.passed is True for player in self.game.players):
            for player in self.game.players:
                PlayerTurn(self, player)
        self.end()

    def reduce_air(self, amount: int):
        """Reduce remaining air."""
        self.air = self.air - amount if self.air - amount >= 0 else 0

    def end(self):
        """Handle round endgame."""
        for player in self.game.players:
            self.game.players.sort(key=lambda x: x.position)
            if player.position != 0:
                self.game_board.tiles.append(player.treasures)
            else:
                player.inventory += player.treasures
            player.reset()

    def visualise_board(self, delay: bool):
        """Print the current state of the game board to console."""
        players = [(player.name[0].upper(), player.position) for player in self.game.players]
        players_in_submarine = [player[0] for player in players if player[1] == 0]
        tiles = []
        sub = "( _ o _ o _ o _ )"
        for i, player in enumerate(players_in_submarine):
            sub = sub.replace("_", player, 1)
        for i, pos in enumerate(self.game_board.tiles):
            match = next((position for position in players if position[1] == i+1), None)
            if match:
                tiles.append(f"[{match[0]}]")
            else:
                tile_count = len(self.game_board.tiles[i])
                tiles.append(f"[{tile_count if tile_count > 0 else "X"}]")
        print(sub + "".join(tiles))
        if delay:
            time.sleep(1)

class PlayerTurn:
    """A player's turn."""
    def __init__(self, parent_round: Round, player: Player):
        self.parent_round = parent_round
        self.player = player
        self.tiles = self.parent_round.game.game_board.tiles
        self.moved = False
        self.visualise_board = self.parent_round.visualise_board
        self.play()

    def play(self):
        """Start and handle a player's turn."""
        if (self.player.position <= 0 and not self.player.surfacing) or self.player.position > 0:

            self.player.boosting = False
            self.reduce_air(len(self.player.treasures))

            self.visualise_board(False)
            print(f"{self.player.name}'s turn")
            print(f"There is {self.parent_round.air} air left.")

            self.prompt_player_choice()

    def prompt_player_choice(self):
        """Display available moves to a player and facilitate the player's choice."""

        os.system("cls" if os.name == "nt" else "clear")
        self.visualise_board(False)

        choices = [
            choice for choice, condition in (
                (
                    "Start surfacing",
                    self.player.position > 0 and not self.moved and not self.player.surfacing
                ),
                (
                    "Move",
                    not self.moved
                ),
                (
                    "Move with boost",
                    not self.moved and self.parent_round.air > 0 and not self.player.boosting
                ),
                (
                    "Grab treasure",
                    self.player.position > 0 and self.moved and self.tiles[self.player.position-1]
                ),
                (
                    "Drop treasure",
                    self.player.position > 0 and self.moved and self.player.treasures
                ),
                (
                    "Pass", 
                    self.player.position > 0 and self.moved
                )
            ) if condition
        ]

        if choices:
            question = [
                inquirer.List(
                    "choice",
                    f"{self.player.name}'s turn. Depth: {self.player.position} Air: {self.parent_round.air}",
                    choices,
                )
            ]

            decision = inquirer.prompt(question)["choice"]
            os.system("cls" if os.name == "nt" else "clear")

            decision_actions = {
                "Move": self.move,
                "Move with boost": self.boost,
                "Start surfacing": self.surface,
                "Grab treasure": self.grab_treasure,
                "Drop treasure": self.drop_treasure,
                "Pass": None
            }

            self.handle_decision(decision_actions[decision])

    def handle_decision(self, decision: Callable[[], None]):
        """Handle a move made by the player."""
        if decision:
            decision()
            if decision not in [self.grab_treasure, self.drop_treasure]:
                self.prompt_player_choice()

    # Player move functions

    def surface(self):
        """Toggle the surfacing property for the active player."""
        self.player.surfacing = True

    def boost(self):
        """Toggle the boosting property for the active player."""
        self.player.boosting = True
        self.reduce_air(1)
        self.move()

    def grab_treasure(self):
        """Handle treasure grabbing."""
        self.player.treasures.append(self.tiles[self.player.position-1][0])
        self.tiles[self.player.position-1].pop()

    def drop_treasure(self):
        """Handle treasure dropping."""
        dropped_treasure = self.player.treasures.pop()
        self.tiles[self.player.position-1].append(dropped_treasure)

    def reduce_air(self, amount: int):
        """Handle air reduction."""
        self.parent_round.reduce_air(amount)

    def move(self):
        """Handle movement for the active player."""
        dice = [random.randint(0,3) for i in range(3)]

        if not self.player.boosting:
            dice_combos = [
                sum(pair)-len(self.player.treasures)
                if sum(pair)-len(self.player.treasures) >= 1 else 0
                for pair in combinations(dice, 2)
            ]
            a, b, c = dice_combos

            question = [
                inquirer.List(
                    'diceCombination',
                    message=f"The following moves are possible: A) {a} B) {b} C) {c}",
                    choices=["A", "B", "C"],
                ),
            ]

            self.visualise_board(False)
            choice = inquirer.prompt(question)
            options = {"A": a, "B": b, "C": c}

            movement = options[choice["diceCombination"]]
        else:
            movement = sum(dice)-len(self.player.treasures) if sum(dice)-len(self.player.treasures) >= 1 else 0

        os.system("cls" if os.name == "nt" else "clear")
        self.visualise_board(False)
        if self.player.boosting:
            print(f"Rolled a total of {sum(dice)}, moving {movement} tiles.")

        if movement != 0:
            positions = [player.position for player in self.parent_round.game.players]

            time.sleep(1)

            for i in range(movement):
                self.player.position += 1 if not self.player.surfacing else -1

                if self.player.position == 0:
                    self.player.passed = True
                    break

                if any(position == self.player.position for position in positions):
                    self.player.position += 1 if self.player.surfacing is False else -1

                os.system("cls" if os.name == "nt" else "clear")
                self.visualise_board(True)
                os.system("cls" if os.name == "nt" else "clear")

        self.moved = True
