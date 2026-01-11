from dataclasses import dataclass, field
from typing import List, Tuple, Optional

from constants import COLORS, COLOR_P1, COLOR_P2, ROWS, COLS, P1_START_POS, P2_START_POS


@dataclass
class Cube:
    """Represents a single block of the snake's body on the grid."""
    x: int
    y: int
    color: Tuple[int, int, int] = field(default_factory=lambda: COLORS['WHITE'])


class Snake:
    def __init__(self) -> None:
        self.color: Tuple[int, int, int] = COLORS['WHITE']
        self.head: Optional[Cube] = None
        self.length: int = 1
        self.body: List[Cube] = []
        self.dir: Tuple[int, int] = (0, 0)

    def move_snake_body(self) -> bool:
        if self.head is None:
            return False

        x = self.head.x
        y = self.head.y
        dx, dy = self.dir

        # Grid wrapping logic
        if x == 0 and dx == -1:  # Move left from col 0 -> wrap to max col
            x = COLS - 1
        elif x == COLS - 1 and dx == 1:  # Move right from max col -> wrap to 0
            x = 0
        elif y == 0 and dy == -1:  # Move up from top row -> wrap to bottom
            y = ROWS - 1
        elif y == ROWS - 1 and dy == 1:  # Move down from bottom -> wrap to top
            y = 0
        else:
            x += dx
            y += dy

        # Collision detection with self
        # Note: Using dataclass equality check logic here could be applied if we constructed a temporary Cube,
        # but checking coordinates directly is efficient for this loop.
        for part in self.body:
            if self.length > 1 and part.x == x and part.y == y:
                return False

        self.head = Cube(x, y, self.color)
        self.body.insert(0, self.head)
        while len(self.body) > self.length:
            self.body.pop()
        return True

    def eat_snack(self) -> None:
        if self.head:
            # Create a duplicate of the head to extend the body, logic handled in move loop typically
            # But here it seems to be adding a segment. The original code logic was:
            # self.head = Cube(self.head.x, self.head.y, self.color)
            # self.body.insert(0, self.head)
            # This effectively grows the snake by adding a new head on top of the old one?
            # Actually, usually 'eat_snack' simply increments length, and the 'move' loop respects that length.
            # However, respecting the legacy logic:
            new_head = Cube(self.head.x, self.head.y, self.color)
            self.body.insert(0, new_head)
            self.head = new_head


class Player1(Snake):
    def __init__(self) -> None:
        super().__init__()
        self.color = COLOR_P1
        self.head = Cube(P1_START_POS[0], P1_START_POS[1], self.color)
        self.body.append(self.head)


class Player2(Snake):
    def __init__(self) -> None:
        super().__init__()
        self.color = COLOR_P2
        self.head = Cube(P2_START_POS[0], P2_START_POS[1], self.color)
        self.body.append(self.head)
