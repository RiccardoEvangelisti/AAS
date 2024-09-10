import os
import pickle
import tensorflow
from State import State
from algorithms.Algorithm import Algorithm
from combat_actions.CombatActions import CombatAction

import numpy as np
import keras
from keras import layers, models, losses
from keras.src import optimizers
from collections import deque
import random


class DQN(Algorithm):

    def __init__(self, config, all_actions: list[str], num_states):

        self.pickle_filename = config.pickle_filename

        self.all_actions = {actionName: index for index, actionName in enumerate(all_actions)}

        self.num_states = num_states
        self.num_actions = len(all_actions)
        self.gamma = config.GAMMA
        self.learning_rate = config.ALPHA
        self.epsilon = config.EPSILON
        self.epsilon_decay = config.EPSILON_rateDecay
        self.minibatch_size = config.minibatch_size
        self.target_update_freq = config.target_update_freq

        # Initialize the Q-network and the target Q-network
        self.q_network, self.target_q_network = self.create_q_network(), self.create_q_network()
        # Load Q-network weights from file, if it exists
        if os.path.exists(self.pickle_filename):
            with open(self.pickle_filename, "rb") as f:
                weights = pickle.load(f)
                self.q_network.set_weights(weights)
        # Set the target-Q-network weights to the Q-network weights
        self.target_q_network.set_weights(self.q_network.get_weights())

        # Initialize the replay buffer. "deque" simulates a buffer (it removes the oldest element when it's full)
        self.replay_buffer = deque(maxlen=config.replay_buffer_size)

        self.step_counter = 0  # for the target network update

    ##############################################
    def create_q_network(self):
        model = models.Sequential(
            [
                layers.Input(shape=(self.num_states,)),
                layers.Dense(64, activation="relu"),
                layers.Dense(self.num_actions),
            ]
        )
        model.compile(optimizer=optimizers.Adam(learning_rate=self.learning_rate), loss=losses.MeanSquaredError())  # type: ignore
        return model

    ##############################################
    def exploit_best_action(self, state: State, available_actions: list[CombatAction]) -> CombatAction:
        # Get q-values for all actions in the current state, from the Q-network
        q_values = self.q_network.predict(np.expand_dims(state.to_array(), axis=0), verbose=0)  # type: ignore # fed a batch of only one state
        q_values = q_values[0]  # get the first (and only) element (since the batch contains only one state)

        # Filter to keep only actions that are available
        valid_actions = {}  # actionIndex, combatAction
        for available_action in available_actions:
            valid_actions[self.all_actions[available_action.name]] = available_action

        # Get q-values for the valid actions
        valid_q_values = np.array([q_values[i] for i in valid_actions.keys()])
        # Get the highest q-value
        max_q_value = np.max(valid_q_values)

        # Get actions with the highest q-value
        best_actions = [
            combatAction for actionIndex, combatAction in valid_actions.items() if q_values[actionIndex] == max_q_value
        ]

        # Return a random action from the list of actions with the highest q-value
        return random.choice(best_actions)

    ##############################################
    def learn(self, state, action, reward, next_state, done):
        # Add the experience to the replay buffer
        self.replay_buffer.append((state.to_array(), action, reward, next_state.to_array(), done))

        # Update the Q-network using a minibatch of experiences

        # Check if the replay buffer has enough experiences to sample a minibatch
        if len(self.replay_buffer) < self.minibatch_size:
            return

        # Sample the minibatch from the replay buffer
        minibatch = random.sample(self.replay_buffer, self.minibatch_size)

        states, actions, rewards, next_states, dones = zip(*minibatch)
        states = np.array(states)
        actions = np.array([self.all_actions[action.name] for action in actions])
        rewards = np.array(rewards)
        next_states = np.array(next_states)
        dones = np.array(dones)

        # Get q-values for all actions in all the next_states, from the target-Q-network
        q_values_next: np.ndarray = self.target_q_network.predict(next_states, verbose=0)  # type: ignore

        # Max Q-values for each of the next states
        max_q_values_next = np.array([np.max(q_values_next[i]) for i in range(self.minibatch_size)])

        # Get the target Q-values (the updated Q-value)
        targets = np.zeros(self.minibatch_size)
        for i in range(self.minibatch_size):
            # If episode is done, the target Q-value is the reward
            if dones[i]:
                targets[i] = rewards[i]
            # If episode is not done, the target Q-value is the reward + gamma * max Q-value of the next state
            else:
                targets[i] = rewards[i] + self.gamma * max_q_values_next[i]

        with tensorflow.GradientTape() as tape:
            # Forward pass to get the Q-values for the states (the ones before the next_states)
            q_values = self.q_network(states)

            # For each Q-values array of all actions taken in a certain state, get the Q-value for only the action taken in that state
            q_values = keras.ops.sum(q_values * keras.ops.one_hot(actions, self.num_actions), axis=1)

            # Compute the loss (the mean squared error between the target-Q-values and the Q-values)
            loss = keras.ops.mean(keras.ops.square(keras.ops.subtract(targets, q_values)))

        # Backpropagation
        grads = tape.gradient(loss, self.q_network.trainable_variables)
        self.q_network.optimizer.apply_gradients(zip(grads, self.q_network.trainable_variables))  # type: ignore

        # Update the target-Q-network
        self.step_counter += 1
        if self.step_counter == self.target_update_freq:
            self.target_q_network.set_weights(self.q_network.get_weights())
            self.step_counter = 0

    ##############################################
    def save_value_function(self, pickle_filename):
        with open(pickle_filename, "wb") as f:
            pickle.dump(self.q_network.get_weights(), f)
