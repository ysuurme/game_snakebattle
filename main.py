import pygame
import sys

from snakebattle.config import QUIT, WIDTH, HEIGHT, DELAY, FPS
from snakebattle.game import Game


def init_game():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Battle!')  # todo implement AI
    game = Game(win)
    return game


def run(game):
    clock = pygame.time.Clock()
    while True:
        pygame.time.delay(DELAY)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == QUIT:
                pygame.quit()
                sys.exit()

        game.update()

        if game.game_over:
            pygame.time.delay(5000)
            break

    main()


def main():  # todo implement sounds for game start, game won
    snake_battle = init_game()
    run(snake_battle)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
