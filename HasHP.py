from abc import ABC, abstractmethod

class HasHP(ABC):
    @property
    @abstractmethod
    def max_hp(self) -> int:
        pass

    @property
    @abstractmethod
    def current_hp(self) -> int:
        pass

    @current_hp.setter
    def current_hp(self, value: int):
        self._current_hp = value

    def is_alive(self) -> bool:
        return self.current_hp > 0

    def took_damage(self, damage: int):
        self.current_hp -= damage

    def reset_maxHP(self):
        self.current_hp = self.max_hp