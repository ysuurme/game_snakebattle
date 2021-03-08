from snakebattle.config import COLORS, ROWS, COLS

class Snake:
    def __init__(self):
        self.body = []
        self.turns = {}
        self.dirx = 0
        self.diry = 1

    def move_snake(self):
        for i, cube in enumerate(self.body):
            pos = (cube.x, cube.y)
            if pos in self.turns:
                turn = self.turns[pos]
                cube.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            elif cube.dirx == -1 and cube.x <= 0:
                cube.x = COLS-1
            elif cube.dirx == 1 and cube.x >= COLS-1:
                cube.x = 1
            elif cube.diry == 1 and cube.y <= 0:
                cube.y = ROWS-1
            elif cube.diry == -1 and cube.y >= ROWS - 1:
                cube.y = 1
            else:
                cube.x = cube.x + cube.dirx
                cube.y = cube.y + cube.diry

class Player1(Snake):
    def __init__(self):
        super().__init__()
        self.color = COLORS['BLUE']
        self.head = Cube(10, 10)
        self.body.append(self.head)


class Player2(Snake):
    def __init__(self):
        super().__init__()
        self.x = 20
        self.y = 20
        self.color = COLORS['YELLOW']
        self.head = cube(x, y)


class Cube:
    def __init__(self, x, y, dirx=0, diry=1, color=COLORS['WHITE']):
        self.x = x  # x position in the game 'grid'
        self.y = y  # y position in the game 'grid'
        self.dirx = dirx
        self.diry = diry
        self.color = color
