
import Environment
import heapq

class MyAgent:


    def __init__(self, id, initX, initY, env:Environment):
        self.id = id
        self.posX = initX
        self.posY = initY
        self.env = env
        self.mailBox = []

    #two agents are equals if they have the same id
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.getId() == self.getId()
        return False


    #make the agent moves from (x1,y1) to (x2,y2)
    def move(self, x1, y1, x2, y2):
        if x1 == self.posX and y1 == self.posY:
            print("departure position OK")
            if self.env.move(self, x1, y1, x2, y2):
                self.posX = x2
                self.posY = y2
                print("deplacement OK")
                return 1
        return -1

    #return the id of the agent
    def getId(self):
        return self.id

    #return the position of the agent
    def getPos(self):
        return (self.posX, self.posY)

    # add a message to the agent's mailbox
    def receive(self, idReceiver, textContent):
        self.mailBox.append((idReceiver, textContent))

    #the agent reads a message in her mailbox (FIFO mailbox)
    #return a tuple (id of the sender, message  text content)
    def readMail (self):
        idSender, textContent = self.mailBox.pop(0)
        print("mail received from {} with content {}".format(idSender,textContent))
        return (idSender, textContent)


    #send a message to the agent whose id is idReceiver
    # the content of the message is some text
    def send(self, idReceiver, textContent):
        self.env.send(self.id, idReceiver, textContent)



    def __str__(self):
        res = self.id + " ("+ str(self.posX) + " , " + str(self.posY) + ")"
        return res


    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def a_star(self, start, goal):
        open_set = set([start])
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}
        visited = set()  # Track visited nodes

        while open_set:
            current = min(open_set, key=lambda x: f_score[x])
            visited.add(current)  # Mark current as visited

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                return path[::-1]  # Return reversed path

            open_set.remove(current)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (current[0] + dx, current[1] + dy)
                if neighbor in visited:  # Skip visited neighbors
                    continue

                tentative_g_score = g_score[current] + 1
                if 0 <= neighbor[0] < self.env.tailleX and 0 <= neighbor[1] < self.env.tailleY and \
                self.env.grilleAgent[neighbor[0]][neighbor[1]] is None:
                    if neighbor not in open_set or tentative_g_score < g_score.get(neighbor, float('inf')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        open_set.add(neighbor)

        return []  # No path found
    
    
    def find_nearest_treasure(self):
        my_position = self.getPos()
        min_distance = float('inf')
        nearest_treasure_pos = None
        for x in range(self.env.tailleX):
            for y in range(self.env.tailleY):
                treasure = self.env.grilleTres[x][y]
                if treasure is not None and not treasure.isOpen():
                    distance = abs(x - my_position[0]) + abs(y - my_position[1])
                    if distance < min_distance:
                        min_distance = distance
                        nearest_treasure_pos = (x, y)
        return nearest_treasure_pos
    

    def move_to_treasure(self):
        nearest_treasure = self.find_nearest_treasure()
        if not nearest_treasure:
            print("No nearest treasure found. All treasures might be opened or unreachable.")
            return

        path = self.a_star(self.getPos(), nearest_treasure)
        if not path or len(path) <= 1:
            print("No path found to the nearest treasure. Cannot proceed.")
            return

        for next_pos in path[1:]:  # Skip the current position
            success = self.env.move(self, self.posX, self.posY, next_pos[0], next_pos[1])
            if not success:
                print("Invalid move attempted or blocked path. Stopping move to treasure.")
                break  # Exit on failed move
            print(f"Movement successful to {next_pos}")

        # Attempt to open treasure if reached
        if (self.posX, self.posY) == nearest_treasure:
            self.env.open(self, self.posX, self.posY)

            
    def move_to_target(self, targetX, targetY):
        path = self.a_star((self.posX, self.posY), (targetX, targetY))
        if path and len(path) > 1:
            # Move to the next step in the path
            next_step = path[1]  # path[0] is the current position, so we take the next step
            self.move(self.posX, self.posY, next_step[0], next_step[1])
   