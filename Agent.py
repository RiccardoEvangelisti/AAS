from enum import Enum

from HasHP import HasHP
from HasMovement import HasMovement
from HasAttack import HasAttack
from HasEndTurn import HasEndTurn


class Agent:
    def __init__(self, image_path: str, RENDER_MODE="human"):
        RENDER_MODE = RENDER_MODE

        self.id: int
        self.coordinates: tuple[int, int]
        self.allies = list()

        if RENDER_MODE == "human":
            self.image_path = image_path

    def add_allie(self, allie_id: int):
        self.allies.append(allie_id)


class Player(Agent, HasEndTurn, HasHP, HasMovement, HasAttack):
    def __init__(
        self,
        image_path: str,
        max_hp: int = 50,
        movement_speed: int = 30,
        attack_power: int = 5,
        attacks_max_number: int = 1,
    ):
        Agent.__init__(self, image_path)

        self._max_hp = max_hp
        self._current_hp = max_hp

        self._movement_speed = movement_speed
        self._movement_left = movement_speed

        self._attack_power = attack_power
        self._attacks_left = attacks_max_number
        self._attacks_max_number = attacks_max_number

    from DnDEnvironment import DnDEnvironment

    def available_actions(self, env: DnDEnvironment):
        available_actions = []
        # HasEndTurn
        if self.is_end_turn_available():
            available_actions.append(HasEndTurn.EndTurn.END_TURN)
        # HasMovement
        if self.is_movement_available():
            for direction_avail in env.available_directions(self.id):
                available_actions.append(direction_avail)
        # HasAttack
        if self.is_attack_available():
            for attack_avail, target_coord in env.available_attacks(self.id, self.allies):
                available_actions.append((attack_avail, target_coord))

        return available_actions

    @property
    def max_hp(self) -> int:
        return self._max_hp

    @property
    def current_hp(self) -> int:
        return self._current_hp

    @property
    def movement_speed(self) -> int:
        raise NotImplementedError

    @property
    def movement_left(self) -> int:
        raise NotImplementedError

    @property
    def attack_power(self) -> int:
        raise NotImplementedError

    @property
    def attacks_left(self) -> int:
        raise NotImplementedError

    @property
    def attacks_max_number(self) -> int:
        raise NotImplementedError
