import gymnasium as gym
from minigrid.core.grid import Grid
from minigrid.core.world_object import Goal
from minigrid.minigrid_env import MiniGridEnv
from minigrid.core.mission import MissionSpace
from minigrid.manual_control import ManualControl
from minigrid.core.actions import Actions


class DnDEnvironment(MiniGridEnv):
    def __init__(
        self,
        size=8,
        agent_start_pos=(1, 1),
        agent_start_dir=0,
        max_steps: int | None = None,
        **kwargs,
    ):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir

        mission_space = MissionSpace(mission_func=self._gen_mission, seed=42)

        super().__init__(
            mission_space=mission_space,
            grid_size=size,
            max_steps=256,
            **kwargs,
        )

    @staticmethod
    def _gen_mission():
        return "Kill the monster"

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)
        # Create the walls that surrounds the grid
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent in the environment
        if self.agent_start_pos is not None:
            self.agent_pos = self.agent_start_pos
            self.agent_dir = self.agent_start_dir
        else:
            self.place_agent()

        # Place the Goal
        self.put_obj(Goal(), width - 2, height - 2)

    def step(self, action):
        obs, reward, done, info, _ = super().step(action)

        # Customize the reward or done condition here if needed

        return obs, reward, done, info, _


def main():
    
    # # enable manual control for testing
    # env = DnDEnvironment(render_mode="human")
    # manual_control = ManualControl(env, seed=42)
    # manual_control.start()

    # Register the environment with Gymnasium
    gym.envs.registration.register(
        id="DnDEnvironment-v0",
        entry_point=DnDEnvironment,
    )

    # Create an instance of the environment
    env = gym.make("DnDEnvironment-v0", render_mode="human")

    # Reset the environment
    obs = env.reset()

    # Example interaction with the environment
    done = False
    while not done:
        env.render()  # Render the environment
        action = env.action_space.sample()  # Take a random action
        obs, reward, done, info, _ = env.step(action)  # Perform the action

    env.close()  # Close the rendering window


if __name__ == "__main__":
    main()
