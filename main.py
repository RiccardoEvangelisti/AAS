from typing import Type
import pygame
import numpy as np

from HasMovement import HasMovement

from Agent import Agent, HasAttack, HasHP, Player
from DnDEnvironment import DnDEnvironment


class State:
    def update_agents_coord(self, agents: list[Agent]):
        self.agents_coordinates = np.array([agent.coordinates for agent in agents]).ravel()

    def update_current_hp(self, agent: HasHP):
        self.current_hp = agent.current_hp

    def update_damage_dealt(self, agents: list[HasHP]):
        self.damage_dealt = np.array([agent.max_hp - agent.current_hp for agent in agents]).ravel()

    def update_attack_available(self, agent: HasAttack):
        self.attack_available = 1 if agent.is_attack_available() else 0

    def update_movement_available(self, agent: HasMovement):
        self.movement_remaining = agent.movement_left

    def to_array(self):
        return np.array([self.agents_coordinates, self.current_hp, self.attack_available, self.movement_remaining])


######################################


def main():
    env = DnDEnvironment(n_squares_width=6, n_squares_height=5, _RENDER_MODE="human")

    player = Player("Erik combat pose-token.png")
    monster = Agent("mimic-token.png")

    env.place_agent(player, "top_left")
    env.place_agent(monster, "random")

    print(f"\nGrid:\n{env.grid.transpose()}")

    print(player.available_actions(env))

    env.startCombat()

    state = State()
    state.update_agents_coord([player, monster])

    print()

    num_episodes = 1000

    pygame.time.wait(1500)
    pygame.quit()


if __name__ == "__main__":
    main()
