import random
from typing import Literal
import pygame
import numpy as np

from Agent import *
from combat_actions.Attack import MeleeAttack, RangedAttack
from combat_actions.Movement import *

SQUARE_SIZE = 100


class DnDEnvironment:

    def __init__(self, n_squares_width=6, n_squares_height=5, _RENDER_MODE="human"):

        global RENDER_MODE
        RENDER_MODE = _RENDER_MODE

        self.n_squares_width = n_squares_width
        self.n_squares_height = n_squares_height
        self.grid = np.zeros((n_squares_width, n_squares_height), dtype=int)

        self.agents: list[Agent] = []

        if RENDER_MODE == "human":
            self.space_width = n_squares_width * SQUARE_SIZE
            self.space_height = n_squares_height * SQUARE_SIZE
            self.render_screenbase()

    def reset(self):
        # Set playing agent to the agent first added to the environment
        if len(self.agents) > 0:
            self.playing_agentID = self.agents[0].id
        else:
            raise Exception("No agents in the environment")

        for agent in self.agents:
            # Full health
            agent.reset_maxHP()
            # Full movement
            if isinstance(agent, HasMovement):
                agent.reset_movement()
            # Full attacks
            if isinstance(agent, HasAttack):
                agent.reset_attacks()
            # Reset position
            self.update_occupied_position(
                agent.coordinates, self.get_empty_cell_coordinates(agent.default_coordinates), agent.id
            )

    def takeAction(self, action):
        playing_agent = self.get_playing_agent()

        if action.name == MeleeAttack.name and isinstance(playing_agent, HasAttack):
            # Get the agent that is being attacked
            target_agent = self.agents[action.target_id - 1]
            # Target takes damage
            target_agent.took_damage(action.attack_damage)
            playing_agent.attacked()

        if action.name == RangedAttack.name and isinstance(playing_agent, HasAttack):
            # Get the agent that is being attacked
            target_agent = self.agents[action.target_id - 1]
            # Target takes damage
            target_agent.took_damage(action.attack_damage)
            playing_agent.attacked()

        if action.name == "EndTurn":
            self.change_turn()

        if action.name == Movement_UP.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0], playing_agent.coordinates[1] - 1)
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_DOWN.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0], playing_agent.coordinates[1] + 1)
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_LEFT.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0] - 1, playing_agent.coordinates[1])
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_RIGHT.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0] + 1, playing_agent.coordinates[1])
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_UP_LEFT.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0] - 1, playing_agent.coordinates[1] - 1)
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_UP_RIGHT.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0] + 1, playing_agent.coordinates[1] - 1)
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_DOWN_LEFT.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0] - 1, playing_agent.coordinates[1] + 1)
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

        if action.name == Movement_DOWN_RIGHT.name and isinstance(playing_agent, HasMovement):
            # Get the new position
            new_position = (playing_agent.coordinates[0] + 1, playing_agent.coordinates[1] + 1)
            # Update the grid
            self.update_occupied_position(playing_agent.coordinates, new_position, playing_agent.id)
            playing_agent.moved_of(1)

    def change_turn(self):
        playing_agent = self.get_playing_agent()

        # Full Movement speed
        if isinstance(playing_agent, HasMovement):
            playing_agent.reset_movement()
        # Full attacks left
        if isinstance(playing_agent, HasAttack):
            playing_agent.reset_attacks()

        # Change playing agent
        if self.playing_agentID == len(self.agents):
            # the agents list is over, so we start again
            self.playing_agentID = self.agents[0].id
        else:
            self.playing_agentID += 1

        if RENDER_MODE == "human":
            self.render_grid()
            for agent in self.agents:
                self.render_agent(agent)

    def get_agent_byID(self, agentID: int) -> Agent:
        return self.agents[agentID - 1]

    def get_playing_agent(self) -> Agent:
        return self.agents[self.playing_agentID - 1]

    def get_not_playing_agents(self) -> list[Agent]:
        return [agent for agent in self.agents if agent.id != self.playing_agentID]

    def update_occupied_position(self, old_position: tuple[int, int], new_position: tuple[int, int], agentID: int):
        """
        0-value means empty cell"""
        self.grid[old_position] = 0
        self.grid[new_position] = agentID

        self.agents[agentID - 1].coordinates = new_position

        if RENDER_MODE == "human":
            self.render_grid()
            for agent in self.agents:
                self.render_agent(agent)

    def generate_agentID(self):
        return len(self.agents)

    def place_agent(
        self,
        agent: Agent,
        position: tuple[int, int] | Literal["top_left", "top_right", "bottom_left", "bottom_right", "random"],
    ):
        self.agents.append(agent)
        agent.id = self.generate_agentID()
        if agent.id == 1:
            self.playing_agentID = agent.id

        agent.default_coordinates = position

        coordinates = self.get_empty_cell_coordinates(position)
        self.update_occupied_position(coordinates, coordinates, agent.id)

    def get_empty_cell_coordinates(
        self,
        position: tuple[int, int] | Literal["top_left", "top_right", "bottom_left", "bottom_right", "random"] | str,
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

    def render_screenbase(self):
        # Create the screen
        pygame.display.set_mode((self.space_width, self.space_height))
        # Update the full display Surface to the screen
        pygame.display.update()

    def render_grid(self):
        screen = pygame.display.get_surface()
        background_image = pygame.transform.smoothscale(
            pygame.image.load("pictures/background.png"), (self.space_width, self.space_height)
        )
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

    def render_agent(self, agent: Agent):
        screen = pygame.display.get_surface()
        # Draw the agent
        agent.image_obj = pygame.transform.smoothscale(agent.image_obj, (SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(
            (agent.image_obj.convert() if agent.id == self.get_playing_agent().id else agent.image_obj),
            self.grid_to_screen_position(agent.coordinates),
        )
        # Draw the agent's health bar
        health_bar_width = (agent.current_hp / agent.max_hp) * SQUARE_SIZE
        health_bar_height = SQUARE_SIZE / 10
        x, y = self.grid_to_screen_position(agent.coordinates)
        y += SQUARE_SIZE - health_bar_height
        pygame.draw.rect(screen, "green", (x, y, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, "black", (x, y, SQUARE_SIZE, health_bar_height), 1)  # black border
        # Update the full display Surface to the screen
        pygame.display.flip()
