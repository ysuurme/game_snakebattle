from typing import Tuple
from constants import COLORS
from src.resources import SNACK_IMAGE


class Snack:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int] = COLORS['WHITE']) -> None:
        self.x: int = x
        self.y: int = y
        self.color: Tuple[int, int, int] = color
        self.image = SNACK_IMAGE