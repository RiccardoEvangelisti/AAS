from abc import ABC, abstractmethod
from enum import Enum

from CombatActions import CombatAction
from HasHP import HasHP


class Attack(CombatAction):

    def __init__(self):
        self._name = "Attack"

    @property
    def name(self):
        return self._name
    
    def is_available(self, character: HasAttack) -> bool:



class HasAttack(ABC):

    @property
    @abstractmethod
    def attack_power(self) -> int:
        pass

    @property
    @abstractmethod
    def attacks_left(self) -> int:
        pass

    @property
    @abstractmethod
    def attacks_max_number(self) -> int:
        pass

    @attack_power.setter
    def attack_power(self, value: int):
        self._attack_power = value

    @attacks_left.setter
    def attacks_left(self, value: int):
        self._attacks_left = value

    @attacks_max_number.setter
    def attacks_max_number(self, value: int):
        self._attacks_max_number = value

    def attack(self, enemy: HasHP):
        enemy.took_damage(self.attack_power)
        self._attacks_left -= 1

    def is_attack_available(self) -> bool:
        return self._attacks_left > 0

    def reset_attacks(self):
        self._attacks_left = self._attacks_max_number

    def get_combat_action_Attack(self):
        return Attack()