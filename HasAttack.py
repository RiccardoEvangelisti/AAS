from abc import ABC, abstractmethod

from CombatActions import CombatAction


class Attack(CombatAction, ABC):
    @property
    @abstractmethod
    def target_coord(self):
        pass

    @property
    @abstractmethod
    def attack_damage(self) -> int:
        pass

    @property
    @abstractmethod
    def attack_range(self) -> int:
        pass

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        if isinstance(agent, HasAttack) and not agent.is_attack_available():
            return False
        x, y = current_position

        if isinstance(self, Attack):
            min_cell_x = max(0, x - self.attack_range)
            max_cell_x = min(n_squares_width - 1, x + self.attack_range)
            min_cell_y = max(0, y - self.attack_range)
            max_cell_y = min(n_squares_height - 1, y + self.attack_range)

            for cell_x in range(min_cell_x, max_cell_x + 1):
                for cell_y in range(min_cell_y, max_cell_y + 1):
                    if (cell_x, cell_y) != (x, y) and grid[cell_x, cell_y] != 0:
                        self.target = ((cell_x, cell_y), grid[cell_x, cell_y])
                        return True
        return False


#########################################


class MeleeAttack(Attack):
    def __init__(self, attack_damage):
        self._name = "MeleeAttack"
        self._attack_damage = attack_damage
        self._attack_range = 1

    @property
    def name(self):
        return self._name

    @property
    def target_coord(self):
        return self._target_coord
    
    @target_coord.setter
    def target_coord(self, value: tuple[tuple[int, int], int]):
        self._target_coord = value

    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @property
    def attack_range(self) -> int:
        return self._attack_range


#########################################


class RangeAttack(Attack):
    def __init__(self, attack_damage, attack_range):
        self._name = "RangeAttack"
        self._attack_damage = attack_damage
        self._attack_range = attack_range

    @property
    def name(self):
        return self._name

    @property
    def target_coord(self):
        return self._target_coord

    @target_coord.setter
    def target_coord(self, value: tuple[tuple[int, int], int]):
        self._target_coord = value

    @property
    def attack_damage(self):
        return self._attack_damage

    @property
    def attack_range(self):
        return self._attack_range


#########################################


class HasAttack:

    def set_attacks_left(self, value: int):
        self._attacks_left = value

    def set_attacks_max_number(self, value: int):
        self._attacks_max_number = value

    attacks_left = property(fset=set_attacks_left)
    attacks_max_number = property(fset=set_attacks_max_number)

    def attacked(self):
        self._attacks_left -= 1

    def is_attack_available(self) -> bool:
        return self._attacks_left > 0

    def reset_attacks(self):
        self._attacks_left = self._attacks_max_number

    def get_combat_action_MeleeAttack(self, attack_damage):
        return MeleeAttack(attack_damage)

    def get_combat_action_RangedAttack(self, attack_damage, attack_range):
        return RangeAttack(attack_damage, attack_range)
