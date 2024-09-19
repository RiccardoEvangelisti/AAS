import os
import pickle
import tensorflow
from DnDEnvironment import DnDEnvironment
from State import State
from algorithms.Algorithm import Algorithm
from combat_actions.CombatActions import CombatAction

from tensorflow.python.framework.ops import enable_eager_execution

import numpy as np
import tensorflow as tf
import keras
from keras import layers, models, losses
from keras.src import optimizers
from collections import deque
import random


class DQN(Algorithm):

    def __init__(self, config, all_actions: list[str], num_states):

        Algorithm.__init__(self, config.EPSILON, config.EPSILON_rateDecay)

        self.pickle_filename = config.pickle_filename + "_" + config.train_code + ".pkl"

        self.all_actions = list([actionName for actionName in all_actions])

        self.num_states = num_states
        self.num_actions = len(all_actions)
        self.gamma = config.GAMMA
        self.learning_rate = config.ALPHA
        self.minibatch_size = config.minibatch_size
        self.target_update_freq = config.target_update_freq

        # Initialize the Q-network and the target Q-network
        self.q_network, self.target_q_network = self.create_q_network(), self.create_q_network()
        # Load Q-network weights from file, if it exists
        if os.path.exists(self.pickle_filename):
            with open(self.pickle_filename, "rb") as f:
                weights = pickle.load(f)
                self.q_network.set_weights(weights)
                print("Loaded %s" % self.pickle_filename)
        # Set the target-Q-network weights to the Q-network weights
        self.target_q_network.set_weights(self.q_network.get_weights())

        # Initialize the replay buffer. "deque" simulates a buffer (it removes the oldest element when it's full)
        self.replay_buffer = deque(maxlen=config.replay_buffer_size)

        self.step_counter = 0  # for the target network update

        enable_eager_execution()
        print("Eager Execution:", tf.executing_eagerly())

    ##############################################
    def create_q_network(self):
        network = models.Sequential(
            [
                layers.Input(shape=(self.num_states,)),
                layers.Dense(128, activation="relu"),
                layers.Dense(self.num_actions),
            ]
        )
        network.compile(optimizer=optimizers.Adam(learning_rate=self.learning_rate), loss=losses.MeanSquaredError())  # type: ignore
        return network

    ##############################################
    @tf.function
    def exploit_best_action_tf(self, state, valid_action_indices):
        # Get q-values for all actions in the current state, from the Q-network
        q_values = self.q_network(tf.expand_dims(state, axis=0))  # fed a batch of only one state
        q_values = q_values[0]  # get the first (and only) element (since the batch contains only one state)

        # Get q-values for only the valid actions
        valid_q_values = tf.gather(q_values, valid_action_indices)
        # Get the first index with highest q-value (yes, only the first)
        max_q_value_index = tf.argmax(valid_q_values)

        # Return the index of the first valid action with the highest q-value
        return valid_action_indices[max_q_value_index]

    def exploit_best_action(self, state: State, available_actions: list[CombatAction]) -> CombatAction:
        state_tf = tf.convert_to_tensor(state.to_array())

        # Convert available_actions to list of action indices
        valid_action_indices = tf.constant(
            list(self.all_actions.index(av_action.name) for av_action in available_actions)
        )

        best_action_index = self.exploit_best_action_tf(state_tf, valid_action_indices)

        for av_action in available_actions:
            if av_action.name == self.all_actions[best_action_index.numpy()]:  # type: ignore
                return av_action
        raise ValueError("Action not found in available actions")

    ##############################################

    @tf.function
    def learn_tf(self):
        # Update the Q-network using a minibatch of experiences

        # Check if the replay buffer has enough experiences to sample a minibatch
        if len(self.replay_buffer) < self.minibatch_size:
            return

        # Sample the minibatch from the replay buffer
        minibatch = random.sample(self.replay_buffer, self.minibatch_size)

        states, actions, rewards, next_states, dones, valid_actions_indices_batch = zip(*minibatch)
        states = tf.convert_to_tensor(np.array(states))
        actions = tf.convert_to_tensor(np.array(actions))
        rewards = tf.convert_to_tensor(np.array(rewards), dtype=tf.float32)
        next_states = tf.convert_to_tensor(np.array(next_states))
        dones = tf.convert_to_tensor(np.array(dones))

        # Get q-values for all actions in all the next_states, from the target-Q-network
        q_values_next = self.target_q_network(next_states)

        # Max Q-value for each of the next states, filtering in only the valid actions for each state
        max_q_values_next = []
        for i in range(self.minibatch_size):
            valid_q_values_next = tf.gather(q_values_next[i], valid_actions_indices_batch[i])
            max_q_value_next = tf.reduce_max(valid_q_values_next)
            max_q_values_next.append(max_q_value_next)
        max_q_values_next = tf.stack(max_q_values_next)

        # Get the target Q-values (the updated Q-value)
        # If episode is done, the target Q-value is the reward
        # If episode is not done, the target Q-value is the reward + gamma * max Q-value of the next state
        targets = tf.where(dones, rewards, rewards + self.gamma * max_q_values_next)

        with tensorflow.GradientTape() as tape:
            # Forward pass to get the Q-values for the states (the ones before the next_states)
            q_values = self.q_network(states)
            """
            Now q_values is in the form of:
            [[q-value of all actions for state 1],
             [q-value of all actions for state 2],
             [...]]
            """

            # For each of the Q-values array of all actions taken in a certain state, keep only the Q-value for the action actually took in each state
            q_values = tf.gather(q_values, actions, batch_dims=1)

            """
            Now q_values is in the form of:
            [q-value for state 1,
             q-value for state 2,
             ...]
            """

            # Compute the loss (the MSE between the target-Q-values and the Q-values)
            loss = keras.ops.mean(keras.ops.square(keras.ops.subtract(targets, q_values)))

        # Backpropagation
        grads = tape.gradient(loss, self.q_network.trainable_variables)
        self.q_network.optimizer.apply_gradients(zip(grads, self.q_network.trainable_variables))  # type: ignore

        # Update the target-Q-network
        self.step_counter += 1
        if self.step_counter == self.target_update_freq:
            self.target_q_network.set_weights(self.q_network.get_weights())
            self.step_counter = 0

    def learn(self, state, action, reward, next_state, done, **kwargs):
        # Get the available actions for the "next state" which is now the current (because we already took the step)
        env: DnDEnvironment = kwargs.get("env")  # type: ignore
        available_actions = env.get_playing_agent().available_actions(
            env.grid, env.n_squares_height, env.n_squares_width
        )

        # Convert available_actions to list of action indices
        valid_action_indices_tf = tf.constant(
            list(self.all_actions.index(av_action.name) for av_action in available_actions)
        )

        state_tf = tf.constant(state.to_array())
        action_tf = tf.constant(self.all_actions.index(action.name))
        reward_tf = tf.constant(reward, dtype=tf.float32)
        next_state_tf = tf.constant(next_state.to_array())
        done_tf = tf.constant(done)

        # Add the experience to the replay buffer
        self.replay_buffer.append((state_tf, action_tf, reward_tf, next_state_tf, done_tf, valid_action_indices_tf))

        self.learn_tf()

    ##############################################
    def save_value_function(self, pickle_filename):
        with open(pickle_filename, "wb") as f:
            pickle.dump(self.q_network.get_weights(), f)
