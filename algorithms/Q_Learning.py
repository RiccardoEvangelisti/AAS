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
    def q_dict(self, value: dict[tuple[bytes, str], float]):
        """Dictionary to store Q-values: {(state.to_bytes(), action.name): q_value}"""
        self.__q_dict = value

    # Constructor
    def __init__(self, config):
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

        # Take action-value pairs that match the current state and in available actions
        q_filtered = {
            _action_str: _value
            for (_state, _action_str), _value in self.q_dict.items()
            if _state == state.to_bytes() and any(action.name == _action_str for action in available_actions)
        }

        # If there are no matching state-action pairs, return a random action
        if not q_filtered:
            return random.choice(available_actions)

        # Get the highest q-value
        max_q_value = max(q_filtered.values())
        # Get actions with the highest q-value
        best_actions = [action for action in available_actions if q_filtered.get(action.name) == max_q_value]
        # Return a random action from the list of actions with the highest q-value
        return random.choice(best_actions)

    ##############################################
    def learn(self, state, action, reward, next_state):
        # Get current value of Q(s, a) (if not exist, default to 0)
        q_value_current = self.q_dict.get((state.to_bytes(), action), 0)

        # Take the state-action pairs that match the next_state
        q_filtered = {(state, _): value for (state, _), value in self.q_dict.items() if state == next_state.to_bytes()}
        # Get the highest q-value for the next_state (if not exist, default to 0)
        max_q_value_next = max(q_filtered.values()) if q_filtered else 0

        # Update the Q-value for the current state-action pair
        self.q_dict[(state.to_bytes(), action.name)] = q_value_current + self.ALPHA * (
            reward + self.GAMMA * max_q_value_next - q_value_current
        )

    ##############################################
    def save_value_function(self, pickle_filename):
        with open(pickle_filename, "wb") as f:
            pickle.dump(self.q_dict, f)
