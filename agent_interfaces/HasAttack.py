from combat_actions.Attack import MeleeAttack, RangedAttack


class HasAttack:

    # attacks_max_number
    @property
    def attacks_max_number(self) -> int:
        return self._attacks_max_number

    @attacks_max_number.setter
    def attacks_max_number(self, value: int):
        self._attacks_max_number = value

    # attacks_left
    @property
    def attacks_left(self) -> int:
        return self._attacks_left

    @attacks_left.setter
    def attacks_left(self, value: int):
        self._attacks_left = value

    # Constructor
    def __init__(self, attacks_max_number: int):
        self.attacks_max_number = attacks_max_number
        self.attacks_left = attacks_max_number

    def attacked(self):
        self.attacks_left -= 1

    def is_attack_available(self) -> bool:
        return self.attacks_left > 0

    def reset_attacks(self):
        self.attacks_left = self.attacks_max_number

    def get_combat_action_MeleeAttack(self, attack_damage):
        return MeleeAttack(attack_damage)

    def get_combat_action_RangedAttack(self, attack_damage, attack_range):
        return RangedAttack(attack_damage, attack_range)
