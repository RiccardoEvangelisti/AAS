from abc import ABC, abstractmethod


class CombatAction(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    def name(self, value):
        self._name = value

    @abstractmethod
    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        pass
