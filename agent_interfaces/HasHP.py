class HasHP:
    """The agent has HP"""

    # max_hp
    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value: int):
        self._max_hp = value

    # current_hp
    @property
    def current_hp(self):
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value: int):
        self._current_hp = value

    # Constructor
    def __init__(self, max_hp) -> None:
        self.max_hp = max_hp
        self.current_hp = max_hp

    def is_alive(self) -> bool:
        """Check if the agent is alive"""
        return self.current_hp > 0

    def took_damage(self, damage: int):
        """Decrease the current HP by the damage"""
        self.current_hp -= damage

    def reset_maxHP(self):
        """Reset the current HP to the max_HP"""
        self.current_hp = self.max_hp
