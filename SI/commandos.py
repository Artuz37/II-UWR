import queue
import heapq
import itertools

output = open("zad_output.txt","w" )

def init():
    commandoses = set()
    goals = set()
    walls = set()
    file = open("zad_input.txt")
    lines = file.readlines()
    i = 0
    for y in lines:
        j = 0
        for x in y:
            if x == '#':
                walls.add((j, i))
            elif x == 'G':
                goals.add((j, i))
            elif x == 'S':
                commandoses.add((j, i))
            elif x == 'B':
                goals.add((j, i))
                commandoses.add((j, i))
            # print(chests, goals)
            j += 1
        i += 1

    return walls, goals, commandoses, j-1, i


dane = init()
#print(dane)

class Hstate:
    def __init__(self, walls, goals, commandos, moves):
        self.walls = walls
        self.goals = goals
        self.commandos = commandos
        self.moves = moves

    def win(self):
        return self.commandos in self.goals

    def legal_move(self):
        res = []
        vec = [["R", 1, 0], ["D", 0, 1], ["L", -1, 0], ["U", 0, -1]]
        for vector in vec:
            new_commandos = (self.commandos[0]+vector[1], self.commandos[1]+vector[2])
            if new_commandos not in self.walls:
                res.append((new_commandos, self.moves + 1))
        return res


class State:
    def __init__(self, walls, goals, commandoses, moves):
        self.walls = walls
        self.goals = goals
        self.commandoses = commandoses
        self.moves = moves

    def win(self):
        return self.commandoses.issubset(self.goals)


    def legal_move(self):
        res = []
        vec = [["R", 1, 0], ["D", 0, 1], ["L", -1, 0], ["U", 0, -1]]
        for vector in vec:
            new_commandoses = set()
            difference = 0
            for commandos in self.commandoses:
                new_commandos = (commandos[0]+vector[1], commandos[1]+vector[2])
                if new_commandos not in self.walls:
                    difference += 1
                    new_commandoses.add(new_commandos)
                else: new_commandoses.add(commandos)
            if difference > 0:
                res.append((new_commandoses, self.moves + vector[0]))
        return res

    def move_vecs(self):
        win_commandoses = self.commandoses.copy()
        win_moves = ""
        vec = list(itertools.permutations([["R", 1, 0], ["D", 0, 1], ["L", -1, 0], ["U", 0, -1]]))
        best = len(self.commandoses)
        for vectors in vec:
            moves = ""
            new_commandoses = self.commandoses.copy()
            for vector in vectors:
                newer_commandoses = new_commandoses.copy()
                for commandos in newer_commandoses:
                    new_commandos = commandos #zmiana pozycji komandosa
                    for i in range (18):
                        newer_commandos = (new_commandos[0]+vector[1], new_commandos[1]+vector[2])
                        if newer_commandos in self.walls: #jak komandos w ścianie, to już go olewamy i zwracamy poprzedniego
                            break                               #i kończymy pętlę dla tego komandosa
                        new_commandos = newer_commandos

                    new_commandoses.remove(commandos) #zmiana pozycji komandosa
                    new_commandoses.add(new_commandos)
                moves = moves + 18*vector[0]
            if len(new_commandoses) <= best:
                win_commandoses = new_commandoses.copy()
                win_moves = moves
        return win_commandoses, win_moves



def bfs(walls, goals, commandoses):
    visited = {tuple(commandoses)}
    eliminacja = State(walls, goals, commandoses, "")
    kolejka = queue.Queue()
    kolejka.put(eliminacja.move_vecs())
    #print(eliminacja.move_vecs())
    while True:
        current_state = kolejka.get()
        current_state = State(walls, goals, current_state[0], current_state[1])
        if current_state.win():
            return output.write(current_state.moves)
        for e in current_state.legal_move():
            if tuple(e[0]) not in visited:
                visited.add(tuple(e[0]))
                kolejka.put(e)


def legal_move(commandos, walls):
    res = []
    vec = [["R", 1, 0], ["D", 0, 1], ["L", -1, 0], ["U", 0, -1]]
    #print('commandos', commandos)
    for vector in vec:
        new_commandos = (commandos[0]+vector[1], commandos[1]+vector[2])
        if new_commandos not in walls:
            res.append(new_commandos)
    return res

def hbfs(commandos, goals, walls):
    visited = {commandos}
    kolejka = []
    heapq.heappush(kolejka, (commandos, 0))
    while True:
        current_state = heapq.heappop(kolejka)
        #print(current_state)
        if current_state[0] in goals:
            return current_state[1]
        for e in legal_move(current_state[0], walls):
            if e not in visited:
                visited.add(e)
                heapq.heappush(kolejka, (e, current_state[1]+1))

def distances(walls, goals, x, y):
    slownik = {}
    for i in range(x):
        for j in range(y):
            if (i, j) not in walls and (i, j) != (22, 0):
                slownik[i, j] = hbfs((i, j), goals, walls)
    return slownik

def h(commandoses):
    dists = []
    dists = [dict[commandos] for commandos in commandoses]

    return max(dists)

def astar(walls, goals, commandoses):
    visited = {tuple(commandoses)}
    kolejka = []
    heapq.heappush(kolejka, (h(commandoses), (commandoses, "")))
    while True:
        current_state = heapq.heappop(kolejka)
        current_state = State(walls, goals, current_state[1][0], current_state[1][1])
        #print(current_state.moves)
        if current_state.win():
            return print(current_state.moves, len(current_state.moves))
            #return output.write(current_state.moves)
        for e in current_state.legal_move():
            if tuple(e[0]) not in visited:
                #print("komandos",e[0])
                visited.add(tuple(e[0]))
                heapq.heappush(kolejka, (h(e[0]) + len(e[1]), e))


dict = distances(dane[0], dane[1], dane[3], dane[4])
#print(dict)
#print(dict)
#bfs(dane[0], dane[1], dane[2])
astar(dane[0], dane[1], dane[2])