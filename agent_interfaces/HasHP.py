class HasHP:
    @property
    def max_hp(self):
        return self._max_hp

    @max_hp.setter
    def max_hp(self, value: int):
        self._max_hp = value

    @property
    def current_hp(self):
        return self._current_hp

    @current_hp.setter
    def current_hp(self, value: int):
        self._current_hp = value

    def __init__(self, max_hp) -> None:
        self._max_hp = max_hp
        self._current_hp = max_hp

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def took_damage(self, damage: int):
        self.current_hp -= damage

    def reset_maxHP(self):
        self.current_hp = self._max_hp
