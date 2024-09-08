import pygame
from combat_actions.CombatActions import CombatAction
from agent_interfaces.HasHP import HasHP
from agent_interfaces.HasMovement import HasMovement
from agent_interfaces.HasAttack import HasAttack
from agent_interfaces.HasEndTurn import HasEndTurn


class Agent(HasHP):

    # id
    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        self.__id = value

    # name
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    # coordinates
    @property
    def coordinates(self) -> tuple[int, int]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, value: tuple[int, int]):
        self.__coordinates = value

    # default_coordinates
    @property
    def default_coordinates(self) -> tuple[int, int] | str:
        return self.__default_coordinates

    @default_coordinates.setter
    def default_coordinates(self, value: tuple[int, int] | str):
        self.__default_coordinates = value

    # combatActions: dict of {CombatActions.name: CombatAction}
    @property
    def combatActions(self) -> dict[str, CombatAction]:
        return self.__combatActions

    @combatActions.setter
    def combatActions(self, value: dict[str, CombatAction]):
        self.__combatActions = value

    # Constructor
    def __init__(self, name: str, image_path: str, RENDER_MODE: str):
        self.name = name
        self.combatActions = {}

        if RENDER_MODE == "human":
            self.image_obj = pygame.image.load(image_path)

    def available_actions(self, grid, n_squares_height, n_squares_width) -> list[CombatAction]:
        """For all the actions that the agent can do, check which are available"""
        available_actions: list[CombatAction] = []
        for _, combat_action in self.combatActions.items():
            if combat_action.is_available(self, self.coordinates, grid, n_squares_height, n_squares_width):
                available_actions.append(combat_action)
        return available_actions

    def save_action(self, action: CombatAction):
        self.combatActions[action.name] = action

    def save_actions(self, action: list[CombatAction]):
        for act in action:
            self.save_action(act)


########################################################
#### CUSTOM AGENTS #####################################
########################################################


class Player(Agent, HasHP, HasEndTurn, HasMovement, HasAttack):
    def __init__(
        self,
        name: str,
        image_path: str,
        max_hp: int,
        movement_speed: int,
        attack_damage: int,
        attacks_max_number: int,
        RENDER_MODE: str,
    ):
        Agent.__init__(self, name, image_path, RENDER_MODE)

        HasHP.__init__(self, max_hp)

        HasEndTurn.__init__(self)
        self.save_action(self.get_combat_action_EndTurn())

        HasMovement.__init__(self, movement_speed)
        self.save_actions(self.get_all_movements())

        HasAttack.__init__(self, attacks_max_number)
        self.save_action(self.get_combat_action_MeleeAttack(attack_damage))
        self.save_action(self.get_combat_action_RangedAttack(attack_damage, 3))


#############################################


class Monster(Agent, HasEndTurn, HasMovement, HasAttack):
    def __init__(
        self,
        name: str,
        image_path: str,
        max_hp: int,
        movement_speed: int,
        attack_damage: int,
        attacks_max_number: int,
        RENDER_MODE: str,
    ):
        Agent.__init__(self, name, image_path, RENDER_MODE)

        HasHP.__init__(self, max_hp)

        HasEndTurn.__init__(self)
        self.save_action(self.get_combat_action_EndTurn())

        HasMovement.__init__(self, movement_speed)
        self.save_actions(self.get_all_movements())

        HasAttack.__init__(self, attacks_max_number)
        self.save_action(self.get_combat_action_MeleeAttack(attack_damage))
