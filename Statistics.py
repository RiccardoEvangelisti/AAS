class Statistics:
    def __init__(self):
        self.episode_statistics: list[EpisodeStatistics] = []

    def print(self):
        print("\n\n\nStatistics", end="\r")


class EpisodeStatistics:

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
    def enemy_hp_remaining(self):
        return self.__enemy_hp_remaining

    @enemy_hp_remaining.setter
    def enemy_hp_remaining(self, value: int):
        self.__enemy_hp_remaining = value

    @property
    def total_reward(self) -> int:
        return self.__total_reward

    @total_reward.setter
    def total_reward(self, value: int):
        self.__total_reward = value

    @property
    def actions_taken(self) -> dict[int, list[str]]:
        return self.__actions_taken

    @actions_taken.setter
    def actions_taken(self, value: dict[int, list[str]]):
        """Dictionary of actions taken by each player: {agentID, list[actions]}"""
        self.__actions_taken = value

    def __init__(self, episode_number: int, agentIDs: list[int]):
        self.episode_number = episode_number
        self.total_reward = 0
        self.actions_taken = {}
        for agentID in agentIDs:
            self.actions_taken[agentID] = []
