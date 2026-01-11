import pygame

# Initialize pygame module to access standard constants if needed, 
# though we try to keep this file data-focused.
pygame.init() 

# Game Dimensions
SQ_SIZE = 25
ROWS = 25
COLS = 25
WIDTH = COLS * SQ_SIZE
HEIGHT = ROWS * SQ_SIZE
BORDER_WIDTH = 10

# Game Settings
DELAY = 50  # game delay in ms
FPS = 10    # game frames per second

# Colors
COLORS = {
    "BLACK": (0, 0, 0),
    "GREY": (128, 128, 128),
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "YELLOW": (255, 255, 0),
    "WHITE": (255, 255, 255)
}

COLOR_P1 = COLORS["BLUE"]
COLOR_P2 = COLORS["YELLOW"]

# Player Starting Positions (Grid Coordinates)
P1_START_POS = (10, 10)
P2_START_POS = (20, 20)

# Asset Paths
ASSET_DIR = "assets"
IMAGE_BACKGROUND_PATH = f"{ASSET_DIR}/snakeBackground.png"
IMAGE_SNACK_PATH = f"{ASSET_DIR}/snack.png"
SOUND_MUNCH_PATH = f"{ASSET_DIR}/snakeMunch.mp3"
SOUND_HIT_PATH = f"{ASSET_DIR}/snakeHit.mp3"

# Events
# Using a specific ID for custom quit event
QUIT = pygame.USEREVENT + 1