import pygame
import sys
from constants import WIDTH, HEIGHT
from src.game import Game
from src.menu import Menu

def start_pvp(win):
    game = Game(win, mode="PvP")
    game.run()

def start_single(win):
    game = Game(win, mode="Single")
    game.run()

def start_pvai(win):
    from src.ai.agent import Agent
    from src.ai.helper import plot
    game = Game(win, mode="PvAI")
    agent = Agent()
    scores = []
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            
            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Battle!')

    menu = Menu(win)
    menu.add_item("Player vs Player", lambda: start_pvp(win))
    menu.add_item("Single Player", lambda: start_single(win))
    menu.add_item("Player vs AI (Train)", lambda: start_pvai(win))
    menu.add_item("Exit", lambda: sys.exit())
    
    menu.run()

if __name__ == '__main__':
    main()
