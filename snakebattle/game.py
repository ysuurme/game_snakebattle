import pygame
import random

from .config import QUIT, BACKGROUND, COLS, ROWS, WIDTH, HEIGHT, SQ_SIZE, COLORS, FONT_SCORE, FONT_WINNER,\
    SOUND_MUNCH, SOUND_HIT
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
            if i == 0:  # first cube in body is snake head
                    
                tongue_size = SQ_SIZE / 3
                tongue_pos = SQ_SIZE / 2 - tongue_size / 2
                eye_size = 4

                x = snake.head.x * SQ_SIZE
                y = snake.head.y * SQ_SIZE

                eyeh1 = (x + SQ_SIZE * (1 / 3) - eye_size / 3, y + SQ_SIZE / 2)  # horizontal eye
                eyeh2 = (x + SQ_SIZE * (2 / 3) + eye_size / 3, y + SQ_SIZE / 2)  # horizontal eye

                eyev1 = (x + SQ_SIZE / 2, y + SQ_SIZE * (1 / 3) - eye_size / 3)  # vertical eye
                eyev2 = (x + SQ_SIZE / 2, y + SQ_SIZE * (2 / 3) + eye_size / 3)  # vertical eye
                eye1, eye2 = eyeh1, eyeh2

                if snake.dir == (0, 0):  # start
                    x += tongue_pos
                    y -= tongue_size - 2
                elif snake.dir == (0, -1):  # up
                    x += tongue_pos
                    y -= tongue_size - 2
                    eye1, eye2 = eyeh1, eyeh2
                elif snake.dir == (0, 1):  # down
                    x += tongue_pos
                    y += SQ_SIZE - 1
                    eye1, eye2 = eyeh1, eyeh2
                elif snake.dir == (-1, 0):  # left
                    x -= tongue_size - 2
                    y += tongue_pos
                    eye1, eye2 = eyev1, eyev2
                elif snake.dir == (1, 0):  # right
                    x += SQ_SIZE - 1
                    y += tongue_pos
                    eye1, eye2 = eyev1, eyev2

                pygame.draw.circle(self.win, COLORS['BLACK'], eye1, eye_size)
                pygame.draw.circle(self.win, COLORS['BLACK'], eye2, eye_size)

                tongue = pygame.Rect(x, y, tongue_size, tongue_size)
                pygame.draw.rect(self.win, COLORS['RED'], tongue)

    def draw_snack(self):
        self.win.blit(self.snack.image, (self.snack.x * SQ_SIZE, self.snack.y * SQ_SIZE, SQ_SIZE - 2, SQ_SIZE - 2))

    def move_snake(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]:  # Quit game
            pygame.event.post(pygame.event.Event(QUIT))

        if keys_pressed[pygame.K_LEFT]:  # P1 left
            if self.player1.dir != (1, 0) or len(self.player1.body) == 1:
                self.player1.dir = (-1, 0)
        elif keys_pressed[pygame.K_UP]:  # P1 up
            if self.player1.dir != (0, 1) or len(self.player1.body) == 1:
                self.player1.dir = (0, -1)
        elif keys_pressed[pygame.K_RIGHT]:  # P1 right
            if self.player1.dir != (-1, 0) or len(self.player1.body) == 1:
                self.player1.dir = (1, 0)
        elif keys_pressed[pygame.K_DOWN]:  # P1 down
            if self.player1.dir != (0, -1) or len(self.player1.body) == 1:
                self.player1.dir = (0, 1)

        if keys_pressed[pygame.K_a]:  # P2 left
            if self.player2.dir != (1, 0) or len(self.player2.body) == 1:
                self.player2.dir = (-1, 0)
        elif keys_pressed[pygame.K_w]:  # P2 up
            if self.player2.dir != (0, 1) or len(self.player2.body) == 1:
                self.player2.dir = (0, -1)
        elif keys_pressed[pygame.K_d]:  # P2 right
            if self.player2.dir != (-1, 0) or len(self.player2.body) == 1:
                self.player2.dir = (1, 0)
        elif keys_pressed[pygame.K_s]:  # P2 down
            if self.player2.dir != (0, -1) or len(self.player2.body) == 1:
                self.player2.dir = (0, 1)

        if not self.player1.move_snake_body():  # P1 move snake, if can't move P1 hit itself, P2 wins!
            self.winner(self.player2)
        elif not self.player2.move_snake_body():  # P2 move snake, if can't move P2 hit itself, P1 wins!
            self.winner(self.player1)
        else:
            self.winner()  # Check if a player hits another player

    def init_snack(self):
        x, y = 0, 0
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
        munch = False
        if self.player1.head.x == self.snack.x and self.player1.head.y == self.snack.y:
            self.player1.length += 1
            munch = True
        elif self.player2.head.x == self.snack.x and self.player2.head.y == self.snack.y:
            self.player2.length += 1
            munch = True
        if munch:
            SOUND_MUNCH.play()
            self.init_snack()

    def winner(self, winner=None):
        winner_text = FONT_WINNER.render("Game completed!", 1, COLORS['WHITE'])
        if winner == self.player1:
            winner_text = FONT_WINNER.render("Player 1 has won the game!", 1, self.player1.color)
            self.game_over = True
        if winner == self.player2:
            winner_text = FONT_WINNER.render("Player 2 has won the game!", 1, self.player2.color)
            self.game_over = True

        for part in self.player2.body:  # validate if snake head P1 is not in body P2
            if self.player1.head.x == part.x and self.player1.head.y == part.y:
                winner_text = FONT_WINNER.render("Player 2 has won the game!", 1, self.player2.color)
                self.game_over = True
                break

        for part in self.player1.body:  # validate if snake head P2 is not in body P1
            if self.player2.head.x == part.x and self.player2.head.y == part.y:
                winner_text = FONT_WINNER.render("Player 1 has won the game!", 1, self.player1.color)
                self.game_over = True
                break

        if self.game_over:
            SOUND_HIT.play()
            self.win.blit(winner_text,
                          (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
