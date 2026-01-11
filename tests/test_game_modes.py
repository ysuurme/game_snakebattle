import unittest
import pygame
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.game import Game
from constants import WIDTH, HEIGHT

# Mock Pygame
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))

class TestGameModes(unittest.TestCase):
    def test_single_player_mode(self):
        print("Testing Single Player Mode...")
        win = pygame.Surface((WIDTH, HEIGHT))
        game = Game(win, mode="Single")
        
        # Verify player1 exists, player2 does not
        self.assertIsNotNone(game.player1)
        self.assertIsNone(game.player2)
        
        # Simulate 10 frames
        for _ in range(10):
            game.update()
        print("Single Player Mode OK")

    def test_pvp_mode(self):
        print("Testing PvP Mode...")
        win = pygame.Surface((WIDTH, HEIGHT))
        game = Game(win, mode="PvP")
        
        # Verify both players exist
        self.assertIsNotNone(game.player1)
        self.assertIsNotNone(game.player2)
        
        # Simulate 10 frames
        for _ in range(10):
            game.update()
        print("PvP Mode OK")

if __name__ == '__main__':
    unittest.main()
