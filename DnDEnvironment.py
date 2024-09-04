from enum import Enum
import random
from typing import Literal
import pygame
import numpy as np

from Agent import *
from Agent import HasMovement

SQUARE_SIZE = 100


class DnDEnvironment:
    def __init__(self, n_squares_width=6, n_squares_height=5, _RENDER_MODE="human"):

        global RENDER_MODE
        RENDER_MODE = _RENDER_MODE

        self.n_squares_width = n_squares_width
        self.n_squares_height = n_squares_height
        self.grid = np.zeros((n_squares_width, n_squares_height))

        self.agents: list[Agent] = []

        if RENDER_MODE == "human":
            self.space_width = n_squares_width * SQUARE_SIZE
            self.space_height = n_squares_height * SQUARE_SIZE
            self.render_grid()

    # def can_move(self, direction: Movement, n_squares_width, n_squares_height) -> bool:
    #     result = True
    #     if direction in [Movement.UP, Movement.UP_RIGHT, Movement.UP_LEFT]:
    #         result = result and self.coordinates[1] > 0
    #     if direction in [Movement.DOWN, Movement.DOWN_RIGHT, Movement.DOWN_LEFT]:
    #         result = result and self.coordinates[1] < n_squares_height - 1
    #     if direction in [Movement.LEFT, Movement.UP_LEFT, Movement.DOWN_LEFT]:
    #         result = result and self.coordinates[0] > 0
    #     if direction in [Movement.RIGHT, Movement.UP_RIGHT, Movement.DOWN_RIGHT]:
    #         result = result and self.coordinates[0] < n_squares_width - 1
    #     return result

    def startCombat(self):
        if len(self.agents) > 0:
            self.playing_agentID = self.agents[0].id
        else:
            raise Exception("No agents in the environment")

    def change_turn(self):
        if self.playing_agentID == len(self.agents):
            # the agents list is over, so we start again
            self.playing_agentID = self.agents[0].id
        else:
            self.playing_agentID += 1

    # def available_directions(self, agentID: int) -> list[HasMovement.Movement]:
    #     x, y = self.agents[agentID - 1].coordinates
    #     directions = [
    #         (HasMovement.Movement.UP, y > 0 and self.grid[x, y - 1] == 0),
    #         (HasMovement.Movement.DOWN, y < self.n_squares_height - 1 and self.grid[x, y + 1] == 0),
    #         (HasMovement.Movement.LEFT, x > 0 and self.grid[x - 1, y] == 0),
    #         (HasMovement.Movement.RIGHT, x < self.n_squares_width - 1 and self.grid[x + 1, y] == 0),
    #         (HasMovement.Movement.UP_LEFT, y > 0 and x > 0 and self.grid[x - 1, y - 1] == 0),
    #         (HasMovement.Movement.UP_RIGHT, y > 0 and x < self.n_squares_width - 1 and self.grid[x + 1, y - 1] == 0),
    #         (HasMovement.Movement.DOWN_LEFT, y < self.n_squares_height - 1 and x > 0 and self.grid[x - 1, y + 1] == 0),
    #         (
    #             HasMovement.Movement.DOWN_RIGHT,
    #             y < self.n_squares_height - 1 and x < self.n_squares_width - 1 and self.grid[x + 1, y + 1] == 0,
    #         ),
    #     ]
    #     return [direction for direction, condition in directions if condition]

    def update_occupied_position(self, old_position: tuple[int, int], new_position: tuple[int, int], agentID: int):
        """
        0-value means empty cell"""
        self.grid[old_position] = 0
        self.grid[new_position] = agentID

        self.agents[agentID - 1].coordinates = new_position

    def available_attacks(self, agentID: int, alliesID: list[int]) -> list[tuple[HasAttack.Attack, tuple[int, int]]]:
        x, y = self.agents[agentID - 1].coordinates
        empty_or_ally = [0] + alliesID
        attacks = [
            (HasAttack.Attack.MELEE, (x, y - 1)),
            (HasAttack.Attack.MELEE, (x, y + 1)),
            (HasAttack.Attack.MELEE, (x - 1, y)),
            (HasAttack.Attack.MELEE, (x + 1, y)),
            (HasAttack.Attack.MELEE, (x - 1, y - 1)),
            (HasAttack.Attack.MELEE, (x + 1, y - 1)),
            (HasAttack.Attack.MELEE, (x - 1, y + 1)),
            (HasAttack.Attack.MELEE, (x + 1, y + 1)),
        ]
        return [(attack, coords) for attack, coords in attacks if self.grid[coords] not in empty_or_ally]

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
        if type(position) == tuple:
            if (
                position[0] < 0
                or position[1] < 0
                or position[0] >= self.n_squares_width
                or position[1] >= self.n_squares_height
            ):
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
