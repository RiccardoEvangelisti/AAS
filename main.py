import random
from typing import Literal
import pygame
import numpy as np

SQUARE_SIZE = 100

RENDER_MODE = "human"


class Agent:
    def __init__(self, image_path: str):
        self.id = None
        self.coordinates = None
        if RENDER_MODE == "human":
            self.image_path = image_path


class DnDEnvironment:
    def __init__(self, n_squares_width=6, n_squares_height=5):

        self.n_squares_width = n_squares_width
        self.n_squares_height = n_squares_height
        self.grid = np.zeros((n_squares_width, n_squares_height))

        self.agents = list()

        if RENDER_MODE == "human":
            self.space_width = n_squares_width * SQUARE_SIZE
            self.space_height = n_squares_height * SQUARE_SIZE
            self.render_grid()

    def update_occupied_position(self, old_position: tuple[int, int], new_position: tuple[int, int], agentID: int):
        """
        0-value means empty cell"""
        self.grid[old_position] = 0
        self.grid[new_position] = agentID

        self.agents[agentID - 1].coordinates = new_position

    def generate_agentID(self):
        return len(self.agents)

    def place_agent(
        self,
        agent: Agent,
        position: tuple[int, int] | Literal["top_left", "top_right", "bottom_left", "bottom_right", "random"],
    ):

        self.agents.append(agent)

        agent.id = self.generate_agentID()

        coordinates = self.get_empty_cell_coordinates(position)

        self.update_occupied_position(coordinates, coordinates, agent.id)

        if RENDER_MODE == "human":
            self.render_agent(agent)
        

    def get_empty_cell_coordinates(
        self, position: tuple[int, int] | Literal["top_left", "top_right", "bottom_left", "bottom_right", "random"]
    ):

        if type(position) == tuple[int, int]:
            if position < 0 or position[0] >= self.n_squares_width or position[1] >= self.n_squares_height:
                ValueError(
                    f"Invalid input cell position: {position} out of {self.n_squares_width}x{self.n_squares_height}"
                )
            else:
                coordinates = position
        elif position == "top_left":
            coordinates = (0, 0)
        elif position == "top_right":
            coordinates = (self.n_squares_width - 1, 0)
        elif position == "bottom_left":
            coordinates = (0, self.n_squares_height - 1)
        elif position == "bottom_right":
            coordinates = (self.n_squares_width - 1, self.n_squares_height - 1)
        elif position == "random":
            x = random.randint(0, self.n_squares_width - 1)
            y = random.randint(0, self.n_squares_height - 1)
            coordinates = (x, y)
        else:
            raise ValueError(f"Invalid input cell name: {position}")

        # If it's not empty, find an empty cell
        if self.grid[coordinates] != 0:
            coordinates = self.get_empty_cell_coordinates("random")

        return coordinates

    def render_grid(self):
        # Create the screen
        screen = pygame.display.set_mode((self.space_width, self.space_height))
        pygame.display.set_caption("Kill the Monster")
        background_image = pygame.image.load("background.png")
        background_image = pygame.transform.smoothscale(background_image, (self.space_width, self.space_height))
        # Color the screen
        screen.blit(background_image, (0, 0))
        # Draw lines to represent the grid
        for x in range(0, self.space_width, SQUARE_SIZE):
            pygame.draw.line(screen, "black", (x, 0), (x, self.space_height))
        for y in range(0, self.space_height, SQUARE_SIZE):
            pygame.draw.line(screen, "black", (0, y), (self.space_width, y))
        # Update the full display Surface to the screen
        pygame.display.flip()

    def grid_to_screen_position(self, grid_position):
        return (grid_position[0] * SQUARE_SIZE, grid_position[1] * SQUARE_SIZE)

    def render_agent(self, agent):
        screen = pygame.display.get_surface()
        # Draw the agent
        agent_image = pygame.image.load(agent.image_path)
        agent_image = pygame.transform.smoothscale(agent_image, (SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(agent_image, self.grid_to_screen_position(agent.coordinates))
        # Update the full display Surface to the screen
        pygame.display.flip()


def main():
    env = DnDEnvironment(n_squares_width=6, n_squares_height=5)

    player = Agent("Erik combat pose-token.png")
    monster = Agent("mimic-token.png")

    env.place_agent(player, "top_left")
    env.place_agent(monster, "random")

    print(f"\nGrid:\n{env.grid.transpose()}")

    pygame.time.wait(1500)
    pygame.quit()


if __name__ == "__main__":
    main()
