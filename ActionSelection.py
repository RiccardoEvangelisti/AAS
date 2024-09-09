import random
from typing import Any
from State import State
from algorithms.Algorithm import Algorithm
from combat_actions.CombatActions import CombatAction


class ActionSelection:
    def __init__(self, max_epsilon: float = 0, epsilon_decay_rate: float = 1):
        self.epsilon_decay_rate = epsilon_decay_rate
        self.epsilon = max_epsilon

    def epsilon_greedy(self, state: State, available_actions: list[CombatAction], algorithm: Algorithm) -> CombatAction:
        self.epsilon = self.epsilon * self.epsilon_decay_rate
        # Explore
        if random.random() < self.epsilon:
            return random.choice(available_actions)

        # Exploit
        return algorithm.exploit_best_action(state, available_actions)
