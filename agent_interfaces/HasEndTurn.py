from combat_actions.EndTurn import EndTurn


class HasEndTurn:
    """The agent can end its turn"""

    def get_combat_action_EndTurn(self):
        return EndTurn()
