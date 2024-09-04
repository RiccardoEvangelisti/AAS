from CombatActions import CombatAction


class EndTurn(CombatAction):

    def __init__(self):
        self._name = "EndTurn"

    @property
    def name(self):
        return self._name

    def is_available(self, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        return True


class HasEndTurn:
    def get_combat_action_EndTurn(self):
        return EndTurn()
