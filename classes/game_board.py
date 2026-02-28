import random

class GameBoard:
    """The virtual game board."""
    def __init__(self):
        self.tiles = []
        for i in range(32):
            self.tiles.append([])
        self.assign_treasures()

    def assign_treasures(self):
        """Assign treasures to game tiles."""
        for i, tile in enumerate(self.tiles):
            if i <= 7:
                tile.append(random.randint(0,10))
            elif i <= 15:
                tile.append(random.randint(10,20))
            elif i <= 23:
                tile.append(random.randint(15,30))
            else:
                tile.append(random.randint(25,40))

    def clean(self):
        """Remove empty tiles from the game board."""
        self.tiles = [tile for tile in self.tiles if tile]
