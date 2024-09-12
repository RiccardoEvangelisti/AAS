from State import State
from algorithms.Algorithm import Algorithm
from combat_actions.CombatActions import CombatAction


class Random(Algorithm):

    def __init__(self, config):
        Algorithm.__init__(self, config.EPSILON, config.EPSILON_rateDecay)

    def exploit_best_action(self, state: State, available_actions: list[CombatAction]) -> CombatAction:
        raise Exception("Random algorithm does not implement exploit_best_action method")

    def learn(self, state, action, reward, next_state, done, **kwargs):
        pass

    def save_value_function(self, pickle_filename):
        pass
