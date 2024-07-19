
from Environment import Environment
from MyAgentGold import  MyAgentGold
from MyAgentChest import MyAgentChest
from MyAgentStones import MyAgentStones
from Treasure import Treasure

import pygame

def loadFileConfig(nameFile) :

    file = open(nameFile)
    lines = file.readlines()
    tailleEnv = lines[1].split()
    tailleX = int(tailleEnv[0])
    tailleY = int(tailleEnv[1])
    zoneDepot = lines[3].split()
    cPosDepot =  (int(zoneDepot[0]), int(zoneDepot[1]))
    dictAgent = dict()

    env = Environment(tailleX, tailleY, cPosDepot)
    cpt = 0

    for ligne  in lines[4:] :
        ligneSplit = ligne.split(":")
        if(ligneSplit[0]=="tres"): # new treasure
            if(ligneSplit[1]=="or"):
                env.addTreasure(Treasure(1, int(ligneSplit[4])), int(ligneSplit[2]), int(ligneSplit[3]))

            elif(ligneSplit[1]=="pierres"):
                tres = Treasure(2, int(ligneSplit[4]))
                env.addTreasure(tres, int(ligneSplit[2]), int(ligneSplit[3]))
        elif(ligneSplit[0]=="AG") : #new agent
            if(ligneSplit[1]=="or"):
                id = "agent" + str(cpt)
                agent = MyAgentGold(id, int(ligneSplit[2]), int(ligneSplit[3]), env, int(ligneSplit[4]))
                dictAgent[id] = agent
                env.addAgent(agent)
                cpt = cpt +1

            elif(ligneSplit[1]=="pierres"):
                id = "agent" + str(cpt)
                agent = MyAgentStones(id, int(ligneSplit[2]), int(ligneSplit[3]), env, int(ligneSplit[4]))
                dictAgent[id] = agent
                env.addAgent(agent)
                cpt = cpt + 1

            elif (ligneSplit[1] == "ouvr"):
                id = "agent" + str(cpt)
                agent = MyAgentChest(id, int(ligneSplit[2]), int(ligneSplit[3]), env)
                dictAgent[id] = agent
                env.addAgent(agent)
                cpt = cpt + 1

    file.close()
    env.addAgentSet(dictAgent)

    return (env, dictAgent)



GOPENING_AGENT_COLOR = (128, 128, 128)  # Gray color for opening agents
GOLD_COLOR = (255, 223, 0)  # Yellow color for gold agents and gold treasures
PRECIOUS_STONE_COLOR = (0, 0, 255)  # Blue color for precious stones agents and treasures

def draw_environment(env, lAg):

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((env.tailleX * 50, env.tailleY * 50))
    pygame.display.set_caption("Environment")

    # Colors
    OPENING_AGENT_COLOR = (128, 128, 128)  # Gray color for opening agents
    GOLD_AGENT_AND_TREASURE_COLOR = (255, 215, 0)  # Yellow color for gold agents and gold treasures
    BLUE_AGENT_AND_STONE_COLOR = (0, 0, 255)  # Blue color for stone agents and treasures
    BLACK = (0, 0, 0)  # Black for grid lines
    BACKGROUND_COLOR = (255, 255, 255)  # White for background

    

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        screen.fill(BACKGROUND_COLOR)

        # Draw grid lines
        for x in range(env.tailleX):
            for y in range(env.tailleY):
                pygame.draw.rect(screen, BLACK, (x * 50, y * 50, 50, 50), 1)  # Draw grid border

        # Draw treasures
        for x in range(env.tailleX):
            for y in range(env.tailleY):
                treasure = env.grilleTres[x][y]
                if treasure is not None:
                    if treasure.type == 1:  # 1 is for gold treasures
                        color = GOLD_COLOR
                    elif treasure.type == 2:  # 2 is for stone treasures
                        color = PRECIOUS_STONE_COLOR
                    pygame.draw.rect(screen, color, (x * 50, y * 50, 50, 50))

        # Draw agents with different colors
        for id, agent in env.agentSet.items():
            x, y = agent.getPos()  # Get the agent's position
            if isinstance(agent, MyAgentGold):
                color = GOLD_COLOR
            elif isinstance(agent, MyAgentChest):
                color = OPENING_AGENT_COLOR
            elif isinstance(agent, MyAgentStones):
                color = PRECIOUS_STONE_COLOR
            else:
                color = BACKGROUND_COLOR  # Default color if agent type is unknown

            pygame.draw.circle(screen, color, (x * 50 + 25, y * 50 + 25), 20)

        # Update the display
        pygame.display.flip()




def main():
    
    env, lAg = loadFileConfig("env1.txt")
    
    
    
    # Move each grey agent towards the nearest treasure using A*
    treasures_remaining = True
    while treasures_remaining:
        treasures_remaining = False
        for x in range(env.tailleX):
            for y in range(env.tailleY):
                if env.grilleTres[x][y] is not None and not env.grilleTres[x][y].isOpen():
                    treasures_remaining = True
                    break
            if treasures_remaining:
                break

        for id, agent in lAg.items():
            if isinstance(agent, MyAgentChest):
                agent.move_to_treasure()  # this method is  implemented to move towards and open treasures. 

        
        pygame.time.delay(100)  # Delay to slow down the simulation
    # Draw the environment and agents
    draw_environment(env, lAg)

    # Print each agent's score 
    for id, agent in lAg.items():
        print(f"Agent {id} score: {agent.get_score()}")  

    print("\n\n******* TOTAL SCORE: {}".format(env.getScore()))

# Call the main function to start the simulation
main()
