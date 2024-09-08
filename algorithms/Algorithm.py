from abc import ABC, abstractmethod

from combat_actions.CombatActions import CombatAction


class Algorithm(ABC):

    @abstractmethod
    def exploit_best_action(self, state, available_actions) -> CombatAction:
        pass

    @abstractmethod
    def learn(self, state, action, reward, next_state):
        pass

    @abstractmethod
    def save_value_function(self, pickle_filename):
        pass
