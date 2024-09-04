
from enum import Enum


class HasEndTurn:
    EndTurn = Enum("EndTurn", "END_TURN")

    def is_end_turn_available(self) -> bool:
        return True