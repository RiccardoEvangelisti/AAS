from abc import ABC, abstractmethod

from CombatActions import CombatAction


class Attack(CombatAction, ABC):
    @property
    @abstractmethod
    def target(self):
        pass

    @property
    @abstractmethod
    def attack_damage(self):
        pass

    @property
    @abstractmethod
    def attack_range(self):
        pass


#########################################


class MeleeAttack(Attack):
    def __init__(self, attack_damage):
        self._name = "MeleeAttack"
        self._attack_damage = attack_damage
        self._attack_range = 1

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position

        min_cell_x = max(0, x - self._attack_range)
        max_cell_x = min(n_squares_width - 1, x + self._attack_range)
        min_cell_y = max(0, y - self._attack_range)
        max_cell_y = min(n_squares_height - 1, y + self._attack_range)

        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                if (cell_x, cell_y) != (x, y) and grid[cell_x, cell_y] != 0:
                    self.target = ((cell_x, cell_y), grid[cell_x, cell_y])
                    return True
        return False

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target_coord

    @target.setter
    def target(self, value: tuple[tuple[int, int], int]):
        self._target_coord = value

    @property
    def attack_damage(self):
        return self._attack_damage

    @property
    def attack_range(self):
        return self._attack_range


#########################################


class HasAttack(ABC):
    @property
    @abstractmethod
    def attacks_left(self) -> int:
        pass

    @property
    @abstractmethod
    def attacks_max_number(self) -> int:
        pass

    @attacks_left.setter
    def attacks_left(self, value: int):
        self._attacks_left = value

    @attacks_max_number.setter
    def attacks_max_number(self, value: int):
        self._attacks_max_number = value

    def attacked(self):
        self._attacks_left -= 1

    def is_attack_available(self) -> bool:
        return self._attacks_left > 0

    def reset_attacks(self):
        self._attacks_left = self._attacks_max_number

    def get_combat_action_MeleeAttack(self, attack_damage):
        return MeleeAttack(attack_damage)
