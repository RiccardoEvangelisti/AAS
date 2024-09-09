import os
import pickle

import numpy as np


class Statistics:

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
    def total_reward(self) -> int:
        return self.__total_reward

    @total_reward.setter
    def total_reward(self, value: int):
        self.__total_reward = value

    @property
    def actions_taken(self) -> dict[str, list[str]]:
        return self.__actions_taken

    @actions_taken.setter
    def actions_taken(self, value: dict[str, list[str]]):
        """Dictionary of actions taken by each player: {agentName, list[actions]}"""
        self.__actions_taken = value

    def __init__(self, agentNames: list[str], pickle_filename):
        # Load value-function from file, if it exists
        if os.path.exists(pickle_filename):
            with open(pickle_filename, "rb") as f:
                last_episode_number = len(pickle.load(f))
        else:
            last_episode_number = 0

        self.episode_number = last_episode_number
        self.total_reward = 0
        self.actions_taken = {}
        for agentName in agentNames:
            self.actions_taken[agentName] = []

    def save_statistics(self, pickle_filename):
        dictionary = {}
        dictionary[self.episode_number] = {
            "winner": self.winner_name,
            "hp_remaining_winner": self.winner_hp_remaining,
            "total_reward": self.total_reward,
            "list": [],
        }

        for agentName, actionList in self.actions_taken.items():
            values, counts = np.unique(actionList, return_counts=True)
            dictionary[self.episode_number]["list"].append(
                {agentName: {value: count for value, count in zip(values, counts)}}
            )

        if os.path.exists(pickle_filename):
            with open(pickle_filename, "rb") as f:
                old_dictionary = pickle.load(f)
                old_dictionary.update(dictionary)
                dictionary = old_dictionary

        with open(pickle_filename, "wb") as f:
            pickle.dump(dictionary, f)
