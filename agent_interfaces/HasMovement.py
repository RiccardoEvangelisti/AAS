from combat_actions.Movement import *


class HasMovement:
    """The agent can move"""

    # movement_speed
    @property
    def movement_speed(self) -> int:
        return self.__movement_speed

    @movement_speed.setter
    def movement_speed(self, value: int):
        self.__movement_speed = value

    # movement_left
    @property
    def movement_left(self) -> int:
        return self._movement_left

    @movement_left.setter
    def movement_left(self, value: int):
        self._movement_left = value

    # Constructor
    def __init__(self, movement_speed: int):
        self.movement_speed = movement_speed
        self.movement_left = movement_speed

    def moved_of(self, n_cells: int):
        """Decrease the movement of n_cells"""
        self.movement_left -= n_cells

    def is_movement_available(self) -> bool:
        """Check if the agent can move"""
        return self.movement_left > 0

    def reset_movement(self):
        """Reset the agent's movement to the maximum"""
        self.movement_left = self.movement_speed

    # Getters
    def get_combat_action_Movement_UP(self):
        return Movement_UP()

    def get_combat_action_Movement_DOWN(self):
        return Movement_DOWN()

    def get_combat_action_Movement_LEFT(self):
        return Movement_LEFT()

    def get_combat_action_Movement_RIGHT(self):
        return Movement_RIGHT()

    def get_combat_action_Movement_UP_LEFT(self):
        return Movement_UP_LEFT()

    def get_combat_action_Movement_UP_RIGHT(self):
        return Movement_UP_RIGHT()

    def get_combat_action_Movement_DOWN_LEFT(self):
        return Movement_DOWN_LEFT()

    def get_combat_action_Movement_DOWN_RIGHT(self):
        return Movement_DOWN_RIGHT()

    def get_all_movements(self):
        return [
            self.get_combat_action_Movement_UP(),
            self.get_combat_action_Movement_DOWN(),
            self.get_combat_action_Movement_LEFT(),
            self.get_combat_action_Movement_RIGHT(),
            self.get_combat_action_Movement_UP_LEFT(),
            self.get_combat_action_Movement_UP_RIGHT(),
            self.get_combat_action_Movement_DOWN_LEFT(),
            self.get_combat_action_Movement_DOWN_RIGHT(),
        ]
