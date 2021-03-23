# Configuration file holding constant values used throughout the project.
import pygame
pygame.font.init()
pygame.mixer.init()

# pygame window:
SQ_SIZE = 25
ROWS, COLS = 30, 30
WIDTH, HEIGHT = COLS*SQ_SIZE, ROWS*SQ_SIZE
DELAY = 50  # game delay in ms, hence a higher value is a slower gameplay
FPS = 10  # game frames per second, hence a higher value is a faster gameplay
BORDER_WIDTH = 10
BORDER = pygame.Rect((WIDTH - BORDER_WIDTH) / 2, 0, BORDER_WIDTH, HEIGHT)

# pygame fonts:
FONT_SCORE = pygame.font.SysFont('comicsans', 40)
FONT_WINNER = pygame.font.SysFont('comicsans', 75)

# Game colors:
COLORS = {
    "BLACK": (0, 0, 0),
    "GREY": (128, 128, 128),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255)
}

# Game images:
BACKGROUND = pygame.transform.scale(pygame.image.load('assets/snakeBackground.png'), (WIDTH, HEIGHT))
SNACK = pygame.transform.scale(pygame.image.load('assets/snack.png'), (SQ_SIZE, SQ_SIZE))

# Game sounds:
SOUND_MUNCH = pygame.mixer.Sound('assets/snakeMunch.mp3')
SOUND_HIT = pygame.mixer.Sound('assets/snakeHit.mp3')

# Game events:
QUIT = pygame.USEREVENT + 1
