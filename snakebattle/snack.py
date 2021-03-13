from .config import COLORS


class Snack:
    def __init__(self, x, y, color=COLORS['WHITE']):
        self.x = x  # x position in the game 'grid'
        self.y = y  # y position in the game 'grid'
        self.color = color
