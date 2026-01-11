import pygame
import random
import sys
import numpy

from constants import COLS, ROWS, WIDTH, HEIGHT, SQ_SIZE, COLORS, DELAY, FPS
from src.resources import BACKGROUND, FONT_SCORE, FONT_WINNER, SOUND_MUNCH, SOUND_HIT
from .snake import Player1, Player2
from .snack import Snack
from .input_handler import InputHandler


class Game:
    """
    Responsible for delegating keyboard input processing to the InputHandler and 
    focuses on updating the simulation of game state.
    """
    def __init__(self, win, mode="PvP"):
        self.win = win
        self.mode = mode
        self.reset()
    
    def reset(self):
        self.game_over = False
        self.player1 = None
        self.player2 = None
        self.snack = None
        self.frame_iteration = 0
        self.input_handler = InputHandler()
        self.init_players()
        self.init_snack()
        self.clock = pygame.time.Clock()
        self.score = 0

    def run(self):
        while not self.game_over:
            pygame.time.delay(DELAY)
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
        
        # Game Over Screen / Delay
        pygame.time.delay(3000)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. Collect User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # 2. Move
        self._move(action) # update head
        
        # 3. Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.player1.body):
            game_over = True
            reward = -10
            return reward, game_over, self.score
            
        # 4. Place new food or just move
        # move_snakes() does the body update, but we need to check snack first or during?
        # Re-using existing logic somewhat, but for AI we need strict order.
        # Let's adapt move_snakes logic here for AI mode or keep it separate?
        # For simplicity, let's allow _move to set direction, then use existing logic.
        
        if not self.player1.move_snake_body():
            # Collision happened during move (self hit)
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Check snack
        if self.handle_snack():
            self.score += 1
            reward = 10
            
        # 5. Update UI and Clock
        self.update_ui()
        self.clock.tick(FPS)
        
        return reward, game_over, self.score

    def update_ui(self):
        self.win.blit(BACKGROUND, (0, 0))
        self.draw_game()
        self.draw_snack()
        self.draw_snake(self.player1)
        if self.player2:
            self.draw_snake(self.player2)
        pygame.display.update()

    def update(self):
        # 1. Process Input
        if self.mode == "PvP":
            self.input_handler.handle_input(self.player1, self.player2)
        else:
             self.input_handler.handle_input(self.player1, None)

        # 2. Update Logic
        self.move_snakes()
        self.handle_snack()

        # 3. Draw Frame
        self.update_ui()

    def init_players(self):
        self.player1 = Player1()
        if self.mode == "PvP":
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
        self.win.blit(p1_score, (10, 10))
        
        if self.player2:
            p2_score = FONT_SCORE.render(f"P2 Score: {self.player2.length}", 1, self.player2.color)
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

    def move_snakes(self):
        """Handles snake movement and collision logic."""
        # Note: Input handling is now done by self.input_handler before this method is called.
        
        if not self.player1.move_snake_body():
             if self.mode == "PvP":
                 self.winner(self.player2) # P2 wins if P1 dies
             else:
                 self.winner(None) # Game over single player

        if self.player2:
            if not self.player2.move_snake_body():
                self.winner(self.player1)
            else:
                 self.winner() # Check collision between players

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
        elif self.player2 and self.player2.head.x == self.snack.x and self.player2.head.y == self.snack.y:
            self.player2.length += 1
            munch = True
        if munch:
            SOUND_MUNCH.play()
            self.init_snack()
        return munch

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.player1.head
        # hits boundary
        if pt.x > COLS-1 or pt.x < 0 or pt.y > ROWS-1 or pt.y < 0:
            return True
        # hits itself
        for body_part in self.player1.body[1:]:
            if pt.x == body_part.x and pt.y == body_part.y:
                return True
        return False

    def _move(self, action):
        # [straight, right, left]
        
        clock_wise = [(0, -1), (1, 0), (0, 1), (-1, 0)] # Up, Right, Down, Left
        
        # Current direction mapping
        curr_dir = self.player1.dir
        if curr_dir == (0,0): curr_dir = (1,0) # Default moving right if stationary
        
        try:
            idx = clock_wise.index(curr_dir)
        except ValueError:
            idx = 0

        if numpy.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif numpy.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn

        self.player1.dir = new_dir

    def winner(self, winner=None):
        winner_text = FONT_WINNER.render("Game completed!", 1, COLORS['WHITE'])
        if winner == self.player1:
            winner_text = FONT_WINNER.render("Player 1 has won the game!", 1, self.player1.color)
            self.game_over = True
        if winner == self.player2:
            winner_text = FONT_WINNER.render("Player 2 has won the game!", 1, self.player2.color)
            self.game_over = True

        if self.player2:
            for part in self.player2.body:
                if self.player1.head.x == part.x and self.player1.head.y == part.y:
                    winner_text = FONT_WINNER.render("Player 2 has won the game!", 1, self.player2.color)
                    self.game_over = True
                    break

            for part in self.player1.body:
                 if self.player2.head.x == part.x and self.player2.head.y == part.y:
                    winner_text = FONT_WINNER.render("Player 1 has won the game!", 1, self.player1.color)
                    self.game_over = True
                    break

        if self.game_over:
            SOUND_HIT.play()
            self.win.blit(winner_text,
                          (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
