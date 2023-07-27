#!/home/condagpu/miniconda3/envs/py39/bin/python
from game import Game
from agent import DQNAgent
import numpy as np
import tensorflow as tf
game = Game()

agent = DQNAgent(game.observation_shape,game.n_actions)

for i in range(4):
        obs = game.reset()
        done = 0
        reward = 0
        action = 0
        agent.replay_memory.add_experience(obs,reward,action,done)

# agent.loadPreTrainedModel()

while not done:
       
        cv2 = game.render(Manual=True)
        print(agent.replay_memory.frames[-1])