import pygame
import yaml

import logging, os

logging.disable(logging.WARNING)  # disable TF logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from ActionSelection import ActionSelection
from Config import Config
from State import State
from agent_interfaces.HasAttack import HasAttack
from algorithms.Algorithm import Algorithm
from algorithms.DQN import DQN
from algorithms.Q_Learning import Q_Learning
from combat_actions.Attack import Attack
from combat_actions.CombatActions import CombatAction

from Agent import Monster, Player
from DnDEnvironment import DnDEnvironment
from Statistics import EpisodeStats, StatSaver


##########################################


def step(action: CombatAction, available_actions, state: State, env: DnDEnvironment):
    OLD_playing_agent = env.get_playing_agent()
    OLD_enemy_agent = env.get_not_playing_agents()[0]

    # Take Action
    env.takeAction(action)

    # New State
    new_state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])

    # !!!
    # FOR THE ENVIRONMENT AND THE AGENTS, FROM NOW WE ARE IN THE NEXT STATE
    # !!!

    # Reward
    # Check if the enemy (of the old state) is dead (now in the new state)
    if not env.get_agent_byID(OLD_enemy_agent.id).is_alive():
        reward = 10
        done = True

    # Check if the enemy (of the old state) had more hp that now (now in the new state), i.e. it took damage
    elif OLD_enemy_agent.current_hp > env.get_agent_byID(OLD_enemy_agent.id).current_hp:
        reward = 3
        done = False

    # Check if the agent took the EndTurn action but still he could made an attack (number of attaks left > 0 AND if it had an Attack action available)
    elif (
        action.name == "EndTurn"  # if took EndTurn action
        and (
            OLD_playing_agent.is_attack_available() > 0 if isinstance(OLD_playing_agent, HasAttack) else False
        )  # if it had attacks left
        and any(isinstance(a, Attack) for a in available_actions)  # if it had an Attack action available
    ):
        reward = -5
        done = False

    # Otherwise
    else:
        reward = 0
        done = False

    return new_state, reward, done


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
        config.player.name,
        config.player.picture_path,
        config.player.max_hp,
        config.player.movement_speed,
        config.player.attack_damage,
        config.player.attacks_max_number,
        config.RENDER.mode,
    )
    monster = Monster(
        config.monster.name,
        config.monster.picture_path,
        config.monster.max_hp,
        config.monster.movement_speed,
        config.monster.attack_damage,
        config.monster.attacks_max_number,
        config.RENDER.mode,
    )

    # Place agents into the environment
    env.place_agent(player, config.player.default_coordinates)
    env.place_agent(monster, config.monster.default_coordinates)

    # Take algorithm from config
    if config.algorithm.name == config.Q_Learning.name:
        algorithm: Algorithm = Q_Learning(config.Q_Learning)
    elif config.algorithm.name == config.DQN.name:
        all_actions = env.get_all_actions()
        state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])
        algorithm: Algorithm = DQN(config.DQN, all_actions, len(state.to_array()))

    # Statistics
    stat_saver = StatSaver(config.algorithm.statistics_filename)

    # Action Selection
    action_selection = ActionSelection(config.algorithm.EPSILON, config.algorithm.EPSILON_rateDecay)

    ########################################################################
    # Episodes loop
    for episode in range(config.num_episodes):
        # Statistics and render
        statistics = EpisodeStats([player.name, monster.name], stat_saver.get_episode_number())
        if config.RENDER.mode == "human":
            pygame.display.set_caption(f"Episode {episode + 1}")

        # Environment reset
        env.reset()

        done = False  # If the episode is concluded

        # Current state
        state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])

        ####################################################################
        # Steps loop
        while not done:
            print(
                f"Episode {episode+1}/{config.num_episodes} progess: %",
                (
                    max(
                        100 - (100 * env.get_playing_agent().current_hp / env.get_playing_agent().max_hp),
                        100
                        - (100 * env.get_not_playing_agents()[0].current_hp / env.get_not_playing_agents()[0].max_hp),
                    )
                ),
                end="\r",
            )
            # Get available actions for the playing agent
            available_actions = env.get_playing_agent().available_actions(
                env.grid, env.n_squares_height, env.n_squares_width
            )
            # Choose action
            action = action_selection.epsilon_greedy(
                state,
                available_actions,
                algorithm,
            )

            # Take the chosen action and observe the next state and reward
            next_state, reward, done = step(action, available_actions, state, env)

            # Learning phase
            algorithm.learn(state, action, reward, next_state, done)

            # Change state
            state = next_state

            # Statistics and render
            statistics.actions_taken[env.get_playing_agent().name].append(action.name)
            statistics.total_reward += reward
            if config.RENDER.mode == "human":
                pygame.time.wait(config.RENDER.wait_timestep_ms)

        # Statistics
        statistics.winner_name = env.get_playing_agent().name
        statistics.winner_hp_remaining = env.get_playing_agent().current_hp
        stat_saver.add_episode(statistics)

        # Save value function and statistics
        if (episode + 1) % config.saving_freq == 0:
            algorithm.save_value_function(config.algorithm.pickle_filename)
            stat_saver.save_statistics()

    # Save in case of not saved in the loop
    if config.num_episodes % config.saving_freq != 0:
        algorithm.save_value_function(config.algorithm.pickle_filename)
        stat_saver.save_statistics()

    if config.RENDER.mode == "human":
        pygame.quit()


if __name__ == "__main__":
    main()
