from binary_heap import BinaryHeap
from node import Node
import time


class Astar:
    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.heuristic = heuristic
        self.solution = None

    def estimate_suboptimality(self):
        fmin = 100000000
        if self.solution is not None:
            for node in self.open:
                if fmin > node.g + node.h:
                    fmin = node.g + node.h
            return self.solution.g/fmin

    def search(self):
        start_search = time.time()
        self.start_time = time.time()
        self.open = BinaryHeap()
        self.expansions = 0
        self.solution = None
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = 10000*self.weight*initial_node.h  # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            if time.time()-start_search > 30*60 :
                self.end_time = time.time()
                return None

            #imprime cada dos minutos
            #if (int(time.time()-start_search)/60)%2 == 0 and time.time()-start_search > 60 : 
                #print("IMPRIMIENDO ESTADO")
                #print(time.time()-start_search, self.expansions, len(self.generated))

            n = self.open.extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.time()
                self.solution = n
                return n
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        child_node.h = self.heuristic(child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = 10000*(child_node.g + self.weight*child_node.h) - child_node.g # actualizamos el f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def search_inadmisible(self, UPPERBOUND):
        start_search = time.time()
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        self.solution = None
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = 10000*self.weight*initial_node.h  # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():

            if time.time()-start_search > 30*60 :
                return None
                
            n = self.open.extract()   # extrae n de la open
            #print(start_search-time.time(), n.g, n.h)
            if n.state.is_goal() and n.g <= UPPERBOUND:
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.DeepCubeA_succesorsA()
            self.expansions += 1
            for child_state, action, cost, learnedheuristic in succ:
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if path_cost <= UPPERBOUND:
                    child_node = self.generated.get(child_state)
                    is_new = child_node is None  # es la primera vez que veo a child_state
                    if is_new or path_cost < child_node.g:
                        # si vemos el estado child_state por primera vez o lo vemos por
                        # un mejor camino, entonces lo agregamos a open
                        if is_new:  # creamos el nodo de child_state
                            child_node = Node(child_state, n)
                            child_node.h = learnedheuristic
                            self.generated[child_state] = child_node
                        child_node.action = action
                        child_node.parent = n
                        child_node.g = path_cost
                        child_node.key =  self.weight*child_node.h #10000*(child_node.g + self.weight*child_node.h) - child_node.g # actualizamos el f de child_node
                        self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None


    def dicrepancy_BFSearch(self, discrepancy_mode="rank"):
        start_search = time.time()
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        self.solution = None
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.path_disc = 0
        initial_node.key = 0 #10000*self.weight*initial_node.h  # asignamos el valor f (el cual sera la discrepancia)
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            if start_search-time.time() > 30*60 :
                return None
                
            n = self.open.extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n
            #print(n.key, n.closed, n.h, n.state)
            succ = n.state.DeepCubeA_succesorsA_sinpreff()
            succ2= succ.sort(key=lambda tup: tup[3]) #ordena de acuerdo a la hnn (tup[3])

            self.expansions += 1
            discrep = 0
            for child_state, action, cost, hnn in succ:
                if discrepancy_mode == "rank":
                    node_discrepancy = discrep
                elif discrepancy_mode == "best":
                    node_discrepancy = 1 if discrep>0 else 0

                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        self.generated[child_state] = child_node
                        child_node.h = hnn
                    child_node.path_disc = n.path_disc + node_discrepancy
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = child_node.path_disc #10000*(child_node.path_disc) + hnn # key es menor disc desempatado por menor heur
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
                    discrep+=1
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def potential_search(self):
        self.start_time = time.process_time()
        self.open = BinaryHeap()
        self.expansions = 0
        self.solution = None
        initial_node = Node(self.initial_state)
        initial_node.g = 0
        initial_node.h = self.heuristic(self.initial_state)
        initial_node.key = 10000*self.weight*initial_node.h  # asignamos el valor f
        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        while not self.open.is_empty():
            n = self.open.extract()   # extrae n de la open
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = Node(child_state, n)
                        child_node.h = self.heuristic(child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key = -(10000000000000-child_node.g)/child_node.h #10000*(child_node.g + self.weight*child_node.h) - child_node.g # actualizamos el f de child_node
                    self.open.insert(child_node) # inserta child_node a la open si no esta en la open
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None
