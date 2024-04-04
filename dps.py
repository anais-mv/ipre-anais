from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time
import sys
from common.debug import debug_compare
from math import log2


class DPS:
    def __init__(self, initial_state, heuristic, weight=1 ):
        self.expansions = 0
        self.total_expansions = 0
        self.generated = 0
        self.initial_state = initial_state
        self.weight = weight
        self.heuristic = heuristic


    def estimate_suboptimality(self):
        # retorna min_{s\in Open} costo_solucion / (g(s)+h(s))

        fmin = 100000000
        if self.solution is not None:
            if self.open.is_empty() and self.preferred.is_empty():
                return 1
            """
            for node in self.open:
                if fmin > node.g + node.h[1]:
                    fmin = node.g + node.h[1]
            for node in self.preferred:
                if fmin > node.g + node.h[0]:
                    fmin = node.g + node.h[0]
            """
            fmin=self.open.top().key[1]
            return self.solution.g/fmin

    def fvalue(self, g, h):
        return g+h

    def hfocal_potential(self, w, fmin, g,h):
        if h==0:
            return -1*float('inf')
        else :
            return -1*(w*fmin-g)/h 
    
    # Recorre toda la open para obtener el menor f=g+h        
    def get_fmin(self):
        fmin = 100000000
        for node in self.open:
            if fmin > node.g + node.h[0]:
                fmin = node.g + node.h[0]
        return fmin


    #   This method make the search in Focal Like style, i.e. use a focal list sorted by
    # potential function and a openlist sorted by f, to obtain the f_min.
    #   When the f_min changes, it's necessary resort the focal list because the 
    # potential function is not efficiently reusable.  
    def search_focallike(self, focal_w=1.5, mode=1):  #  focal_w ajusta el rango del focal_search
        time_start = time.time()
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0
        self.f_updates = 0
        self.update_time = 0.0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        #initial_node.h[1] = initial_node.h[0]

        #initial state has fmin= 0  + h(s_start)
        initial_node.key[0] = self.hfocal_potential(focal_w, initial_node.h[0], 0, initial_node.h[0]) 
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[0])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        f_min = initial_node.key[1]
        while not self.preferred.is_empty():
            if time.time()-time_start > 60*30 : # SI ES MAYOR A MEDIA HORA RETORNA NONE
                print("TIME OUT")
                return None
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            f_min = self.open.top().key[1] if self.open.top().key[1] > f_min else f_min
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open
            #print(n.key[0], f_min, focal_w, n.g, n.h[0])
            assert (n==m)
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.successors() # Para el uso de la learned heuristic como stochastic policy

            self.expansions += 1
            for child_state, action, cost in succ:
                # print("? check", child_state.board)
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = self.heuristic(child_state)
                        #child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key[0] = self.hfocal_potential(focal_w, f_min, child_node.g, child_node.h[0]) 
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[0]) # actualizamos el f de child_node
                    self.open.insert(child_node)
                    self.preferred.insert(child_node)

            
            # IF THE Fmin CHANGES
            newfmin = self.open.top().key[1]
            if self.open.size and f_min < newfmin:
                print("Actualizando fmin",f_min, newfmin, "OPEN SIZE", self.open.size, self.preferred.size)
                for i in range(1, self.preferred.size+1):
                    self.preferred.items[i].key[0] = self.hfocal_potential(focal_w, newfmin, self.preferred.items[i].g, self.preferred.items[i].h[0]) 
                

 
        # print(*[self.open.items[i+1].key[1] for i in range(self.open.size)])
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        # print("none found")
        return None





    def search_bfslike(self, focal_w=1.5, mode=1):  #  focal_w ajusta el rango del focal_search
        time_start = time.time()
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.open = MultiBinaryHeap(0)
        self.expansions = 0
        self.f_updates = 0
        self.update_time = 0.0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        #initial_node.h[1] = initial_node.h[0]

        #initial state has fmin= 0  + h(s_start)
        initial_node.key[0] = self.hfocal_potential(focal_w, initial_node.h[0], 0, initial_node.h[0]) 
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[0])

        self.open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        change_fmin_flag = False # indica un "posible" cambio de fmin
        f_min = initial_node.key[1]
        while not self.open.is_empty():
            if time.time()-time_start > 60*30 : # SI ES MAYOR A MEDIA HORA RETORNA NONE
                print("TIME OUT")
                return None
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            n = self.open.extract()

            # cuando se extrae un nodo con f = fmin, es posible que fmin haya cambiado
            if n.g + n.h[0] == f_min:
                change_fmin_flag = True

            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.successors() # Para el uso de la learned heuristic como stochastic policy

            self.expansions += 1
            for child_state, action, cost in succ:
                # print("? check", child_state.board)
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = self.heuristic(child_state)
                        #child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key[0] = self.hfocal_potential(focal_w, f_min, child_node.g, child_node.h[0]) 
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[0]) # actualizamos el f de child_node
                    self.open.insert(child_node)

            #si es probable que fmin haya cambiado
            if change_fmin_flag:
                change_fmin_flag = False
                fmin_obtained = self.get_fmin()
                # si realmente cambio se configura el nuevo fmin y reordena la open
                if f_min < fmin_obtained:
                    #print("REALMENTE CAMBIO", f_min, fmin_obtained, "UPDATES:", self.open.size )
                    f_min = fmin_obtained                    
                    for i in range(1, self.open.size+1):
                        self.open.items[i].key[0] = self.hfocal_potential(focal_w, f_min, self.open.items[i].g, self.open.items[i].h[0]) 
                
            

 
        # print(*[self.open.items[i+1].key[1] for i in range(self.open.size)])
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        # print("none found")
        return None




     