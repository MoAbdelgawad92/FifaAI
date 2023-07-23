#!/home/condagpu/miniconda3/envs/py39/bin/python
from game import Game
from agent import DQNAgent
import numpy as np
import tensorflow as tf
game = Game()

agent = DQNAgent(game.observation_shape,game.n_actions)
rewards = [0,0]
# agent.loadPreTrainedModel()

for i in range(4):
        obs = game.reset()
        done = 0
        reward = 0
        action = 0
        agent.replay_memory.add_experience(obs,reward,action,done)

for episode in range(600):
    obs = game.reset()
    done = 0
    reward = 0
    action = 0
    for step in range(500):
        agent.epsilon = max(1 - episode / 500, 0.01)
        obs, reward, done, info = agent.play_one_step(game)

        if done:
            break
        if episode > 50:
            agent.training_step()
    
    
    if reward > max(rewards):
        agent.model.save_weights("weightfortest.h5",overwrite=True,save_format="h5")

    rewards.append(reward)
        
    print(f"\rEpisode: {episode}, Steps: {step + 1}, reward: {reward}", end="")
    







