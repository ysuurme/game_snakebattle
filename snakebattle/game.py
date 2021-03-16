import pygame
import random

from .config import QUIT, BACKGROUND, COLS, ROWS, WIDTH, HEIGHT, SQ_SIZE, COLORS, FONT_SCORE, FONT_WINNER
from .snake import Player1, Player2
from .snack import Snack


class Game:
    def __init__(self, win):
        self.win = win
        self.game_over = False
        self.player1 = None
        self.player2 = None
        self.snack = None
        self.init_players()
        self.init_snack()

    def update(self):
        self.win.blit(BACKGROUND, (0, 0))
        self.draw_game()
        self.draw_snack()
        self.draw_snake(self.player1)
        self.draw_snake(self.player2)
        self.move_snake()
        self.handle_snack()
        self.winner()
        pygame.display.update()

    def init_players(self):
        self.player1 = Player1()
        self.player2 = Player2()

    def draw_game(self):
        x = 0
        y = 0
        for i in range(COLS):
            x = x + SQ_SIZE
            pygame.draw.line(self.win, COLORS['WHITE'], (x, 0), (x, HEIGHT))
        for i in range(ROWS):
            y = y + SQ_SIZE
            pygame.draw.line(self.win, COLORS['WHITE'], (0, y), (WIDTH, y))
        p1_score = FONT_SCORE.render(f"P1 Score: {self.player1.length}", 1, self.player1.color)
        p2_score = FONT_SCORE.render(f"P2 Score: {self.player2.length}", 1, self.player2.color)
        self.win.blit(p1_score, (10, 10))
        self.win.blit(p2_score, (WIDTH - p2_score.get_width() - 10, 10))

    def draw_snake(self, snake):
        for i, cube in enumerate(snake.body):
            pygame.draw.rect(self.win, snake.color,
                             (cube.x * SQ_SIZE + 1, cube.y * SQ_SIZE + 1, SQ_SIZE - 2, SQ_SIZE - 2))
            if i == 0:  # draws the head of the snake
                # self.win.blit(self.player1.spaceship, (self.player1.hull.x, self.player1.hull.y))
                center = SQ_SIZE // 2
                radius = 3
                eye1 = (snake.head.x * SQ_SIZE + center - radius, snake.head.y * SQ_SIZE + 8)
                eye2 = (snake.head.x * SQ_SIZE + SQ_SIZE - radius * 2, snake.head.y * SQ_SIZE + 8)
                pygame.draw.circle(self.win, COLORS['BLACK'], eye1, radius)
                pygame.draw.circle(self.win, COLORS['BLACK'], eye2, radius)

    def draw_snack(self):
        pygame.draw.rect(self.win, self.snack.color, (self.snack.x * SQ_SIZE + 1, self.snack.y * SQ_SIZE + 1,
                                                      SQ_SIZE - 2, SQ_SIZE - 2))

    def move_snake(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:  # Quit game
            pygame.event.post(pygame.event.Event(QUIT))

        elif keys_pressed[pygame.K_LEFT]:  # P1 left
            self.player1.dir = (-1, 0)
        elif keys_pressed[pygame.K_UP]:  # P1 up
            self.player1.dir = (0, -1)
        elif keys_pressed[pygame.K_RIGHT]:  # P1 right
            self.player1.dir = (1, 0)
        elif keys_pressed[pygame.K_DOWN]:  # P1 down
            self.player1.dir = (0, 1)

        self.player1.move_snake_body()  # move snake

    def init_snack(self):
        for cube in self.player1.body:
            while True:
                x = random.randrange(COLS)
                y = random.randrange(ROWS)
                if cube.x == x and cube.y == y:  # validates if snack is not in snake body
                    continue  # define new x, y for snack
                else:
                    break
        self.snack = Snack(x, y)

    def handle_snack(self):
        if self.player1.head.x == self.snack.x and self.player1.head.y == self.snack.y:
            self.player1.length += 1
            self.init_snack()

    def blit_spaceships(self):

        self.win.blit(self.player2.spaceship, (self.player2.hull.x, self.player2.hull.y))

    def winner(self):
        winner_text = ""
        if self.player1.head in self.player2.body:
            winner_text = FONT_WINNER.render("Player 1 has lost the game!", 1, COLORS['YELLOW'])
            self.game_over = True
        elif self.player1.head in self.player2.body:
            winner_text = FONT_WINNER.render("Player 2 has lost the game!", 1, COLORS['GREEN'])
            self.game_over = True

        if self.game_over:
            self.win.blit(winner_text,
                          (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
