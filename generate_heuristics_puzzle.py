# Una implementacion muy simplificada de DFS
import sys
import random
from os.path import join, exists
from node import Node
from puzzle import Puzzle

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def insert(self, item):
        self.push(item)

    def extract(self):
        return self.pop()

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (top = final de la lista) '

    def __len__(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (el del principio se muestra primero) '

    def __len__(self):
        return len(self.items)

    def insert(self, item):
        self.enqueue(item)

    def extract(self):
        return self.dequeue()


class GenericSearch:
    def __init__(self, initial_state, strategy, file=None):
        self.mse = 0.0
        self.expansions = 0
        self.initial_state = initial_state
        self.strategy = strategy
        self.max_depth = 0
        self.file = file

    def _newopen(self):
        if self.strategy == 'bfs':
            return Queue()
        elif self.strategy == 'dfs':
            return Stack()
        else:
            print(type, 'is not supported')
            sys.exit(1)

    def write_state(self, state, depth):
        h_nn = depth + self.constant_c * random.gauss(0, 1) * (depth**self.constant_k)
        self.mse += (h_nn - depth)**2
        # self.file.write(' '.join([str(n) for n in state.board]) + ' ' + str(h_nn) + '\n')

    def search(self):
        self.open = self._newopen()
        self.expansions = 0
        self.open.insert(Node(self.initial_state))
        self.generated = set()  ## generated mantiene la union entre OPEN y CLOSED
        self.generated.add(self.initial_state)
        while not self.open.is_empty():
#            print(self.open)      # muestra open list
            n = self.open.extract()   # extrae n de la open
#            print(n.state)   # muestra el estado recien expandido
            self.write_state(n.state, n.depth)
            if n.depth > self.max_depth:
                self.max_depth = n.depth
                print('at depth', n.depth)
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, _ in succ:
                if child_state in self.generated:  # en DFS este chequeo se puede hacer sobre la rama
                    continue
                child_node = Node(child_state, n, action)
                # if child_state.is_goal():
                #     return child_node
                self.generated.add(child_state)
                self.open.insert(child_node)
        self.mse = self.mse/len(self.generated)
        return None

# h_nn = h* + ((h*)^k)*c*N(0,1)
# c = 1  # constant for multiplication
mses = [0,5, 10, 20, 100, 200]
k = 4 # exponent for k multiplied to c

for mse in mses:
    fpath = join('puzzle_', "heuristics", "h_star.txt")
    if not exists(fpath):
        sum_h = "unknown"
    with open(fpath, 'r') as file:
        file.readline()
        lines = file.readlines()
        sum_h = sum([((int(line.strip().split(' ')[-1])**k))**2 for line in lines])/len(lines)
        # mse = c^2 + sum((h*)^2k)
        c = (mse/sum_h)**(1/2)

    init = Puzzle(abstract_init)
    f = open(join('puzzle_', "heuristics", f"{mse}_{k}.txt"), 'w')
    f.write(' '.join([str(x) for x in pattern])+'\n') ## escribimos el patron
    s = GenericSearch(init, 'bfs', f)
    s.constant_c = c
    s.constant_k = k
    result = s.search()
    print('Number of generated states=',len(s.generated))
    f.close()
    print(f"c:= {c} ; k:= {k}")
    print("Error cuadrático medio")
    print("\t Real    :", s.mse)


    print("\t Esperado:", mse)
