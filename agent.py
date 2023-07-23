import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import keras
import tensorflow as tf
import numpy as np
from memory import Memory



class DQNAgent:
    def __init__(self, input_shape, n_outputs, learning_rate=1e-2, epsilon=0, batch_size=32, discount_rate=0.95):
        self.input_shape = input_shape
        self.n_outputs = n_outputs
        self.batch_size = batch_size
        self.discount_rate = discount_rate
        self.optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
        self.loss_fn = keras.losses.mean_squared_error
        self.epsilon = epsilon
        self.model = self._build_model()
        self.replay_memory = Memory(max_len=100000)

    def _build_model(self):
        model = keras.models.Sequential([
            keras.layers.Dense(32, activation="elu", input_shape=(8,)),
            keras.layers.Dense(32, activation="elu"),
            keras.layers.Dense(self.n_outputs)
        ])
        model.summary()
        return model


    # @profile(stream=fp1)
    def epsilon_greedy_policy(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(self.n_outputs)
        else:
            Q_values = self.model.predict(state[np.newaxis], verbose=0)
            return np.argmax(Q_values[0])

    # @profile(stream=fp3)
    def play_one_step(self, env):
        state = self.replay_memory.getlastState()
        action = self.epsilon_greedy_policy(state)
        next_state, reward, done,_, info = env.step(action,state)
        self.replay_memory.add_experience(next_state,reward,action,done)
        return next_state, reward, done, info
    
    # @profile(stream=fp4)
    def training_step(self):
        experiences = self.replay_memory.sample(self.batch_size)
        states, actions, rewards, next_states, dones = experiences
        next_Q_values = self.model.predict(next_states)
        max_next_Q_values = np.max(next_Q_values, axis=1)
        target_Q_values = (rewards +
                           (1 - dones) * self.discount_rate * max_next_Q_values)
        target_Q_values = target_Q_values.reshape(-1, 1)
        mask = tf.one_hot(actions, self.n_outputs)
        with tf.GradientTape() as tape:
            all_Q_values = self.model(states)
            Q_values = tf.reduce_sum(all_Q_values * mask, axis=1, keepdims=True)
            loss = tf.reduce_mean(self.loss_fn(target_Q_values, Q_values))
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))

    def loadPreTrainedModel(self):
        self.model.load_weights("./weightfortest.h5")