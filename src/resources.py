import pygame
from constants import (
    WIDTH, HEIGHT, SQ_SIZE,
    IMAGE_BACKGROUND_PATH, IMAGE_SNACK_PATH,
    SOUND_MUNCH_PATH, SOUND_HIT_PATH
)

# Initialize modules if not already initialized
if not pygame.get_init():
    pygame.init()
if not pygame.font.get_init():
    pygame.font.init()
if not pygame.mixer.get_init():
    pygame.mixer.init()

def load_image(path, size=None):
    """Loads an image from the given path and optionally scales it."""
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Error loading image at {path}: {e}")
        # In a real app, we might return a placeholder or handle this gracefully
        raise SystemExit(e)

def load_sound(path):
    """Loads a sound file from the given path."""
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound at {path}: {e}")
        raise SystemExit(e)

# Initialize Resources
# Note: These are loaded at import time to maintain compatibility 
# with the previous architecture, but typically we'd load these in a Game.init() method.

BACKGROUND = load_image(IMAGE_BACKGROUND_PATH, (WIDTH, HEIGHT))
SNACK_IMAGE = load_image(IMAGE_SNACK_PATH, (SQ_SIZE, SQ_SIZE))

SOUND_MUNCH = load_sound(SOUND_MUNCH_PATH)
SOUND_HIT = load_sound(SOUND_HIT_PATH)

# Fonts
# Re-declaring fonts here or in constants? 
# Config had them. They depend on pygame.font being initialized.
# Constants.py is pure data. Resources.py is for objects.
FONT_SCORE = pygame.font.SysFont('comicsans', 40)
FONT_WINNER = pygame.font.SysFont('comicsans', 60)
