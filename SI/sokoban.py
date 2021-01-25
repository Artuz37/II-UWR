import queue
import heapq

def init():
    chests = set()
    goals = set()
    walls = set()
    file = open("test3.txt")
    lines = file.readlines()
    i = 0
    for y in lines:
        j = 0
        for x in y:
            if x == 'K':
                player_pos = (j, i)
            elif x == 'W':
                walls.add((j, i))
            elif x == 'B':
                chests.add((j, i))
            elif x == 'G':
                goals.add((j, i))
            elif x == '*':
                goals.add((j, i))
                chests.add((j, i))
            #print(chests, goals)
            j += 1
        i += 1

    return walls, chests, goals, player_pos

class state:
    def __init__(self, walls, boxes, goals, player, moves):
        self.walls = walls
        self.boxes = boxes
        self.goals = goals
        self.player = player
        self.moves = moves

    def win(self):
        return self.boxes == self.goals

    def legal_move(self):
        res = []
        vec = [["R", 1, 0], ["D", 0, 1], ["L", -1, 0], ["U", 0, -1]]

        for l in vec:
            new_boxes = self.boxes.copy()
            idea = (self.player[0]+l[1], self.player[1]+l[2]) #idea to gdzie chcemy przesunąć gracza

            if idea in self.walls:
                continue
            if idea in self.boxes:          #przesuwanie skrzynki
                new_box = (idea[0]+l[1], idea[1]+l[2])
                if new_box in self.walls or new_box in self.boxes: #nie można przesunąć
                    continue
                new_boxes.remove(idea)  #zmieniamy współrzędne skrzynki
                new_boxes.add(new_box)
            res.append((new_boxes, idea, self.moves + l[0])) #ściany i cele bez zmian
        return res




def bfs(walls, boxes, goals, player):
    visited = {(tuple(boxes), player)}
    kolejka = queue.Queue()
    kolejka.put((boxes, player, ""))
    while True:
        current_state = kolejka.get()
        #print(current_state[2])
        current_state = state(walls, current_state[0], goals, current_state[1], current_state[2])
        if current_state.win():
            return print('sokoban solved using bfs: ',current_state.moves)
        for e in current_state.legal_move():
            if (tuple(e[0]), e[1]) not in visited:
                visited.add((tuple(e[0]), e[1]))
                kolejka.put(e)

def h1(boxes, goals):
    dist = []
    for box in boxes:
        minimum = 1000
        for goal in goals:
            if abs(box[0]-goal[0]) + abs(box[1]-goal[1]) < minimum:
                minimum = abs(box[0]-goal[0]) + abs(box[1]-goal[1])
        dist.append(minimum)
    return min(dist)

def astar(walls, boxes, goals, player):

    visited = {(tuple(boxes), player)}
    kolejka = []
    heapq.heappush(kolejka, (h1(boxes, goals), (boxes, player, "")))
    while True:
        current_state = heapq.heappop(kolejka)
        #print(current_state)
        current_state = state(walls, current_state[1][0], goals, current_state[1][1], current_state[1][2])
        if current_state.win():
            return print('sokoban solved using A*: ', current_state.moves)
        for e in current_state.legal_move():
            if (tuple(e[0]), e[1]) not in visited:
                visited.add((tuple(e[0]), e[1]))
                heapq.heappush(kolejka, (h1(e[0], goals) + len(e[2]), e))




dane = init()
#print(dane[2])
bfs(dane[0], dane[1], dane[2], dane[3])
astar(dane[0], dane[1], dane[2], dane[3])
