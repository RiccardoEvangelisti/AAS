from CombatActions import CombatAction


class EndTurn(CombatAction):

    def __init__(self):
        self._name = "EndTurn"

    @property
    def name(self):
        return self._name


class HasEndTurn:
    def get_combat_action_EndTurn(self):
        return EndTurn()
