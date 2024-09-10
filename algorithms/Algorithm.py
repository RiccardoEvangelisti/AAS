from abc import ABC, abstractmethod

from State import State
from combat_actions.CombatActions import CombatAction


class Algorithm(ABC):

    @abstractmethod
    def exploit_best_action(self, state: State, available_actions: list[CombatAction]) -> CombatAction:
        pass

    @abstractmethod
    def learn(self, state, action, reward, next_state, done, **kwargs):
        pass

    @abstractmethod
    def save_value_function(self, pickle_filename):
        pass
