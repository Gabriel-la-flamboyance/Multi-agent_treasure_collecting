# -*- coding: utf-8 -*-


import pygame
import numpy as np
from queue import PriorityQueue
import matplotlib.pyplot as plt
import math
import random

# Constants
SCREEN_SIZE = (600, 600)
CELL_SIZE = 50
GRID_OFFSET_X = 50
GRID_OFFSET_Y = 50
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Agent:
    def __init__(self, name, position, skill, backpack_capacity, id):
        self.name = name
        self.position = position
        self.id = id
        self.skill = skill
        self.backpack_capacity = backpack_capacity
        self.backpack_contents = []

    def unload_backpack(self, environment):
        if self.position == environment.collection_point:
            environment.deposited_treasures.extend(self.backpack_contents)
            self.backpack_contents = []
            print(f"{self.name} unloaded backpack at collection point.")
        else:
            print(f"{self.name} cannot unload backpack. Not at collection point.")

    def has_tasks_assigned(self):
        return bool(self.backpack_contents)

class GoldCoinAgent(Agent):
    def __init__(self, name, position, backpack_capacity, id):
        super().__init__(name, position, skill="or", backpack_capacity=backpack_capacity, id=id)


class GemAgent(Agent):
    def __init__(self, name, position, backpack_capacity, id):
        super().__init__(name, position, skill="pierres", backpack_capacity=backpack_capacity, id=id)


class ChestOpenerAgent(Agent):
    def __init__(self, name, position, backpack_capacity, id):
        super().__init__(name, position, skill="ouvr", backpack_capacity=backpack_capacity, id=id)

class Treasure:
    def __init__(self, value, position, treasure_type):
        self.value = value
        self.position = position
        self.treasure_type = treasure_type
        self.unlocked = False
        self.deposited = False

    def __str__(self):
        return f"{self.treasure_type} at position {self.position}"

class Environment:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.treasures = []
        self.collection_point = (0, size // 2)
        self.deposited_treasures = []

    def add_agent(self, agent):
        x, y = agent.position
        if self.grid[x][y] is None:
            self.grid[x][y] = agent
            return True
        else:
            print("Position already occupied.Cannot place agent. ")
            return False

    def add_treasure(self, treasure):
        x, y = treasure.position
        if self.grid[x][y] is None:
            self.grid[x][y] = treasure
            self.treasures.append(treasure)
            return True
        else:
            print("Position already occupied. Cannot place treasure.")
            return False

    def move_agent(self, agent, new_position):
        old_x, old_y = agent.position
        new_x, new_y = new_position
        if self.is_valid_position(new_x, new_y) and self.grid[new_x][new_y] is None:
            self.grid[old_x][old_y] = None
            self.grid[new_x][new_y] = agent
            agent.position = new_position
            return True
        else:
            print("Invalid move. Cannot move to specified position.")
            return False

    def unlock_treasure(self, agent, treasure):
        if agent.skill == treasure.treasure_type:
            treasure.unlocked = True
            print(f"{agent.name} unlocked the treasure chest at position {treasure.position}.")
            return True
        else:
            print(f"{agent.name} does not have the required skill to unlock this treasure chest.")
            return False

    def deposit_treasure(self, agent, treasure):
        if treasure in self.treasures and treasure.unlocked and not treasure.deposited:
            if isinstance(agent, ChestOpenerAgent) or agent.skill == treasure.treasure_type:
                if len(agent.backpack_contents) < agent.backpack_capacity:
                    treasure.deposited = True
                    agent.backpack_contents.append(treasure)
                    print(f"{agent.name} collected {treasure.value} units of treasure.")
                    return True
                else:
                    print(f"{agent.name}'s backpack is full. Cannot collect more treasure.")
                    return False
            else:
                print(f"{agent.name} cannot deposit treasure. Skill mismatch.")
                return False
        return False

    def is_valid_position(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size

    def display_environment(self):
        grid_data = np.zeros((self.size, self.size, 3), dtype=int)
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.grid[i][j], Agent):
                    grid_data[i][j] = [0, 255, 0]  # Green color for agents
                elif isinstance(self.grid[i][j], Treasure):
                    if self.grid[i][j].treasure_type == "pierres":
                        grid_data[i][j] = [255, 0, 0]  # Red color for gems
                    elif self.grid[i][j].treasure_type == "or":
                        grid_data[i][j] = [255, 255, 0]  # Yellow color for gold coins
                    elif self.grid[i][j].treasure_type == "ouvr":
                        grid_data[i][j] = [0, 0, 255]  # Blue color for chest treasures
                elif (i, j) == self.collection_point:
                    grid_data[i][j] = [0, 0, 255]  # Blue color for collection point

        plt.imshow(grid_data)
        plt.title("Environment Grid")
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.xticks(range(self.size))
        plt.yticks(range(self.size))
        plt.grid(color='lightgray', linestyle='-', linewidth=0.5)  # Light gray grid lines
        plt.show()

# Function to find the nearest agent
def find_nearest_agent(env, target_position, agents):
    distances = [manhattan_distance(agent.position, target_position) for agent in agents]
    closest_agent_index = distances.index(min(distances))
    return agents[closest_agent_index]


# Calculate Manhattan distance between two points
def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

# A* pathfinding algorithm
def astar_search(env, start, goal):
    def heuristic(node):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    def reconstruct_path(came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        return path[::-1]

    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            return reconstruct_path(came_from, goal)

        for dx, dy in DIRECTIONS:
            next_node = (current[0] + dx, current[1] + dy)
            new_cost = cost_so_far[current] + 1

            if (
                env.is_valid_position(*next_node)
                and env.grid[next_node[0]][next_node[1]] is None
                and next_node not in [treasure.position for treasure in env.treasures]
            ):

                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(next_node)
                    frontier.put(next_node, priority)
                    came_from[next_node] = current

    return None

# Function to simulate the opening of a chest treasure
def open_treasure(agent, treasure):
    treasure.unlocked = True
    print(f"{agent.name} {agent.id} opened the treasure chest at position {treasure.position}.")


def distribute_tasks(env, agents):
    assigned_tasks = []
    for treasure in env.treasures:
        # if treasure.treasure_type == "ouvr":
            opener_agents = [agent for agent in agents if isinstance(agent, ChestOpenerAgent)]
            if opener_agents:
                assigned_agent = find_nearest_agent(env, treasure.position, opener_agents)
                if assigned_agent:
                    assigned_agent.backpack_contents.append(treasure)
                    assigned_tasks.append([assigned_agent, treasure])
                    print(f"{assigned_agent.name} {assigned_agent.id} assigned to open the chest at position {treasure.position}.")
                else:
                    print(f"No suitable ChestOpenerAgent found to open the chest at position {treasure.position}.")
            else:
                print("No ChestOpenerAgent available to open the chest.")
    print()


    if len(assigned_tasks) > 0:
        for i in assigned_tasks:
            # path = astar_search(env, i[0].position, i[1].position)
            # if path:
            #     for position in path[1:]:
            #         env.move_agent(i[0], position)
            #         pygame.time.wait(500)

                open_treasure(i[0], i[1])
    else:
        print("No agent assigned to open a chest.")

    print()

    for treasure in env.treasures:
        if not treasure.treasure_type == "ouvr":
            # nearest_agent = find_nearest_agent(env, treasure.position, agents)
            nearest_agent = find_nearest_agent_with_skill(env, treasure.position, treasure.treasure_type, agents)
            if nearest_agent:
                nearest_agent.backpack_contents.append(treasure)
                print(f"{nearest_agent.name} {nearest_agent.id} assigned to collect {treasure.treasure_type} at position {treasure.position}.")
            else:
                print(f"No suitable agent found to collect {treasure.treasure_type} at position {treasure.position}.")

                # Add a placeholder "waiting" treasure if collection point is free
                if env.grid[env.collection_point[0]][env.collection_point[1]] is None:
                    env.add_treasure(Treasure(0, env.collection_point, "waiting"))
                else:
                    print("Position already occupied. Cannot place treasure.")

    # Ensure that every agent has a task assigned
    for agent in agents:
        if not agent.has_tasks_assigned():
            print(f"No task assigned for {agent.name} {agent.id}. Waiting for a suitable task.")
            if env.grid[env.collection_point[0]][env.collection_point[1]] is None:
                env.add_treasure(Treasure(0, env.collection_point, "waiting"))
            else:
                print("Position already occupied. Cannot place treasure.")



# Function to find the nearest agent with a specific skill
def find_nearest_agent_with_skill(env, target_position, skill, agents):
    skill_agents = [agent for agent in agents if isinstance(agent, (GoldCoinAgent, GemAgent, ChestOpenerAgent)) and agent.skill == skill]
    if skill_agents:
        distances = [manhattan_distance(agent.position, target_position) for agent in skill_agents]
        closest_agent_index = distances.index(min(distances))
        return skill_agents[closest_agent_index]
    else:
        return None

def create_environment(env_config):
    size = int(env_config[0].split()[0])
    env = Environment(size)

    # Add treasures and agents
    for item in env_config[2:]:
        if item.startswith("tres:"):
            _, treasure_type, pos_x, pos_y, value = item.split(":")
            treasure = Treasure(int(value), (int(pos_x), int(pos_y)), treasure_type)
            env.add_treasure(treasure)
        elif item.startswith("AG:"):
            _, skill, pos_x, pos_y, capacity = item.split(":")
            agent = None
            if skill == "ouvr":
                agent = ChestOpenerAgent(f"Agent_{skill}", (int(pos_x), int(pos_y)), int(capacity), env_config.index(item))
            elif skill == "pierres":
                agent = GemAgent(f"Agent_{skill}", (int(pos_x), int(pos_y)), int(capacity), env_config.index(item))
            elif skill == "or":
                agent = GoldCoinAgent(f"Agent_{skill}", (int(pos_x), int(pos_y)), int(capacity), env_config.index(item))
            env.add_agent(agent)

    return env

# Algorithm to plan actions for each agent
def plan_actions(env, agent):
    for i in agent.backpack_contents:
        task = i
        path = astar_search(env, agent.position, task.position)
        if path:
            for position in path[1:]:
                env.move_agent(agent, position)
                pygame.time.wait(500)  # Adjust speed of movement
        env.deposit_treasure(agent, task)

def main():
    # Environment configuration
    env_config = [
        "12 12",
        "5 0",
        "tres:or:2:10:2",
        "tres:pierres:3:1:3",
        "tres:or:4:8:2",
        "tres:pierres:4:11:6",
        "tres:or:6:3:6",
        "tres:pierres:7:0:2",
        "tres:pierres:7:9:3",
        "tres:or:10:2:8",
        "tres:or:10:7:8",
        "tres:or:11:10:2",
        "AG:ouvr:7:4:10",
        "AG:ouvr:9:9:10",
        "AG:pierres:5:2:9",
        "AG:pierres:5:6:15",
        "AG:or:6:7:6",
        "AG:or:10:5:17"
    ]

    env = create_environment(env_config)
    agents = [agent for row in env.grid for agent in row if isinstance(agent, Agent)]

    # Distribute tasks to agents
    distribute_tasks(env, agents)

    print()

    for agent in agents:
        plan_actions(env, agent)

    print()

    # Display environment
    env.display_environment()


if __name__ == "__main__":
    main()

