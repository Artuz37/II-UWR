import queue
import heapq
import itertools
import random
import copy
import time


weights2 = ((100, -20, 10,  5,  5, 10, -20, 100),
           (-20, -50,  -2, -2, -2, -2, -50, -20),
           (10,   -2,   0, -1, -1,  0,  -2,  10),
           (5,    -2,  -1, -1, -1, -1,  -2,   5),
           (5,    -2,  -1, -1, -1, -1,  -2,   5),
           (10,   -2,   0, -1, -1,  0,  -2,  10),
           (-20, -50,  -2, -2, -2, -2, -50, -20),
           (100, -20,  10,  5,  5, 10, -20, 100))

weights1 = ((100, -40, 10,  -10,  -10, 10, -40, 100),
           (-40, -20,  -2, -2, -2, -2, -20, -40),
           (10,   -2,   0, -1, -1,  0,  -2,  10),
           (-10,    -2,  -1, -1, -1, -1,  -2,   -10),
           (-10,    -2,  -1, -1, -1, -1,  -2,   -10),
           (10,   -2,   0, -1, -1,  0,  -2,  10),
           (-20, -50,  -2, -2, -2, -2, -20, -40),
           (100, -20,  10,  5,  5, 10, -40, 100))

weights3 = ((100, 90, 90, 90, 90, 90, 90, 100),
           (90, 90,  40, 40, 40, 40, 90, 90),
           (90, 40, 50, 30, 30, 50, 40, 90),
           (90, 40, 30, 50, 50, 30, 40, 90),
           (90, 40, 30, 50, 50, 30, 40, 90),
           (90, 40, 50, 30, 30, 50, 40, 90),
           (90, 90, 40, 40, 40, 40, 90, 90),
           (100, 90, 90, 90, 90, 90, 90, 100))

weights = (weights1, weights2, weights3)

def custom_deepcopy(object):
    B = Board()
    B.board = []
    for row in object.board:
        B.board.append(row.copy())
    B.fields = copy.copy(object.fields)
    return B
def initial_board():
    B = [ [None] * 8 for i in range(8)]
    B[3][3] = 1
    B[4][4] = 1
    B[3][4] = 0
    B[4][3] = 0
    return B

class Board:
    dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.board = initial_board()
        self.fields = init_fields()
        self.move_list = []


    def moves(self, player):
        res = []
        for (x, y) in self.fields:
            if any(self.can_beat(x, y, direction, player) for direction in Board.dirs):
                res.append((x, y))
        if not res:
            return [None]
        return res

    def can_beat(self, x, y, d, player):
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def do_move(self, move, player):
        self.move_list.append(move)
        if move == None:
            return

        x, y = move
        x0, y0 = move
        self.board[y][x] = player
        self.fields -= set([move])
        for dx, dy in self.dirs:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == player:
                for (nx, ny) in to_beat:
                    self.board[ny][nx] = player

    def terminal(self):#
        if not self.fields:
            return True
        if len(self.move_list) < 2:
            return False
        return self.move_list[-1] == self.move_list[-2] == None

    def result(self):
        res = 0
        for y in range(8):
            for x in range(8):
                b = self.board[y][x]
                if b == 0:
                    res -= 1
                elif b == 1:
                    res += 1
        #print(res)
        return res

    def heuristic(self, K):
        res = 0
        if K < 6:
            stage = 0
        elif K < 30:
            stage = 1
        elif K < 65:
            stage = 2
        for y in range(8):
            for x in range(8):
                b = self.board[y][x]
                if b == 0:
                    res -= weights[stage][y][x]
                elif b == 1:
                    res += weights[stage][y][x]
        return res

    def random_move(self, player):
        ms = self.moves(player)
        if ms:
            return random.choice(ms)
        return [None]

    def draw(self):
        for i in range(8):
            res = []
            for j in range(8):
                b = self.board[i][j]
                if b == None:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print (''.join(res) )
        print()

    def find_best(self, depth, player, K):
        def alphabeta(state, depth, alpha, beta, maximizing_player):
            # depth = 0 or end of the game or no moves possible
            if depth == 0 or state.terminal() or state.moves(maximizing_player) == [None]:
                return state.heuristic(K)

            children = state.moves(maximizing_player)
            # player == 1 <=> player == white <=> enemy's move
            if maximizing_player:
                for move in children:
                    new_board = custom_deepcopy(state)
                    new_board.do_move(move, player)
                    alpha = max(alpha, alphabeta(new_board, depth - 1, alpha, beta, False))
                    if alpha >= beta:
                        break
                return alpha
            # our move
            else:
                for move in children:
                    new_board = custom_deepcopy(state)
                    new_board.do_move(move, player)
                    beta = min(beta, alphabeta(new_board, depth - 1, alpha, beta, True))
                    if alpha >= beta:
                        break
                return beta

        best_move = None
        best_score = 1e9
        for move in self.moves(player):
            new_board = custom_deepcopy(self)
            new_board.do_move(move, player)

            val = alphabeta(new_board, depth, -1e9, 1e9, 1 - player)
            if val < best_score:
                best_move = move
                best_score = val

        return best_move


def init_fields():
    fields = set()
    for i in range(8):
        for j in range(8):
            if (i,j) not in {(3,3), (3,4), (4, 3), (4,4)}:
                fields.add( (i,j) )
    return fields




outcome = 0
start = time.time()
for i in range(1000):
    B = Board()
    player = 0
    K = 0
    while True:
        if player:
            move = B.random_move(player)
            B.do_move(move, player)
        else:
            move = B.find_best(0, player, K)
            B.do_move(move, player)
        player = 1-player
        if B.terminal():
            end = time.time()
            #print(B.result(), i, end-start)
            break
        K+=1
    if B.result() < 0:
        outcome += 1
end = time.time()
print(f'AI won {outcome} out of 1000 games vs bot doing random moves')
