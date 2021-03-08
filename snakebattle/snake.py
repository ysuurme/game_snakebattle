from snakebattle.config import COLORS

class Snake:
    def __init__(self):
        self.body = []
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def move(self):


class Player1(Snake):
    def __init__(self):
        super().__init__()
        self.x = 10
        self.y = 10
        self.color = COLORS['BLUE']
        self.head = cube(x, y)


class Player2(Snake):
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 20
        self.color = COLORS['YELLOW']
        self.head = cube(x, y)