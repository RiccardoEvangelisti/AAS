import random
from typing import Any
from State import State
from algorithms.Algorithm import Algorithm
from combat_actions.CombatActions import CombatAction


@staticmethod
def epsilon_greedy(state: State, available_actions: list[CombatAction], epsilon, algorithm: Algorithm) -> CombatAction:
    # Explore
    if random.random() < epsilon:
        return random.choice(available_actions)

    # Exploit
    return algorithm.exploit_best_action(state, available_actions)
