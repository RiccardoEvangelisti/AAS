from DnDEnvironment import DnDEnvironment
from State import State
from agent_interfaces.HasMovement import HasMovement
from algorithms.Algorithm import Algorithm
from combat_actions.Attack import Attack
from combat_actions.CombatActions import CombatAction
from combat_actions.EndTurn import EndTurn
from combat_actions.Movement import *


class Raw(Algorithm):

    def __init__(self, config, env: DnDEnvironment):
        Algorithm.__init__(self, config.EPSILON, config.EPSILON_rateDecay)
        self.__env = env

    def exploit_best_action(self, state: State, available_actions: list[CombatAction]) -> CombatAction:
        # If an attack is available, take it
        for action in available_actions:
            if isinstance(action, Attack):
                return action

        # If an attack is not available, but it has movement left, move nearer to the enemy
        playing_agent = self.__env.get_playing_agent()
        if isinstance(playing_agent, HasMovement):
            if playing_agent.is_movement_available():
                enemy_coords = self.__env.get_not_playing_agents()[0].coordinates
                player_coords = playing_agent.coordinates
                action = None

                if enemy_coords[0] < player_coords[0]:
                    if enemy_coords[1] < player_coords[1]:
                        action = Movement_UP_LEFT
                    elif enemy_coords[1] > player_coords[1]:
                        action = Movement_DOWN_LEFT
                    else:
                        action = Movement_LEFT

                elif enemy_coords[0] > player_coords[0]:
                    if enemy_coords[1] < player_coords[1]:
                        action = Movement_UP_RIGHT
                    elif enemy_coords[1] > player_coords[1]:
                        action = Movement_DOWN_RIGHT
                    else:
                        action = Movement_RIGHT

                elif enemy_coords[0] == player_coords[0]:
                    if enemy_coords[1] < player_coords[1]:
                        action = Movement_UP
                    elif enemy_coords[1] > player_coords[1]:
                        action = Movement_DOWN

                if action is not None:
                    for a in available_actions:
                        if a.name == action.name:
                            return a

        # If no movement is available, take EndTurn
        for a in available_actions:
            if a.name == EndTurn.name:
                return a

        raise Exception("No action available")

    def learn(self, state, action, reward, next_state, done, **kwargs):
        pass

    def save_value_function(self, pickle_filename):
        pass
