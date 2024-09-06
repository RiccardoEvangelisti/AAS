from combat_actions.CombatActions import CombatAction


class Movement_UP(CombatAction):
    def __init__(self):
        self.name = "Movement_UP"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return y > 0 and grid[x, y - 1] == 0


class Movement_DOWN(CombatAction):
    def __init__(self):
        self.name = "Movement_DOWN"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return y < n_squares_height - 1 and grid[x, y + 1] == 0


class Movement_LEFT(CombatAction):
    def __init__(self):
        self.name = "Movement_LEFT"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return x > 0 and grid[x - 1, y] == 0


class Movement_RIGHT(CombatAction):
    def __init__(self):
        self.name = "Movement_RIGHT"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return x < n_squares_width - 1 and grid[x + 1, y] == 0


class Movement_UP_LEFT(CombatAction):
    def __init__(self):
        self.name = "Movement_UP_LEFT"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return y > 0 and x > 0 and grid[x - 1, y - 1] == 0


class Movement_UP_RIGHT(CombatAction):
    def __init__(self):
        self.name = "Movement_UP_RIGHT"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return y > 0 and x < n_squares_width - 1 and grid[x + 1, y - 1] == 0


class Movement_DOWN_LEFT(CombatAction):
    def __init__(self):
        self.name = "Movement_DOWN_LEFT"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return y < n_squares_height - 1 and x > 0 and grid[x - 1, y + 1] == 0


class Movement_DOWN_RIGHT(CombatAction):
    def __init__(self):
        self.name = "Movement_DOWN_RIGHT"

    def is_available(self, agent, current_position: tuple[int, int], grid, n_squares_height, n_squares_width) -> bool:
        from agent_interfaces.HasMovement import HasMovement

        if isinstance(agent, HasMovement) and not agent.is_movement_available():
            return False
        x, y = current_position
        return y < n_squares_height - 1 and x < n_squares_width - 1 and grid[x + 1, y + 1] == 0
