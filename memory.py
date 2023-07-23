from collections import deque
import random
import numpy as np

class Memory():
    def __init__(self,max_len):
        self.max_len = max_len
        self.frames = deque(maxlen = max_len)
        self.actions = deque(maxlen = max_len)
        self.rewards = deque(maxlen = max_len)
        self.dones = deque(maxlen = max_len)

    def add_experience(self,next_frame, next_frames_reward, next_action, next_frame_terminal):        
        self.frames.append(next_frame)
        self.actions.append(next_action)
        self.rewards.append(next_frames_reward)
        self.dones.append(next_frame_terminal)

    def getlastState(self):
        index = len(self.frames)
        state = np.concatenate((self.frames[index -4],
                                self.frames[index -3],
                                self.frames[index -2],
                                self.frames[index-1]))

        return state

    def sample(self,length):
        index = random.randint(4,len(self.frames)-4)
        states = []
        next_states = []
        actions = []
        rewards = []
        dones = []

        
        while length:
            # amend numby arrays 
            state = np.concatenate((self.frames[index -3],
                      self.frames[index -2],
                      self.frames[index -1],
                      self.frames[index]))
            
            next_state = np.concatenate((self.frames[index -2],
                      self.frames[index -1],
                      self.frames[index ],
                      self.frames[index + 1]))
            
            states.append(state)
            next_states.append(next_state)
            actions.append(self.actions[index])
            rewards.append(self.rewards[index+1])
            dones.append(self.dones[index+1])
            length -= 1
        
        states = np.array(states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        next_states = np.array(next_states)
        dones = np.array(dones)

        return states, actions, rewards, next_states, dones