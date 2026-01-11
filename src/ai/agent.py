import torch
import random
import numpy as np
from collections import deque
from src.game import Game
from src.ai.model import Linear_QNet
from src.ai.trainer import QTrainer
from constants import MAX_MEMORY, BATCH_SIZE, LR
from src.snake import Player1, Player2

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game, player=None):
        if player is None:
            player = game.player1
            
        head = player.head
        point_l = (head.x - 1, head.y)
        point_r = (head.x + 1, head.y)
        point_u = (head.x, head.y - 1)
        point_d = (head.x, head.y + 1)
        
        dir_l = player.dir == (-1, 0)
        dir_r = player.dir == (1, 0)
        dir_u = player.dir == (0, -1)
        dir_d = player.dir == (0, 1)

        # Temporary objects for collision check
        # We assume game.is_collision works with objects having x, y
        # Also need to exclude the head itself if logic is strict, but is_collision checks bodies.
        
        Obj = type('Obj', (object,), {})
        def pt(coords):
            o = Obj()
            o.x, o.y = coords
            return o

        state = [
            # Danger straight
            (dir_r and game.is_collision(pt(point_r), exclude_body=head)) or 
            (dir_l and game.is_collision(pt(point_l), exclude_body=head)) or 
            (dir_u and game.is_collision(pt(point_u), exclude_body=head)) or 
            (dir_d and game.is_collision(pt(point_d), exclude_body=head)),

            # Danger right
            (dir_u and game.is_collision(pt(point_r), exclude_body=head)) or 
            (dir_d and game.is_collision(pt(point_l), exclude_body=head)) or 
            (dir_l and game.is_collision(pt(point_u), exclude_body=head)) or 
            (dir_r and game.is_collision(pt(point_d), exclude_body=head)),

            # Danger left
            (dir_d and game.is_collision(pt(point_r), exclude_body=head)) or 
            (dir_u and game.is_collision(pt(point_l), exclude_body=head)) or 
            (dir_r and game.is_collision(pt(point_u), exclude_body=head)) or 
            (dir_l and game.is_collision(pt(point_d), exclude_body=head)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.snack.x < head.x,  # food left
            game.snack.x > head.x,  # food right
            game.snack.y < head.y,  # food up
            game.snack.y > head.y  # food down
            ]

        return np.array(state, dtype=int)
    
    def load_model(self, file_name='model.pth'):
        self.model.load_state_dict(torch.load(f'./models/{file_name}'))
        self.model.eval()

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
