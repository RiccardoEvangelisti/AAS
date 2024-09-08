from abc import ABC, abstractmethod


class CombatAction(ABC):
    """
    Abstract class representing an action that an agent can take during combat"""

    @property
    def name(self) -> str:
        """Name of the action"""
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @abstractmethod
    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        """Returns True if the action is available to the agent at the current position, False otherwise"""
        pass
