from abc import ABC, abstractmethod

import pygame
from CombatActions import CombatAction
from HasMovement import HasMovement
from HasAttack import HasAttack
from HasEndTurn import HasEndTurn


class Agent:
    def __init__(self, image_path: str, max_hp: int, RENDER_MODE="human"):
        RENDER_MODE = RENDER_MODE

        self.id: int
        self.coordinates: tuple[int, int]
        self.default_coordinates: tuple[int, int]

        self.max_hp = max_hp
        self.current_hp = max_hp
        self.combatActions = {}  # action.name, action

        if RENDER_MODE == "human":
            self.image_obj = pygame.image.load(image_path)

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def took_damage(self, damage: int):
        self.current_hp -= damage

    def reset_maxHP(self):
        self.current_hp = self.max_hp

    def available_actions(self, grid, n_squares_height, n_squares_width) -> list[CombatAction]:
        available_actions: list[CombatAction] = []
        for _, combat_action in self.combatActions.items():
            if combat_action.is_available(self, self.coordinates, grid, n_squares_height, n_squares_width):
                available_actions.append(combat_action)
        return available_actions


########################################################


class Player(Agent, HasEndTurn, HasMovement, HasAttack):
    def __init__(
        self,
        image_path: str,
        max_hp: int = 50,
        movement_speed: int = 30,
        attack_damage: int = 5,
        attacks_max_number: int = 1,
    ):
        Agent.__init__(self, image_path, max_hp)

        action = self.get_combat_action_EndTurn()
        self.combatActions[action.name] = action

        self.movement_speed = movement_speed
        self.movement_left = self._movement_speed
        action = self.get_combat_action_Movements()
        for a in action:
            self.combatActions[a.name] = a

        self.attacks_left = attacks_max_number
        self.attacks_max_number = attacks_max_number
        action = self.get_combat_action_MeleeAttack(attack_damage)
        self.combatActions[action.name] = action


#############################################


class Monster(Agent, HasEndTurn):
    def __init__(
        self,
        image_path: str,
        max_hp: int = 100,
    ):
        Agent.__init__(self, image_path, max_hp)

        action = self.get_combat_action_EndTurn()
        self.combatActions[action.name] = action
