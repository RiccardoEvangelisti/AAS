from combat_actions.Movement import *


class HasMovement:

    def __init__(self, movement_speed: int):
        self._movement_speed = movement_speed
        self._movement_left = movement_speed

    def moved_of(self, n_cells: int):
        self._movement_left -= n_cells

    def is_movement_available(self) -> bool:
        return self._movement_left > 0

    def reset_movement(self):
        self._movement_left = self._movement_speed

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
