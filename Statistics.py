import os
import pickle
import gzip

import numpy as np


class StatSaver:
    def __init__(self, pickle_filename):
        self.pickle_filename = pickle_filename

        # Load value-function from file, if it exists
        if os.path.exists(pickle_filename):
            with gzip.open(pickle_filename, "rb") as f:
                self.__last_episode_number = len(pickle.load(f)) - 1
        else:
            self.__last_episode_number = -1

        self.episode_stats_list = []

    def get_episode_number(self):
        self.__last_episode_number += 1
        return self.__last_episode_number

    def add_episode(self, stats):
        self.episode_stats_list.append(stats)

    def save_statistics(self):

        if os.path.exists(self.pickle_filename):
            with gzip.open(self.pickle_filename, "rb") as f:
                old_episode_stats_list = pickle.load(f)
                old_episode_stats_list.extend(self.episode_stats_list)
                self.episode_stats_list = old_episode_stats_list

        with gzip.open(self.pickle_filename, "wb") as f:
            pickle.dump(self.episode_stats_list, f)

        # Clear the list
        self.episode_stats_list = []


class EpisodeStats:

    @property
    def episode_number(self) -> int:
        return self.__episode_number

    @episode_number.setter
    def episode_number(self, value: int):
        self.__episode_number = value

    @property
    def winner_name(self) -> str:
        return self.__winner_name

    @winner_name.setter
    def winner_name(self, value: str):
        self.__winner_name = value

    @property
    def winner_hp_remaining(self):
        return self.__enemy_hp_remaining

    @winner_hp_remaining.setter
    def winner_hp_remaining(self, value: int):
        self.__enemy_hp_remaining = value

    @property
    def step_stats(self) -> list[tuple[str, str, int]]:
        return self.__actions_taken

    @step_stats.setter
    def step_stats(self, value: list[tuple[str, str, int]]):
        """List of (agentName, action_taken, reward)"""
        self.__actions_taken = value

    def __init__(self, agentNames: list[str], episode_number):
        self.episode_number = episode_number
        self.step_stats = []
