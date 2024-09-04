from abc import ABC, abstractmethod


class CombatAction(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    def name(self, value):
        self._name = value