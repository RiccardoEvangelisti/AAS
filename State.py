import numpy as np

from agent_interfaces.HasMovement import HasMovement

from Agent import Agent, HasAttack


class State:
    """
    x coordinate of playing agent\n
    y coordinate of playing agent\n
    x coordinate of enemy agent\n
    y coordinate of enemy agent\n
    current HP of playing agent\n
    damage dealt to enemy agent\n
    how many attack actions the playing agent has left\n
    how many movement actions the playing agent has left\n
    """

    def __init__(self, player: Agent, enemy: Agent):
        self.__update_agents_coord([player, enemy])
        self.__update_current_hp(player)
        self.__update_damage_dealt(enemy)
        self.__update_attack_available(player)
        self.__update_movement_available(player)

    def __update_agents_coord(self, agents: list[Agent]):
        """Sets the agents coordinates in the state in the order of the list"""
        self.agents_coordinates = []
        for agent in agents:
            self.agents_coordinates.append(agent.coordinates[0])
            self.agents_coordinates.append(agent.coordinates[1])

    def __update_current_hp(self, agent: Agent):
        """Sets the current hp of the agent"""
        self.current_hp = agent.current_hp

    def __update_damage_dealt(self, enemy: Agent):
        """Sets the damage dealt to the passed agent"""
        self.damage_dealt = enemy.max_hp - enemy.current_hp

    def __update_attack_available(self, agent: Agent):
        """Sets how many attacks the agent has left"""
        if isinstance(agent, HasAttack):
            self.attacks_remaining = agent.attacks_left
        else:
            self.attacks_remaining = 0

    def __update_movement_available(self, agent: Agent):
        """Sets how much movement the agent has left"""
        if isinstance(agent, HasMovement):
            self.movement_remaining = agent.movement_left
        else:
            self.movement_remaining = 0

    def to_array(self):
        """Returns the state as a numpy array in a single dimension"""
        return np.hstack(
            [
                self.agents_coordinates,
                self.current_hp,
                self.damage_dealt,
                self.attacks_remaining,
                self.movement_remaining,
            ]
        )

    def to_bytes(self):
        """Returns the state as bytes of a numpy array in a single dimension"""
        return self.to_array().tobytes()
