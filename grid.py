import gymnasium as gym
from minigrid.core.grid import Grid
from minigrid.core.world_object import Goal
from minigrid.minigrid_env import MiniGridEnv
from minigrid.core.actions import Actions


class CustomGridEnv(MiniGridEnv):
    def __init__(self, size=30):
        super().__init__(grid_size=size, max_steps=4 * size * size, agent_view_size=7)

    def _gen_grid(self, width, height):
        # Create an empty grid
        self.grid = Grid(width, height)

        # Generate surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Place the agent at a random position
        self.place_agent()

        # Place a goal square in the environment
        goal = Goal()
        self.put_obj(goal, width - 2, height - 2)

        # Set the mission statement
        self.mission = "Reach the goal"

    def step(self, action):
        obs, reward, done, info = super().step(action)

        # Customize the reward or done condition here if needed

        return obs, reward, done, info


# Register the environment with Gymnasium
gym.envs.registration.register(
    id="CustomGridEnv-v0",
    entry_point=CustomGridEnv,
)

# Create an instance of the environment
env = gym.make("CustomGridEnv-v0")

# Reset the environment
obs = env.reset()

# Example interaction with the environment
done = False
while not done:
    env.render()  # Render the environment
    action = env.action_space.sample()  # Take a random action
    obs, reward, done, info = env.step(action)  # Perform the action

env.close()  # Close the rendering window
