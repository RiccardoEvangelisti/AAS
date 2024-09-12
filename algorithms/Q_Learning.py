import os
import pickle
import random
from State import State
from algorithms.Algorithm import Algorithm
from combat_actions.CombatActions import CombatAction


class Q_Learning(Algorithm):

    # q_dict
    @property
    def q_dict(self):
        return self.__q_dict

    @q_dict.setter
    def q_dict(self, value: dict[bytes, dict[str, float]]):
        """Dictionary to store Q-values: {state.to_bytes(): {action.name: q_value}}"""
        self.__q_dict = value

    # Constructor
    def __init__(self, config):
        Algorithm.__init__(self, config.EPSILON, config.EPSILON_rateDecay)
        
        self.ALPHA = config.ALPHA  # Learning rate
        self.GAMMA = config.GAMMA  # Discount factor
        self.pickle_filename = config.pickle_filename

        # Load value-function from file, if it exists
        if os.path.exists(self.pickle_filename):
            with open(self.pickle_filename, "rb") as f:
                self.q_dict = pickle.load(f)
        else:
            self.q_dict = {}

    ##############################################
    def exploit_best_action(self, state: State, available_actions: list[CombatAction]) -> CombatAction:

        # Take action-value pairs that match the current state
        action_values = self.q_dict.get(state.to_bytes(), {})

        # Filter to keep only actions that are available
        action_values = {
            action.name: action_values[action.name] for action in available_actions if action.name in action_values
        }

        # If there are no matching state-action pairs, return a random action
        if not action_values:
            return random.choice(available_actions)

        # Get the highest q-value
        max_q_value = max(action_values.values())
        # Get actions with the highest q-value
        best_actions = [action for action in available_actions if action_values.get(action.name) == max_q_value]
        # Return a random action from the list of actions with the highest q-value
        return random.choice(best_actions)

    ##############################################
    def learn(self, state, action, reward, next_state, done, **kwargs):

        # Get the dictionary of q-values for the current state
        state_q_values = self.q_dict.get(state.to_bytes(), {})

        # Get current value of Q(s, a) (if not exist, default to 0)
        q_value_current = state_q_values.get(action.name, 0)

        # Get q-values for the next state
        next_state_q_values = self.q_dict.get(next_state.to_bytes(), {})

        # Get the highest q-value for the next_state (if not exist, default to 0)
        max_q_value_next = max(next_state_q_values.values(), default=0)

        # Update the Q-value for the current state-action pair
        state_q_values[action.name] = q_value_current + self.ALPHA * (
            reward + self.GAMMA * max_q_value_next - q_value_current
        )

        # Save the updated state-action q-values back to the q_dict
        self.q_dict[state.to_bytes()] = state_q_values

    ##############################################
    def save_value_function(self, pickle_filename):
        with open(pickle_filename, "wb") as f:
            pickle.dump(self.q_dict, f)
