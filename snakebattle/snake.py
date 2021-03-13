from snakebattle.config import COLORS, ROWS, COLS


class Snake:
    def __init__(self):
        self.body = []
        self.moves = [(0, 0)]

    def move_snake(self):
        for i, cube in enumerate(self.body):
            if cube.x == 0 and self.moves[i][0] == -1:  # snake moves from column 0 to left, enter game right
                cube.x = COLS - 1
            elif cube.x == COLS - 1 and self.moves[i][0] == 1:  # snake moves from max column to right, enter game left
                cube.x = 0
            elif cube.y == 0 and self.moves[i][1] == -1:  # snake moves from top row to above, enter game last row
                cube.y = ROWS - 1
            elif cube.y == ROWS - 1 and self.moves[i][1] == 1:  # snake moves from last row down, enter game top row
                cube.y = 1
            else:
                cube.x += self.moves[i][0]
                cube.y += self.moves[i][1]
                if i == len(self.moves):
                    self.moves.pop(i + 1)


class Player1(Snake):
    def __init__(self):
        super().__init__()
        self.color = COLORS['BLUE']
        self.head = Cube(10, 10)
        self.body.append(self.head)


class Player2(Snake):
    def __init__(self):
        super().__init__()
        self.color = COLORS['YELLOW']
        self.head = Cube(20, 20)
        self.body.append(self.head)


class Cube:
    def __init__(self, x, y, color=COLORS['WHITE']):
        self.x = x  # x position in the game 'grid'
        self.y = y  # y position in the game 'grid'
        self.color = color
