class Statistics:
    def __init__(self):
        self.episode_statistics = []


class EpisodeStatistics:
    def __init__(self, episode_number, winner, enemy_hp_remaining, total_reward):
        self.episode_number = episode_number
        self.winner = winner
        self.enemy_hp_remaining = enemy_hp_remaining
        self.total_reward = total_reward
