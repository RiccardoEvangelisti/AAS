import pygame
import yaml

import logging, os

logging.disable(logging.WARNING)  # disable TF logging
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from Config import Config
from State import State
from agent_interfaces.HasAttack import HasAttack
from agent_interfaces.HasMovement import HasMovement
from algorithms.Algorithm import Algorithm
from algorithms.DQN import DQN
from algorithms.Q_Learning import Q_Learning
from algorithms.Random import Random
from algorithms.RuleBased import RuleBased
from combat_actions.Attack import Attack
from combat_actions.CombatActions import CombatAction

from Agent import Monster, Player
from DnDEnvironment import DnDEnvironment
from Statistics import EpisodeStats, StatSaver


##########################################


def step(action: CombatAction, available_actions, state: State, env: DnDEnvironment):
    OLD_playing_agent = env.get_playing_agent()
    OLD_playing_agent_coord = OLD_playing_agent.coordinates
    OLD_playing_agent_movement_left = (
        OLD_playing_agent.movement_left if isinstance(OLD_playing_agent, HasMovement) else 0
    )
    OLD_playing_agent_is_attack_available = (
        OLD_playing_agent.is_attack_available() > 0 if isinstance(OLD_playing_agent, HasAttack) else False
    )

    OLD_enemy_agent = env.get_not_playing_agents()[0]
    OLD_enemy_agent_HP = OLD_enemy_agent.current_hp
    OLD_enemy_agent_coord = OLD_enemy_agent.coordinates

    # Take Action
    env.takeAction(action)

    # New State
    new_state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])

    # !!!
    # FOR THE ENVIRONMENT AND THE AGENTS, FROM NOW ON WE ARE IN THE NEXT STATE
    # !!!

    # Rewards:

    #######################
    # Check if the enemy (of the old state) is dead (now in the new state)
    if not OLD_enemy_agent.is_alive():
        reward = 10
        done = True
        return new_state, reward, done

    #######################
    # Check if the enemy (of the old state) had more hp that now (now in the new state), i.e. it took damage
    if OLD_enemy_agent_HP > OLD_enemy_agent.current_hp:
        reward = 4
        done = False
        return new_state, reward, done

    #######################
    # Check if the agent took the EndTurn action but still he could made an attack (number of attaks left > 0 AND if it had an Attack action available)
    if config.advanced_reward:
        if (
            action.name == "EndTurn"  # if took EndTurn action
            and OLD_playing_agent_is_attack_available  # if it had attacks left
            and any(isinstance(a, Attack) for a in available_actions)  # if it had an Attack action available
        ):
            reward = -5
            done = False
            return new_state, reward, done

        #######################
        # Check if the agent took the EndTurn action but still has movement to go in range for an attack
        max_range = 0
        # Take the maximum range of the all attacks that the agent is capable of
        for _a in OLD_playing_agent.combatActions.values():
            if isinstance(_a, Attack):
                if _a.attack_range > max_range:
                    max_range = _a.attack_range
        chebyshev_distance = max(
            abs(OLD_playing_agent_coord[0] - OLD_enemy_agent_coord[0]),
            abs(OLD_playing_agent_coord[1] - OLD_enemy_agent_coord[1]),
        )
        if (
            action.name == "EndTurn"  # if took EndTurn action
            and OLD_playing_agent_is_attack_available  # if it had attacks left
            and chebyshev_distance - max_range <= OLD_playing_agent_movement_left
        ):
            reward = -3
            done = False
            return new_state, reward, done

    #######################
    # Otherwise
    reward = 0
    done = False
    return new_state, reward, done


#####################################


def setAlgorithm(algorithm, env: DnDEnvironment) -> Algorithm:
    # Take algorithms from config
    if algorithm.name == config.Q_Learning.name:
        return Q_Learning(config.Q_Learning)
    elif algorithm.name == config.DQN.name:
        state = State(env.get_playing_agent(), env.get_not_playing_agents()[0])
        return DQN(config.DQN, env.get_all_actions(), len(state.to_array()))
    elif algorithm.name == config.Random.name:
        return Random(config.Random)
    elif algorithm.name == config.RuleBased.name:
        return RuleBased(config.RuleBased, env)
    else:
        raise Exception(f"Algorithm '{algorithm}' not found in config")


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

    player.algorithm = setAlgorithm(config.player.algorithm, env)
    monster.algorithm = setAlgorithm(config.monster.algorithm, env)

    player_algorithm_filename = config.player.algorithm.pickle_filename + "_" + config.train_code + ".pkl"
    monster_algorithm_filename = config.monster.algorithm.pickle_filename + "_" + config.train_code + ".pkl"

    # Statistics
    stat_saver = StatSaver(config.statistics_filename, config.saving_freq)

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
            playing_agent = env.get_playing_agent()
            print(
                f"Episode {episode+1}/{config.num_episodes} progess: %",
                (
                    max(
                        100 - (100 * playing_agent.current_hp / playing_agent.max_hp),
                        100
                        - (100 * env.get_not_playing_agents()[0].current_hp / env.get_not_playing_agents()[0].max_hp),
                    )
                ),
                end="\r",
            )
            # Get available actions for the playing agent
            available_actions = playing_agent.available_actions(env.grid, env.n_squares_height, env.n_squares_width)
            # Choose action
            action = playing_agent.algorithm.epsilon_greedy(state, available_actions)

            # Take the chosen action and observe the next state and reward
            next_state, reward, done = step(action, available_actions, state, env)

            # Learning phase
            playing_agent.algorithm.learn(state, action, reward, next_state, done, env=env)

            # Change state
            state = next_state

            # Statistics and render
            statistics.step_stats.append((playing_agent.name, action.name, reward))
            if config.RENDER.mode == "human":
                pygame.time.wait(config.RENDER.wait_timestep_ms)

        # Statistics
        statistics.winner_name = playing_agent.name
        statistics.winner_hp_remaining = playing_agent.current_hp
        stat_saver.add_episode(statistics)

        # Save value functions
        if (episode + 1) % config.saving_freq == 0:
            player.algorithm.save_value_function(player_algorithm_filename)
            monster.algorithm.save_value_function(monster_algorithm_filename)

    # Save in case of not saved in the loop
    if config.num_episodes % config.saving_freq != 0:
        player.algorithm.save_value_function(player_algorithm_filename)
        monster.algorithm.save_value_function(monster_algorithm_filename)
        stat_saver.save_statistics()

    if config.RENDER.mode == "human":
        pygame.quit()


if __name__ == "__main__":
    main()
