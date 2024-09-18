import os
import pickle
import gzip

import numpy as np


class StatSaver:
    def __init__(self, pickle_filename, max_episodes_per_file=10000):
        self.pickle_filename = pickle_filename
        self.max_episodes_per_file = max_episodes_per_file
        self.current_file_index = 0
        self.__last_episode_number = self._get_last_episode_number()

        self.episode_stats_list = []

    def _get_last_episode_number(self):
        # Check for existing files and get the last episode number
        file_exists = True
        last_episode_number = -1
        while file_exists:
            current_filename = f"{self.pickle_filename}_save{self.current_file_index}.pkl.gz"
            if os.path.exists(current_filename):
                with gzip.open(current_filename, "rb") as f:
                    stats = pickle.load(f)
                    last_episode_number += len(stats)
                self.current_file_index += 1
            else:
                file_exists = False
        return last_episode_number

    def get_episode_number(self):
        self.__last_episode_number += 1
        return self.__last_episode_number

    def __save_current_file(self):
        current_filename = f"{self.pickle_filename}_save{self.current_file_index}.pkl.gz"
        if os.path.exists(current_filename):
            with gzip.open(current_filename, "rb") as f:
                old_episode_stats_list = pickle.load(f)
                old_episode_stats_list.extend(self.episode_stats_list)
                self.episode_stats_list = old_episode_stats_list

        with gzip.open(current_filename, "wb") as f:
            pickle.dump(self.episode_stats_list, f)

        # Clear the list and move to the next file
        self.episode_stats_list = []
        self.current_file_index += 1

    def add_episode(self, stats):
        self.episode_stats_list.append(stats)
        # If we reach the max number of episodes per file, save and start a new file
        if len(self.episode_stats_list) >= self.max_episodes_per_file:
            self.__save_current_file()

    def save_statistics(self):
        # Save remaining episodes (if less than max_episodes_per_file)
        if self.episode_stats_list:
            self.__save_current_file()

    @staticmethod
    def load_all_statistics(pickle_filename):
        episode_stats_list = []
        file_index = 0
        while True:
            current_filename = f"{pickle_filename}_save{file_index}.pkl.gz"
            if not os.path.exists(current_filename):
                break
            with gzip.open(current_filename, "rb") as f:
                stats = pickle.load(f)
                episode_stats_list.extend(stats)
            file_index += 1
        return episode_stats_list


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
