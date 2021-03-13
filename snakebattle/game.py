import pygame

from .config import QUIT, BACKGROUND, COLS, ROWS, WIDTH, HEIGHT, SQ_SIZE, COLORS
from .snake import Player1, Player2


class Game:
    def __init__(self, win):
        self.win = win
        self.game_over = False
        self.player1 = None
        self.player2 = None
        self.init_players()

    def update(self):
        self.win.blit(BACKGROUND, (0, 0))
        self.draw_game()
        self.draw_snake(self.player1)
        # self.winner()
        pygame.display.update()

    def draw_game(self):
        x = 0
        y = 0
        for i in range(COLS):
            x = x + SQ_SIZE
            pygame.draw.line(self.win, COLORS['WHITE'], (x, 0), (x, HEIGHT))
        for i in range(ROWS):
            y = y + SQ_SIZE
            pygame.draw.line(self.win, COLORS['WHITE'], (0, y), (WIDTH, y))
        # p1_score = FONT_HEALTH.render(f"P1 Health: {self.player1.health}", 1, COLORS['GREEN'])
        # p2_score = FONT_HEALTH.render(f"P2 Health: {self.player2.health}", 1, COLORS['YELLOW'])

    def draw_snake(self, snake):
        for i, cube in enumerate(snake.body):
            if i == 0:
                snake.head = cube  # draws the head of the snake
                center = SQ_SIZE // 2
                radius = 3
                eye1 = (snake.head.x * SQ_SIZE + center - radius, snake.head.y * SQ_SIZE + 8)
                eye2 = (snake.head.x * SQ_SIZE + SQ_SIZE - radius * 2, snake.head.y * SQ_SIZE + 8)
                pygame.draw.circle(self.win, COLORS['BLACK'], eye1, radius)
                pygame.draw.circle(self.win, COLORS['BLACK'], eye2, radius)
            pygame.draw.rect(self.win, snake.color,
                             (cube.x * SQ_SIZE + 1, cube.y * SQ_SIZE + 1, SQ_SIZE - 2, SQ_SIZE - 2))

    def init_players(self):
        self.player1 = Player1()
        # self.player2 = Player2(800, 250)

    def move(self, keys_pressed):
        if keys_pressed[pygame.K_ESCAPE]:  # Quit game
            pygame.event.post(pygame.event.Event(QUIT))
        elif keys_pressed[pygame.K_LEFT]:  # P1 left
            self.player1.moves.insert(0, (-1, 0))

        elif keys_pressed[pygame.K_UP]:  # P1 up
            self.player1.moves.insert(0, (0, -1))

        elif keys_pressed[pygame.K_RIGHT]:  # P1 right
            self.player1.moves.insert(0, (1, 0))

        elif keys_pressed[pygame.K_DOWN]:  # P1 down
            self.player1.moves.insert(0, (0, 1))

        self.player1.move_snake()  # move snake

    def shoot(self, player):
        if player.ammo >= 0:
            player.ammo -= 1
            bullet = Bullet(player)  # Create bullet
            SOUND_BLT_FIRE.play()
            self.bullets.append(bullet)
        else:
            print(f'Player: {type(player).__name__} is out of ammo!')

    def handle_bullets(self):
        for b in self.bullets:
            b.shape.move_ip(b.BLT_SPEED, 0)
            if self.player1.hull.colliderect(b.shape):
                pygame.event.post(pygame.event.Event(P1_HIT))
                self.bullets.remove(b)
            elif self.player2.hull.colliderect(b.shape):
                pygame.event.post(pygame.event.Event(P2_HIT))
                self.bullets.remove(b)
            elif b.x < 0:
                self.bullets.remove(b)
            elif b.x > WIDTH:
                self.bullets.remove(b)

    def draw_bullets(self):
        for b in self.bullets:
            if b.player == 'Player1':
                color = COLORS['GREEN']
            elif b.player == 'Player2':
                color = COLORS['YELLOW']
            else:
                color = COLORS['WHITE']
            pygame.draw.rect(self.win, color, b.shape)

    def reload(self):  # todo limit bullet spamming
        if self.player1.ammo < MAX_BLTS:
            self.player1.ammo += 1
        if self.player2.ammo < MAX_BLTS:
            self.player2.ammo += 1

    def blit_spaceships(self):
        self.win.blit(self.player1.spaceship, (self.player1.hull.x, self.player1.hull.y))
        self.win.blit(self.player2.spaceship, (self.player2.hull.x, self.player2.hull.y))

    def winner(self):
        winner_text = ""
        if self.player1.health <= 0:
            winner_text = FONT_WINNER.render("Player 2 has won the game!", 1, COLORS['YELLOW'])
            self.game_over = True
        elif self.player2.health <= 0:
            winner_text = FONT_WINNER.render("Player 1 has won the game!", 1, COLORS['GREEN'])
            self.game_over = True
        if self.game_over:
            self.win.blit(winner_text,
                          (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
