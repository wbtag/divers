"""Player dataclass"""
import dataclasses

@dataclasses.dataclass
class Player:
    """A player."""
    def __init__(self, name: str):
        self.name = name
        self.surfacing = False
        self.treasures = []
        self.inventory = []
        self.position = 0
        self.boosting = False
        self.passed = False

    def reset(self):
        """Reset the player's round-dependent properties."""
        self.position = 0
        self.treasures = []
        self.surfacing = False
        self.passed = False
