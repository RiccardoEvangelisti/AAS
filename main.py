import os
import pickle
import random
import pygame
import numpy as np

from CombatActions import CombatAction
from HasAttack import Attack, MeleeAttack
from HasMovement import HasMovement

from Agent import Agent, HasAttack, Monster, Player
from DnDEnvironment import DnDEnvironment
from Statistics import EpisodeStatistics


class State:
    def update_agents_coord(self, agents: list[Agent]):
        self.agents_coordinates = []
        for agent in agents:
            self.agents_coordinates.append(agent.coordinates[0])
            self.agents_coordinates.append(agent.coordinates[1])

    def update_current_hp(self, agent: Agent):
        self.current_hp = agent.current_hp

    def update_damage_dealt(self, enemy: Agent):
        self.damage_dealt = enemy.max_hp - enemy.current_hp

    def update_attack_available(self, agent: Agent):
        if isinstance(agent, HasAttack):
            self.attacks_remaining = agent._attacks_left
        else:
            self.attacks_remaining = 0

    def update_movement_available(self, agent: Agent):
        if isinstance(agent, HasMovement):
            self.movement_remaining = agent._movement_left
        else:
            self.movement_remaining = 0

    def to_array(self):
        return np.hstack(
            [
                self.agents_coordinates,
                self.current_hp,
                self.damage_dealt,
                self.attacks_remaining,
                self.movement_remaining,
            ]
        )


##########################################


def step(action: CombatAction, available_actions, state: State, env: DnDEnvironment):
    playing_agent = env.get_playing_agent()
    enemy_agent = env.get_not_playing_agents()[0]

    old_enemy_hp = enemy_agent.current_hp

    # Take Action
    env.takeAction(action)

    # Reward
    if not enemy_agent.is_alive():
        reward = 10
        done = True
    elif not playing_agent.is_alive():
        reward = -10
        done = True
    elif enemy_agent.current_hp < old_enemy_hp:
        reward = 3
        done = False
    elif (
        action.name == "EndTurn"
        and state.attacks_remaining > 0
        and any(isinstance(a, Attack) for a in available_actions)
    ):
        reward = -5
        done = False
    else:
        reward = 0
        done = False

    # New State
    playing_agent = env.get_playing_agent()
    enemy_agent = env.get_not_playing_agents()[0]
    new_state = State()
    new_state.update_agents_coord([playing_agent, enemy_agent])
    new_state.update_current_hp(playing_agent)
    new_state.update_damage_dealt(enemy_agent)
    new_state.update_attack_available(playing_agent)
    new_state.update_movement_available(playing_agent)
    print(f"\tNew State: {new_state.to_array()}")

    return new_state, reward, done


######################################

EPSILON = 0.2  # Exploration rate
ALPHA = 0.1  # Learning rate
GAMMA = 0.9  # Discount factor


# Load value function from a file
ql_file = "q_learning_values.pkl"
if os.path.exists(ql_file):
    with open(ql_file, "rb") as f:
        q_dict = pickle.load(f)
else:
    q_dict = {}  # Dictionary to store Q-values: {(state.to_array, action.name): q_value}
    with open(ql_file, "wb") as f:
        pickle.dump(q_dict, f)


# epsilon-greedy policy
def chooseAction(state, available_actions: list[CombatAction]):
    # Explore
    if random.random() < EPSILON:
        return random.choice(available_actions)

    # Exploit
    state_bytes = state.to_array().tobytes()

    # Take action-value pairs that match the current state and in available actions
    q_filtered = {
        _action_str: _value
        for (_state, _action_str), _value in q_dict.items()
        if _state == state_bytes and any(action.name == _action_str for action in available_actions)
    }

    # If there are no matching state-action pairs, return a random action
    if not q_filtered:
        return random.choice(available_actions)

    # Get the actions with the highest q-value
    max_q_value = max(q_filtered.values())  # Get the highest q-value
    # Get actions with the highest q-value
    best_actions = [action for action in available_actions if q_filtered.get(action.name) == max_q_value]
    # Return a random action from the list of actions with the highest q-value
    return random.choice(best_actions)


def learn(state, action, reward, next_state):
    q_value_current = q_dict.get((state.to_array().tobytes(), action), 0)
    # Take the state-action pairs that match the next_state
    q_filtered = dict(filter(lambda item: item[0][0] == next_state.to_array().tobytes(), q_dict.items()))

    # Get the highest q-value for the next_state
    max_q_value_next = max(q_filtered.values()) if q_filtered else 0

    # Update the Q-value for the current state-action pair
    q_dict[(state.to_array().tobytes(), action.name)] = q_value_current + ALPHA * (
        reward + GAMMA * max_q_value_next - q_value_current
    )


#####################################


def main():
    env = DnDEnvironment(n_squares_width=6, n_squares_height=5, _RENDER_MODE="human")

    player = Player("Erik combat pose-token.png", max_hp=50)
    monster = Monster("mimic2-token.png", max_hp=100, attack_damage=10, movement_speed=15)

    env.place_agent(player, "random")
    env.place_agent(monster, "random")

    print(f"\nGrid:\n{env.grid.transpose()}")

    statistics: list[EpisodeStatistics] = []
    num_episodes = 100
    for episode in range(num_episodes):
        env.reset()

        done = False

        total_reward = 0

        # Get the current state
        state = State()
        playing_agent = env.get_playing_agent()
        enemy_agent = env.get_not_playing_agents()[0]
        state.update_agents_coord([playing_agent, enemy_agent])
        state.update_current_hp(playing_agent)
        state.update_damage_dealt(env.get_not_playing_agents()[0])
        state.update_attack_available(playing_agent)
        state.update_movement_available(playing_agent)
        print(f"Initial State: {state.to_array()}")

        while not done:
            # Choose an action based on the current state
            available_actions = env.get_playing_agent().available_actions(
                env.grid, env.n_squares_height, env.n_squares_width
            )
            action = chooseAction(state, available_actions)
            print(f"Episode {episode + 1}:\n\tAction: {action.name}")

            # Take the chosen action and observe the next state and reward
            next_state, reward, done = step(action, available_actions, state, env)

            learn(state, action, reward, next_state)

            total_reward += reward
            state = next_state

            print(f"\tReward: {reward}")

            # pygame.time.wait(30)

        # Save value function to a file
        with open(ql_file, "wb") as f:
            pickle.dump(q_dict, f)

        print(f"Episode {episode + 1}: Total Reward = {total_reward}")
        print(f"Won {env.get_playing_agent().id} with {env.get_playing_agent().current_hp} HP left")
        statistics.append(
            EpisodeStatistics(
                episode + 1,
                env.get_playing_agent().id,
                env.get_playing_agent().current_hp,
                total_reward,
            )
        )

    print("\n\n\nStatistics")
    for stat in statistics:
        print(
            f"Episode: {stat.episode_number}, Winner: {stat.winner}, HP_enemy: {stat.enemy_hp_remaining}, Total Reward: {stat.total_reward}"
        )
    pygame.quit()


if __name__ == "__main__":
    main()
