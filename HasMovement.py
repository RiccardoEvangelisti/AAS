from abc import ABC, abstractmethod
from enum import Enum


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

    Movement = Enum("Movement", ["UP", "DOWN", "LEFT", "RIGHT", "UP_RIGHT", "DOWN_RIGHT", "UP_LEFT", "DOWN_LEFT"])

    def moved_of(self, n_cells: int):
        self._movement_left -= n_cells

    def is_movement_available(self) -> bool:
        return self._movement_left > 0

    def reset_movement(self):
        self._movement_left = self._movement_speed
