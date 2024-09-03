import random
from typing import Literal
import pygame
import numpy as np

SQUARE_SIZE = 100

RENDER_MODE = "human"


class Agent:
    def __init__(self, position):
        self.position = position


class DnDEnvironment:
    def __init__(self, n_squares_width=6, n_squares_height=5):

        self.space_width = n_squares_width * SQUARE_SIZE
        self.space_height = n_squares_height * SQUARE_SIZE

        if RENDER_MODE == "human":
            self.render_grid()

    def add_agents(self, player: Agent, monsters: list[Agent]):
        self.player = player
        self.monsters = monsters

        if RENDER_MODE == "human":
            self.render_agents()


    def get_cell_position_by_name(
        self, cell_name=Literal["top_left", "top_right", "bottom_left", "bottom_right", "random"]
    ):
        if cell_name == "top_left":
            return (0, 0)
        elif cell_name == "top_right":
            return (self.space_width - SQUARE_SIZE, 0)
        elif cell_name == "bottom_left":
            return (0, self.space_height - SQUARE_SIZE)
        elif cell_name == "bottom_right":
            return (self.space_width - SQUARE_SIZE, self.space_height - SQUARE_SIZE)
        elif cell_name == "random":
            x = random.randint(0, self.space_width - SQUARE_SIZE)
            y = random.randint(0, self.space_height - SQUARE_SIZE)
            return (x, y)
        else:
            raise ValueError(f"Invalid cell name: {cell_name}")

    def render_grid(self):
        # Create the screen
        screen = pygame.display.set_mode((self.space_width, self.space_height))
        pygame.display.set_caption("Kill the Monster")
        background_image = pygame.image.load("background.png")
        background_image = pygame.transform.chop(background_image, (0, 0, self.space_width, self.space_height))
        # background_image = pygame.transform.smoothscale(background_image, (self.space_width, self.space_height))
        # Color the screen
        screen.blit(background_image, (0, 0))
        # Draw lines to represent the grid
        for x in range(0, self.space_width, SQUARE_SIZE):
            pygame.draw.line(screen, "black", (x, 0), (x, self.space_height))
        for y in range(0, self.space_height, SQUARE_SIZE):
            pygame.draw.line(screen, "black", (0, y), (self.space_width, y))
        # Update the full display Surface to the screen
        pygame.display.flip()

    def render_agents(self):
        screen = pygame.display.get_surface()
        # Draw the player
        player_image = pygame.image.load("Erik combat pose-token.png")
        player_image = pygame.transform.smoothscale(player_image, (SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(player_image, (self.player.position[0], self.player.position[1]))
        # Draw the monsters
        for monster in self.monsters:
            monster_image = pygame.image.load("mimic-token.png")
            monster_image = pygame.transform.smoothscale(monster_image, (SQUARE_SIZE, SQUARE_SIZE))
            screen.blit(monster_image, (monster.position[0], monster.position[1]))
        # Update the full display Surface to the screen
        pygame.display.flip()


def main():
    env = DnDEnvironment(n_squares_width=6, n_squares_height=5)

    player = Agent(env.get_cell_position("top_left"))
    monsters = list([Agent(env.get_cell_position("random"))])

    env.add_agents(player=player, monsters=monsters)

    pygame.time.wait(3000)
    pygame.quit()


if __name__ == "__main__":
    main()
