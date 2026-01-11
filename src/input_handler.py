import pygame
from typing import Tuple
from constants import QUIT
from src.snake import Snake

class InputHandler:
    """
    Responsible for processing raw keyboard input and converting it 
    into directional changes for the Snake entities.
    """
    def handle_input(self, player1: Snake, player2: Snake) -> None:
        keys = pygame.key.get_pressed()

        # Global Events
        if keys[pygame.K_ESCAPE]:
            pygame.event.post(pygame.event.Event(QUIT))

        # Player 1 Controls (Arrow Keys)
        self._update_direction(player1, keys, 
                               left=pygame.K_LEFT, right=pygame.K_RIGHT, 
                               up=pygame.K_UP, down=pygame.K_DOWN)

        # Player 2 Controls (WASD)
        self._update_direction(player2, keys, 
                               left=pygame.K_a, right=pygame.K_d, 
                               up=pygame.K_w, down=pygame.K_s)

    def _update_direction(self, snake: Snake, keys, left, right, up, down) -> None:
        """Helper to safely change direction preventing 180-degree turns."""
        curr_dir = snake.dir
        
        new_dir: Tuple[int, int] = curr_dir # Default direction is current direction

        if keys[left]:
            new_dir = (-1, 0)
        elif keys[right]:
            new_dir = (1, 0)
        elif keys[up]:
            new_dir = (0, -1)
        elif keys[down]:
            new_dir = (0, 1)
        
        # Apply direction, prevent 180 degree turns unless snake length is 1
        if new_dir != curr_dir:
            opposite_dir = (curr_dir[0] * -1, curr_dir[1] * -1)
            if new_dir != opposite_dir or len(snake.body) <= 1:
                snake.dir = new_dir
