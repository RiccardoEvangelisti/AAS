import os
import pickle
import random
import pygame
import yaml

from Config import Config
from State import State
from combat_actions.Attack import Attack
from combat_actions.CombatActions import CombatAction

from Agent import Monster, Player
from DnDEnvironment import DnDEnvironment
from Statistics import EpisodeStatistics, Statistics


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
    new_state = state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])
    print(f"\tNew State: {new_state.to_array()}")

    return new_state, reward, done


######################################


# Load value function from a file
ql_file = "outputs/q_learning_values.pkl"
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
    if random.random() < config.Q_learning.EPSILON:
        return random.choice(available_actions)

    # Exploit
    state_bytes = state.to_bytes()

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
    q_value_current = q_dict.get((state.to_bytes(), action), 0)
    # Take the state-action pairs that match the next_state
    q_filtered = dict(filter(lambda item: item[0][0] == next_state.to_bytes(), q_dict.items()))

    # Get the highest q-value for the next_state
    max_q_value_next = max(q_filtered.values()) if q_filtered else 0

    # Update the Q-value for the current state-action pair
    q_dict[(state.to_bytes(), action.name)] = q_value_current + config.Q_learning.ALPHA * (
        reward + config.Q_learning.GAMMA * max_q_value_next - q_value_current
    )


#####################################


def main():

    # Load config file
    with open("config.yml", "r") as file:
        global config
        config = Config(yaml.safe_load(file.read()))

    # Create the environment
    env = DnDEnvironment(
        n_squares_width=config.n_squares_width,
        n_squares_height=config.n_squares_height,
        _RENDER_MODE=config.RENDER.mode,
    )

    # Create the agents
    player = Player(
        config.player.picture_path,
        config.player.max_hp,
        config.player.movement_speed,
        config.player.attack_damage,
        config.player.attacks_max_number,
    )
    monster = Monster(
        config.monster.picture_path,
        config.monster.max_hp,
        config.monster.movement_speed,
        config.monster.attack_damage,
        config.monster.attacks_max_number,
    )

    # Place agents into the environment
    env.place_agent(player, config.player.default_coordinates)
    env.place_agent(monster, config.monster.default_coordinates)

    # Initialize statistics
    stat = Statistics()

    # Episodes loop
    for episode in range(config.num_episodes):
        # Statistics and render
        total_reward = 0
        if config.RENDER.mode == "human":
            pygame.display.set_caption(f"Episode {episode + 1}")

        # Environment reset
        env.reset()

        done = False  # If the episode is concluded

        # Initialize the current state
        state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])

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

            if config.RENDER.mode == "human":
                pygame.time.wait(config.RENDER.wait_timestep_ms)

        # Save value function to a file
        with open(ql_file, "wb") as f:
            pickle.dump(q_dict, f)

        print(f"Episode {episode + 1}: Total Reward = {total_reward}")
        print(f"Won {env.get_playing_agent().id} with {env.get_playing_agent().current_hp} HP left")
        stat.episode_statistics.append(
            EpisodeStatistics(
                episode + 1,
                env.get_playing_agent().id,
                env.get_playing_agent().current_hp,
                total_reward,
            )
        )

    print("\n\n\nStatistics")
    for stat in stat.episode_statistics:
        print(
            f"Episode: {stat.episode_number}, Winner: {stat.winner}, HP_enemy: {stat.enemy_hp_remaining}, Total Reward: {stat.total_reward}"
        )
    pygame.quit()


if __name__ == "__main__":
    main()
