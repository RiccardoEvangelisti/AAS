from combat_actions.CombatActions import CombatAction


class EndTurn(CombatAction):

    def __init__(self):
        self._name = "EndTurn"

    @property
    def name(self):
        return self._name

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width):
        return True