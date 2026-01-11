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
        def save_callback():
            agent.model.save()
            print("Model saved manually!")
            
        reward, done, score = game.play_step(final_move, on_save_callback=save_callback)
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

def start_pv_agent(win):
    from src.ai.agent import Agent
    import os
    
    # Check if model exists
    if not os.path.exists('./models/model.pth'):
        print("No trained model found! Please train the agent first.")
        return

    game = Game(win, mode="PvP") # PvP mode ensures Player 2 exists
    agent = Agent()
    agent.load_model()
    
    clock = pygame.time.Clock()
    
    while not game.game_over:
        pygame.time.delay(50) # Same delay as standard run
        clock.tick(10) # Same FPS as standard run
        
        # Handle Events
        game.handle_events()
        
        # 1. P1 Input (Human - WASD)
        # We pass None for P2 so input_handler ignores Arrow keys (which would otherwise control P2)
        game.input_handler.handle_input(game.player1, None)
        
        # 2. P2 Input (Agent)
        state = agent.get_state(game, game.player2)
        action = agent.get_action(state)
        new_dir = game.get_move_from_action(action, game.player2.dir)
        game.player2.dir = new_dir
        
        # 3. Update Logic
        game.move_snakes()
        game.handle_snack()
        
        # 4. Draw
        game.update_ui()
        
    pygame.time.delay(3000)

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake Battle!')

    menu = Menu(win)
    menu.add_item("Player vs Player", lambda: start_pvp(win))
    menu.add_item("Single Player", lambda: start_single(win))
    menu.add_item("Player vs Agent", lambda: start_pv_agent(win))
    menu.add_item("Agent Training", lambda: start_pvai(win))
    menu.add_item("Exit", lambda: sys.exit())
    
    menu.run()

if __name__ == '__main__':
    main()
