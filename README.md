# The challenge (unfinished)

We consider agents who must collect all the treasures scattered in an environment.

•	The environment is represented by a grid. An agent can move from one cell to another if they are adjacent (diagonal movements are allowed). Two agents cannot occupy the same cell.

•	Treasures are distributed throughout the environment. There are 2 types of treasures: gems and gold coins. These treasures are contained in chests that must be unlocked before agents can collect the treasures (once a chest is unlocked, an agent can collect the corresponding treasure without waiting for all chests to be unlocked). To collect a treasure or unlock a chest, an agent with the proper skill must move to the cell containing the treasure and perform the desired action.

•	There are 3 different types of agents: agents who collect gold coins, agents who collect gems, and agents who unlock chests. An agent who collects gold coins cannot collect gems and vice versa. An agent who unlocks chests cannot collect any treasure.

•	Each treasure can be collected by only one agent, provided that the chest has been unlocked. Once collected, a treasure must be deposited at an identified collection point. Only the treasures deposited at this collection point are counted.

•	Each agent has a backpack capacity that corresponds to the maximum amount of treasure they can collect. If the quantity to be collected is greater than the remaining space in the backpack, the uncollected portion of the treasure is permanently lost. However, agents can unload their backpacks at the final collection point and then collect more treasures.

![image](https://github.com/user-attachments/assets/760179a9-61eb-49fc-baf4-27bfa0560e76)

## The goal

The objective of the project is to develop a distributed planning method that allows agents to coordinate the collection of treasures to maximize the quantity of treasures deposited at the collection point.

To achieve this, you will need to develop algorithms and protocols that allow the agents to:

- Divide the chests to be unlocked and the treasures to be collected (while respecting the types of agents and the capacities of their backpacks)
  
- Individually plan their actions
  
- Coordinate the individual plans in a distributed manner to obtain an efficient overall plan.
 
Note that coordination is particularly necessary to meet the constraints of non-collision (2 agents cannot be on the same cell at the same time), precedence between unlocking a chest and collecting a treasure, and to coordinate the collection.

## What I have made so far

### Allocation of Treasures and Tasks to Agents
In a multi-agent environment, task allocation is possible under the following protocols:

- Contract Net: This protocol involves a call for bids where one agent (the initiator) sends a task to several agents. These agents then submit proposals or bids. The initiator selects the most appropriate bid and assigns the task to that agent.

- Auctions: In this protocol, tasks are put up for auction, and agents bid to obtain them. There are different types of auctions, such as first-price auctions, where the agent with the highest bid wins the task, and Vickrey auctions, where the winner pays the price of the second-highest bid.

- Economic Market Simulation: In this protocol, agents act like economic entities, buying and selling tasks in a virtual market. Prices can vary based on supply and demand, thus guiding task allocation efficiently.

- Shortest Path Algorithms: In these movement methods, agents can respond to calls with proposals based on their proximity and current capacity. Essentially, the most appropriate agent closest to the goal wins the task, as they are considered the least costly.

### Task Allocation in the Project

-Task Allocation Protocol: First-price auctions, where the agent with the highest bid wins the task, are particularly suitable. Since the type or role of agents is already defined, we will just add a proximity component to the treasure, using a shortest path algorithm, and based on the agent's role, the closest agent will perform the task.

- Task Planning Methods: An approach based on heuristic search algorithms, such as A*, Greedy Best-First Search, or Dijkstra, can be used to optimize the paths of agents towards their goals. This method will be coupled with constraint-based planning to manage dependencies between tasks, such as the need to unlock a chest before collecting the treasure.

- Distributed Coordination Methods: We will use event-based communication, such as the announcement of the discovery of a treasure or the unlocking of a chest.

### Methodology and Program Structure

We have a base class MyAgent, which serves as a superclass for the different types of agents (gold, gems, chests). The MyAgent class includes key methods such as agent movements, agent type, position, agent messaging, as well as the method for movement and decision-making on which task to undertake.

- Environment.py: Defines the environment in which the agents operate. It is responsible for creating the environment grid, managing the locations of treasures and gems, and updating the state of the environment based on the actions of the agents.

- Main.py: Initializes the environment, draws the agents and treasures with pygame, and starts the simulation process. It controls the main flow of the program, including the simulation loop where agents act in the environment.

- MyAgent.py: This module defines the base class for agents. It includes methods and attributes common to all types of agents in the system, such as methods for moving the agent and collecting treasures.

- MyAgentChest.py, MyAgentGold.py, MyAgentStones.py: These define specific subclasses of the base agent class (MyAgent). Each subclass represents a type of agent with specializations, for example, an agent specialized in collecting chests, gold, or gems. These subclasses can override methods of the base class to implement behavior specific to their specialization.

- Treasure.py: This module manages the treasures (gold, gems, chests) in the environment. It defines the structure and behavior of treasure objects that agents can collect.

### Individual Planning of Agents
For each agent's plan, once they know their function, their movements are based on the A* algorithm.

### Why choose A?*
![image](https://github.com/user-attachments/assets/71b199b9-6936-4a3c-ad47-619d5024aa46)

### Results so far (opens the first 2 chests)
![image](https://github.com/user-attachments/assets/c59cd65d-18b2-400d-9328-2243075c9319)

- In gray: These are the agents who unlock chests.

- In blue: These are the agents who collect gems. Agents are represented as circles, and treasures are represented as squares.
  
- In yellow: These are the agents who collect gold. Agents are represented as circles, and treasures are represented as squares.

  ![image](https://github.com/user-attachments/assets/d6cca1cc-a397-4a27-a2b7-d79e32c252c0)
  
  ![image](https://github.com/user-attachments/assets/42d69ba7-4ce2-4a65-bb94-38ad425557eb)

  ### Other alternative 
With the "code_MODIFIE_v8.py" file, we get this result: 

![image](https://github.com/user-attachments/assets/cb602a7e-3757-4544-bbef-fab655e6d26f)

![image](https://github.com/user-attachments/assets/c79f9b94-9cb8-4ca1-8e1f-884c4225b0d4)

![image](https://github.com/user-attachments/assets/6bade8eb-a52a-4349-a1fd-131972cc9e57)

Here the agents are in green without distinguision, the gems are in red, and the gold is in yellow. The collection point is in blue.

### To be continued...



