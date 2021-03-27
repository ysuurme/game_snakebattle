from snakebattle.config import COLORS, COLOR_P1, COLOR_P2, ROWS, COLS


class Snake:
    def __init__(self):
        self.color = None
        self.head = None
        self.length = 1
        self.body = []
        self.dir = (0, 0)

    def move_snake_body(self):
        x = self.head.x
        y = self.head.y
        if self.head.x == 0 and self.dir[0] == -1:  # snake moves from column 0 to left, enter game right
            x = COLS - 1
        elif self.head.x == COLS - 1 and self.dir[0] == 1:  # snake moves from max column to right, enter game left
            x = 0
        elif self.head.y == 0 and self.dir[1] == -1:  # snake moves from top row to above, enter game last row
            y = ROWS - 1
        elif self.head.y == ROWS - 1 and self.dir[1] == 1:  # snake moves from last row down, enter game top row
            y = 0
        else:
            x += self.dir[0]
            y += self.dir[1]

        for part in self.body:
            if self.length > 1 and part.x == x and part.y == y:
                return False

        self.head = Cube(x, y, self.color)
        self.body.insert(0, self.head)
        while len(self.body) > self.length:
            self.body.pop()
        return True

    def eat_snack(self):
        self.head = Cube(self.head.x, self.head.y, self.color)
        self.body.insert(0, self.head)


class Player1(Snake):
    def __init__(self):
        super().__init__()
        self.color = COLOR_P1
        self.head = Cube(10, 10)
        self.body.append(self.head)


class Player2(Snake):
    def __init__(self):
        super().__init__()
        self.color = COLOR_P2
        self.head = Cube(20, 20)
        self.body.append(self.head)


class Cube:
    def __init__(self, x, y, color=COLORS['WHITE']):
        self.x = x  # x position in the game 'grid'
        self.y = y  # y position in the game 'grid'
        self.color = color
