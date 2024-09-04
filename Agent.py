from enum import Enum


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


class HasEndTurn:
    EndTurn = Enum("EndTurn", "END_TURN")

    def is_end_turn_available(self) -> bool:
        return True


class HasHP:
    def __init__(self, max_hp: int):
        self.max_hp = max_hp
        self.current_hp = max_hp

    def took_damage(self, damage: int):
        self.current_hp -= damage

    def is_alive(self) -> bool:
        return self.current_hp > 0


class HasMovement:
    Movement = Enum("Movement", ["UP", "DOWN", "LEFT", "RIGHT", "UP_RIGHT", "DOWN_RIGHT", "UP_LEFT", "DOWN_LEFT"])

    def __init__(self, movement_speed: int = 30):
        if movement_speed % 5 != 0:
            raise ValueError("Movement speed must be a multiple of 5")
        self.movement_speed = movement_speed / 5
        self.movement_left = movement_speed

    def moved_of(self, n_cells: int):
        self.movement_left -= n_cells

    def is_movement_available(self) -> bool:
        return self.movement_left > 0


class HasAttack:
    Attack = Enum("Attack", ["MELEE"])

    def __init__(self, attack_power: int = 5):
        self.attack_power = attack_power
        self.attack_available = True

    def attack(self, enemy: HasHP):
        enemy.took_damage(self.attack_power)
        self.attack_available = False  # Only one attack per turn

    def is_attack_available(self) -> bool:
        return self.attack_available


class Player(Agent, HasEndTurn, HasHP, HasMovement, HasAttack):
    def __init__(self, image_path: str, max_hp: int = 50, movement_speed: int = 30, attack_power: int = 5):
        Agent.__init__(self, image_path)
        HasHP.__init__(self, max_hp)
        HasMovement.__init__(self, movement_speed)
        HasAttack.__init__(self, attack_power)

    from DnDEnvironment import DnDEnvironment

    def available_actions(self, env: DnDEnvironment):
        available_actions=[]
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
