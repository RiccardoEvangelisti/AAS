from abc import ABC, abstractmethod
from enum import Enum

from CombatActions import CombatAction


class Movement(CombatAction, ABC):
    @abstractmethod
    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        pass


#################################################


class Movement_UP(Movement):
    def __init__(self):
        self._name = "Movement_UP"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return y > 0 and grid[x, y - 1] == 0


class Movement_DOWN(Movement):
    def __init__(self):
        self._name = "Movement_DOWN"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return y < n_squares_height - 1 and grid[x, y + 1] == 0


class Movement_LEFT(Movement):
    def __init__(self):
        self._name = "Movement_LEFT"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return x > 0 and grid[x - 1, y] == 0


class Movement_RIGHT(Movement):
    def __init__(self):
        self._name = "Movement_RIGHT"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return x < n_squares_width - 1 and grid[x + 1, y] == 0


class Movement_UP_LEFT(Movement):
    def __init__(self):
        self._name = "Movement_UP_LEFT"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return y > 0 and x > 0 and grid[x - 1, y - 1] == 0


class Movement_UP_RIGHT(Movement):
    def __init__(self):
        self._name = "Movement_UP_RIGHT"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return y > 0 and x < n_squares_width - 1 and grid[x + 1, y - 1] == 0


class Movement_DOWN_LEFT(Movement):
    def __init__(self):
        self._name = "Movement_DOWN_LEFT"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return y < n_squares_height - 1 and x > 0 and grid[x - 1, y + 1] == 0


class Movement_DOWN_RIGHT(Movement):
    def __init__(self):
        self._name = "Movement_DOWN_RIGHT"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        x, y = current_position
        return y < n_squares_height - 1 and x < n_squares_width - 1 and grid[x + 1, y + 1] == 0


#################################################


class HasMovement(ABC):
    @property
    @abstractmethod
    def movement_speed(self) -> int:
        pass

    @property
    @abstractmethod
    def movement_left(self) -> int:
        pass

    @movement_left.setter
    def movement_left(self, value: int):
        self._movement_left = value

    @movement_speed.setter
    def movement_speed(self, value: int):
        if value % 5 != 0:
            raise ValueError("Movement speed must be a multiple of 5")
        self._movement_speed = value / 5

    def moved_of(self, n_cells: int):
        self._movement_left -= n_cells

    def is_movement_available(self) -> bool:
        return self._movement_left > 0

    def reset_movement(self):
        self._movement_left = self._movement_speed

    def get_combat_action_Movements(self):
        return (
            Movement_UP(),
            Movement_DOWN(),
            Movement_LEFT(),
            Movement_RIGHT(),
            Movement_UP_LEFT(),
            Movement_UP_RIGHT(),
            Movement_DOWN_LEFT(),
            Movement_DOWN_RIGHT(),
        )
