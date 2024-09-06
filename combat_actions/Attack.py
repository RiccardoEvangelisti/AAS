from abc import ABC

from combat_actions.CombatActions import CombatAction


class Attack(CombatAction, ABC):

    # attack_damage
    @property
    def attack_damage(self) -> int:
        return self._attack_damage

    @attack_damage.setter
    def attack_damage(self, value: int):
        self._attack_damage = value

    # attack_range
    @property
    def attack_range(self) -> int:
        return self._attack_range

    @attack_range.setter
    def attack_range(self, value: int):
        self._attack_range = value

    # target_coord
    @property
    def target_coord(self) -> tuple[int, int]:
        return self._target_coord

    @target_coord.setter
    def target_coord(self, value: tuple[int, int]):
        self._target_coord = value

    # target_id
    @property
    def target_id(self) -> int:
        return self._target_id

    @target_id.setter
    def target_id(self, value: int):
        self._target_id = value

    # is_available
    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasAttack import HasAttack

        # Check if the agent has at least one attack available
        if isinstance(agent, HasAttack) and not agent.is_attack_available():
            return False

        x, y = current_position

        # Take the minimim and maximum cell coordinates that the agent can attack, based on his attack range and his position on the grid
        min_cell_x = max(0, x - self.attack_range)
        max_cell_x = min(n_squares_width - 1, x + self.attack_range)
        min_cell_y = max(0, y - self.attack_range)
        max_cell_y = min(n_squares_height - 1, y + self.attack_range)

        # Check if there is an enemy within range of the attack
        # Return the first enemy found
        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                if (cell_x, cell_y) != (x, y) and grid[cell_x, cell_y] != 0:
                    self.target_coord = (cell_x, cell_y)  # save its coordinates
                    self.target_id = grid[cell_x, cell_y]  # save its id
                    return True

        return False


#########################################


class MeleeAttack(Attack):
    def __init__(self, attack_damage):
        self.name = "MeleeAttack"
        self.attack_damage = attack_damage
        self.attack_range = 1


#########################################


class RangedAttack(Attack):
    def __init__(self, attack_damage, attack_range):
        self.name = "RangeAttack"
        self.attack_damage = attack_damage
        self.attack_range = attack_range
