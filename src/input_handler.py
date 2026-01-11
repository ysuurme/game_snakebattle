import pygame
from typing import Tuple
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
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Player 1 controls (WASD)
        if keys[pygame.K_a]:
            if player1.dir != (1, 0):
                player1.dir = (-1, 0)
        elif keys[pygame.K_d]:
            if player1.dir != (-1, 0):
                player1.dir = (1, 0)
        elif keys[pygame.K_w]:
            if player1.dir != (0, 1):
                player1.dir = (0, -1)
        elif keys[pygame.K_s]:
            if player1.dir != (0, -1):
                player1.dir = (0, 1)

        # Player 2 controls (Arrows) - Only if player2 exists
        if player2:
            if keys[pygame.K_LEFT]:
                if player2.dir != (1, 0):
                    player2.dir = (-1, 0)
            elif keys[pygame.K_RIGHT]:
                if player2.dir != (-1, 0):
                    player2.dir = (1, 0)
            elif keys[pygame.K_UP]:
                if player2.dir != (0, 1):
                    player2.dir = (0, -1)
            elif keys[pygame.K_DOWN]:
                if player2.dir != (0, -1):
                    player2.dir = (0, 1)

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

