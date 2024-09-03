import pygame
import numpy as np
import random

# Initialize Pygame
pygame.init()

# Grid settings
GRID_SIZE = 10
CELL_SIZE = 60
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
pygame.display.set_caption("D&D Reinforcement Learning")

class Agent:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self, dx, dy):
        new_x = (self.x + dx) % GRID_SIZE
        new_y = (self.y + dy) % GRID_SIZE
        self.x, self.y = new_x, new_y

    def draw(self):
        pygame.draw.circle(screen, self.color, 
                           (self.x * CELL_SIZE + CELL_SIZE // 2, 
                            self.y * CELL_SIZE + CELL_SIZE // 2), 
                           CELL_SIZE // 3)

class Environment:
    def __init__(self):
        self.player = Agent(0, 0, BLUE)
        self.monster = Agent(GRID_SIZE - 1, GRID_SIZE - 1, RED)

    def update_player_position(self, x, y):
        self.player.x = x % GRID_SIZE
        self.player.y = y % GRID_SIZE

    def update_monster_position(self, x, y):
        self.monster.x = x % GRID_SIZE
        self.monster.y = y % GRID_SIZE

    def draw_grid(self):
        screen.fill(WHITE)
        for x in range(0, GRID_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (x, 0), (x, GRID_HEIGHT))
        for y in range(0, GRID_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, BLACK, (0, y), (GRID_WIDTH, y))

    def draw_agents(self):
        self.player.draw()
        self.monster.draw()

    def draw(self):
        self.draw_grid()
        self.draw_agents()
        pygame.display.flip()


class State:
    def __init__(self, player_x, player_y, monster_x, monster_y):
        self.player_x = player_x
        self.player_y = player_y
        self.monster_x = monster_x
        self.monster_y = monster_y

    def to_array(self):
        return np.array([self.player_x, self.player_y, self.monster_x, self.monster_y])

class QLearningAgent:
    def __init__(self, action_space, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.q_table = {}
        self.action_space = action_space
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.action_space)
        else:
            q_values = [self.get_q_value(state, a) for a in self.action_space]
            max_q = max(q_values)
            actions_with_max_q = [a for a, q in zip(self.action_space, q_values) if q == max_q]
            return random.choice(actions_with_max_q)

    def learn(self, state, action, reward, next_state):
        current_q = self.get_q_value(state, action)
        next_max_q = max([self.get_q_value(next_state, a) for a in self.action_space])
        new_q = current_q + self.lr * (reward + self.gamma * next_max_q - current_q)
        self.q_table[(state, action)] = new_q

def initial_state():
    return State(0, 0, GRID_SIZE - 1, GRID_SIZE - 1)

def get_player_position(state):
    return state.player_x, state.player_y

def get_monster_position(state):
    return state.monster_x, state.monster_y

def step(state, action):
    # Define possible moves: up, down, left, right
    moves = {
        0: (0, -1),  # up
        1: (0, 1),   # down
        2: (-1, 0),  # left
        3: (1, 0)    # right
    }
    
    dx, dy = moves[action]
    new_player_x = (state.player_x + dx) % GRID_SIZE
    new_player_y = (state.player_y + dy) % GRID_SIZE
    
    # Simple monster AI: move towards the player
    monster_dx = np.sign(new_player_x - state.monster_x)
    monster_dy = np.sign(new_player_y - state.monster_y)
    new_monster_x = (state.monster_x + monster_dx) % GRID_SIZE
    new_monster_y = (state.monster_y + monster_dy) % GRID_SIZE
    
    new_state = State(new_player_x, new_player_y, new_monster_x, new_monster_y)
    
    # Define reward structure
    if (new_player_x, new_player_y) == (new_monster_x, new_monster_y):
        reward = -10  # Player caught by monster
        done = True
    elif (new_player_x, new_player_y) == (GRID_SIZE - 1, GRID_SIZE - 1):
        reward = 10  # Player reached the goal (opposite corner)
        done = True
    else:
        reward = -1  # Small negative reward for each step to encourage efficiency
        done = False
    
    return new_state, reward, done

def main():
    env = Environment()
    agent = QLearningAgent(action_space=[0, 1, 2, 3])  # up, down, left, right
    num_episodes = 1000
    
    for episode in range(num_episodes):
        state = initial_state()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.choose_action(state.to_array().tobytes())
            next_state, reward, done = step(state, action)
            
            # Update graphics
            env.update_player_position(next_state.player_x, next_state.player_y)
            env.update_monster_position(next_state.monster_x, next_state.monster_y)
            env.draw()
            
            # RL agent learning
            agent.learn(state.to_array().tobytes(), action, reward, next_state.to_array().tobytes())
            
            total_reward += reward
            state = next_state
            
            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            
            pygame.time.wait(100)  # Add a small delay to make the visualization visible
        
        print(f"Episode {episode + 1}: Total Reward = {total_reward}")
    
    pygame.quit()

if __name__ == "__main__":
    main()