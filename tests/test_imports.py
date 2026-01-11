import sys
import os
import unittest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestImports(unittest.TestCase):
    def test_constants_imports(self):
        try:
            from constants import COLORS, COLOR_P1, COLOR_P2, P1_START_POS, P2_START_POS
            from constants import MAX_MEMORY, BATCH_SIZE, LR
        except ImportError as e:
            self.fail(f"Failed to import from constants: {e}")

    def test_snake_imports(self):
        try:
            from src.snake import Player1, Player2, Snake, Cube
        except ImportError as e:
            self.fail(f"Failed to import from src.snake: {e}")

    def test_game_imports(self):
        try:
            from src.game import Game
        except ImportError as e:
            self.fail(f"Failed to import from src.game: {e}")

    def test_ai_imports(self):
        try:
            from src.ai.agent import Agent
            from src.ai.model import Linear_QNet
            from src.ai.trainer import QTrainer
            from src.ai.helper import plot
        except ImportError as e:
            self.fail(f"Failed to import from src.ai: {e}")

if __name__ == '__main__':
    unittest.main()
