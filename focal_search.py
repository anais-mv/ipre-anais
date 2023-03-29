from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time
import sys
from heapq import heappush, heappop  # para beam_ahead
# from common.debug import debug_compare
from math import log2
from collections import deque

class FakeMultiBinHeap(MultiBinaryHeap):
    def __init__(self, original_bin_heap):
        super().__init__(id=1, max_size=0)
        self.items = original_bin_heap.items
        self.id = original_bin_heap.id
        self.max_size = original_bin_heap.max_size
        self.size = original_bin_heap.size

    # def top(self):
    #     return self.items[1]

    def extract(self, hole=1):
        if self.size == 0 or hole==0:
            return None
        element = self.items[hole]
        element.heap_index[self.id] = 0
        # inicio agregado 08/20
        if hole != self.size:  # si el nodo sacado es el último, no se necesitan hacer cambios
            self.percolateupordown(hole, self.items[self.size])
        self.size -= 1
        return element

    def insert(self, element):
        if element.heap_index[self.id] == 0:  # element no esta en el heap
            return
        else:  # element esta en el heap; suponemos que su key ha cambiado
            self.percolateupordown(element.heap_index[self.id], element)


class FocalSearch:
    def __init__(self, initial_state, heuristic, weight=1):
        self.expansions = 0
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
            for node in self.open:
                if fmin > node.g + node.h[1]:
                    fmin = node.g + node.h[1]
            for node in self.preferred:
                if fmin > node.g + node.h[1]:
                    fmin = node.g + node.h[1]
            return self.solution.g/fmin

    def fvalue(self, g, h):
        return g+h # 10000*(g + self.weight*h) - g  # (g+h, h)
        
    def ftrustvalue(self, g, h, trust):
        # el negativo es para ordenarlo en el sentido contrario
        # return (10000*(g + self.weight*h) - g)/trust
        return (g+h)/trust # (-trust, g+h) # 

    def h_focales(self, g,h,trust_nodo, trust_anterior, mode=-1):
        # H_focal1 = Probabilidad acumulada
        if mode == 1:
            return -1*trust_nodo*trust_anterior

        # H_focal2 = Probabilidad acumulada / f
        elif mode == 2:
            return -1*(trust_nodo*trust_anterior)/(g+h) 
        
        # H_focal3 = probabilidad del nodo (no acumulada)
        elif mode == 3:
            return -1*trust_nodo
        
        # H_focal4 = probabilidad del nodo / f
        elif mode == 4:
            return -1*trust_nodo/(g+h)
        
        # H_focal5
        elif mode == 5:
            return 0
        
        # H_focal6
        elif mode == 6:
            return 0
        else :
            print("heuristic no definida")
            return 0

    def discrepancy_beam_search(self, focal_w=1.5, beam=2, discrepancy_mode="best", mult=-1):  #  focal_w ajusta el rango del focal_search
        """
        no usa focal
        USA EL original_search de esqueleto
        usa beam
        discrepancy_mode in ["best", "position"]
        best : el mejor es discrepancia 0, los otros 1
        position := discrepancia segun trust (0=mas confiable, y subiendo de a uno por su orden)
        focal search ordenado por (dicrepancia, -g)
        mult := Determines the sign of the sort, default is -1 which sort greatest to lowest
        """
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.preference = 0  # prioridad del nodo segun red (menor = mas importante)
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        # print("H_i", initial_node.h[1])

        initial_node.key[0] = (0,0) # discrepancias, g
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 1
        while not self.preferred.is_empty():
            # if self.preferred.size == 1:
            #     print("H_x", self.preferred.top().h[1])
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            f_min = self.open.top().key[1]
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open
            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.k_accs_successors()
            # print("S", self.preferred.size)

            # quedarse con los beam mejores estados ordenados por trusts
            trusts = [(trust, child_state) for child_state, _, _, trust in succ]
            trusts.sort(key= lambda x: mult*x[0])
            most_trusted = [i[1] for i in trusts]

            self.expansions += 1
            for child_state, action, cost, trust in succ:
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = self.heuristic(child_state)
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    node_discrepancy = n.key[0][0]
                    if discrepancy_mode == "best":
                        if child_state != most_trusted[0]:
                            node_discrepancy += 1
                    elif discrepancy_mode == "position":
                        node_discrepancy += most_trusted.index(child_state)  # COMPLEJIDAD LINEAL
                    child_node.preference = most_trusted.index(child_state)

                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[0] = (node_discrepancy, child_node.h[1])
                    self.open.insert(child_node)
                    # print(" P", child_node.preference, is_new, child_node.key[1])

                    if child_node.heap_index[0] or (
                        #child_node.key[1] <= focal_w*f_min and 
                        child_node.preference < beam): # estaba en preferred
                        self.preferred.insert(child_node)

            # if self.open.size and f_min < self.open.top().key[1]:
            #     # self.f_updates += 1
            #     # t_time = time.process_time()
            #     for i in range(1, self.open.size+1):
            #         if focal_w*self.open.top().key[1] >= self.open.items[i].key[1] > focal_w*f_min:
            #             if self.open.items[i].preference < beam:
            #                 self.preferred.insert(self.open.items[i])
                # self.update_time += time.process_time() - t_time
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def discrepancy_greedy_search(self, beam=2, discrepancy_mode="best"):  #  focal_w ajusta el rango del focal_search
        """
        UNFINISHED
        discrepancy_search, pero sin subobtimalidad de entrada.
        Usa dos listas, open (ordenada por f) y focal (ordenada por discrepancia). A focal solo entran los beam mejores de la open. No hace updateLowerBound al cambiar el fmin, ya que la focal solo contiene los mejores acc, sin importar su suboptimalidad
        """
        
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = 0 # discrepancias
        initial_node.h[1] = initial_node.h[0]

        initial_node.key[0] = self.ftrustvalue(initial_node.g,initial_node.h[0], initial_node.trust)  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.non_preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 1
        self.non_pref = 0
        while not self.open.is_empty() or not self.preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            if not self.preferred.is_empty():
                queue = self.preferred
            else:
                self.non_pref += 1
                queue = self.non_preferred

            n = queue.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open
            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.k_accs_successors()

            # quedarse con los beam mejores estados ordenados por trusts
            trusts = [(trust, child_state) for child_state, _, _, trust in succ]
            trusts.sort(key= lambda x: -x[0])
            most_trusted = [i[1] for i in trusts]


            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    child_node.key[0] = n.key[0]
                    if discrepancy_mode == "best":
                        if child_state != most_trusted[0]:
                            child_node.key[0] += 1
                    elif discrepancy_mode == "position":
                        child_node.key[0] += most_trusted.index(child_state)

                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node

                    self.open.insert(child_node)
                    if child_node.heap_index[0] or (child_state in most_trusted[:beam]): # estaba en preferred o es de beam
                        self.preferred.insert(child_node)
                        if child_node.heap_index[2]:
                            self.non_preferred.extract(child_node.heap_index[2])
                    else:
                        self.non_preferred.insert(child_node)


        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    
    def discrepancy_h5_search(self, focal_w=1.5, acc=1.0, number_of_actions=None):  #  focal_w ajusta el rango del focal_search
        """
        USA EL original_search de esqueleto
        best : el mejor es discrepancia 0, los otros 1
        position := discrepancia segun trust (0=mas confiable, y subiendo de a uno por su orden)
        focal search ordenado por (dicrepancia, f)
        """
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.pref = 0
        initial_node.non_pref = 0

        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]

        initial_node.key[0] = (0,initial_node.h[0]) # discrepancias, g
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 1
        while not self.preferred.is_empty():
            f_min = self.open.top().key[1]
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open

            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.k_accs_successors()

            # quedarse con los beam mejores estados ordenados por trusts
            best_state = max(succ, key=lambda x: x[3])[0]

            self.expansions += 1
            for child_state, action, cost, trust in succ:
                # print("? check", child_state.board)
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[1] = self.heuristic(child_state)
                        child_node.h[0] = child_node.h[1]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    child_node.pref = n.pref
                    child_node.non_pref = n.non_pref
                    if child_state != best_state:
                        child_node.non_pref += 1
                    else:
                        child_node.pref += 1
                    if acc != 1:
                        child_node.h[0] = child_node.pref*log2(acc)/log2((1-acc)/(number_of_actions-1)) + child_node.non_pref
                    else:
                        child_node.h[0] = child_node.non_pref

                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[0] = (child_node.h[0], child_node.h[1])  # CAMBIO: se usa el h en vez de f para el desempate

                    self.open.insert(child_node)
                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min:  # estaba en focal o cumple con el rango
                        self.preferred.insert(child_node)
                # elif path_cost == child_node.g:
                #     node_discrepancy = n.key[0][0]
                #     if discrepancy_mode == "best":
                #         if child_state != best_state:
                #             node_discrepancy += 1
                #     elif discrepancy_mode == "position":
                #         node_discrepancy += most_trusted[child_state]

                #     child_node.key[0] = (min(child_node.key[0][0], node_discrepancy), child_node.key[0][1])
                #     if child_node.heap_index[0]:
                #         self.preferred.insert(child_node)

            assert f_min <= self.open.top().key[1]
            if self.open.size and f_min < self.open.top().key[1]:
                # self.f_updates += 1
                # t_time = time.process_time()
                for i in range(1, self.open.size+1):
                    if focal_w*self.open.top().key[1] >= self.open.items[i].key[1] > focal_w*f_min:
                        self.preferred.insert(self.open.items[i])
                # self.update_time += time.process_time() - t_time

        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def discrepancy_search(self, focal_w=1.5, discrepancy_mode="best"):  #  focal_w ajusta el rango del focal_search
        """
        USA EL original_search de esqueleto
        discrepancy_mode in ["best", "position"]
        best : el mejor es discrepancia 0, los otros 1
        position := discrepancia segun trust (0=mas confiable, y subiendo de a uno por su orden)
        focal search ordenado por (dicrepancia, f)
        """
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0

        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]

        initial_node.key[0] = (0,initial_node.h[0]) # discrepancias, g
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 1
        while not self.preferred.is_empty():
            f_min = self.open.top().key[1]
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open

            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.k_accs_successors()

            # quedarse con los beam mejores estados ordenados por trusts
            if discrepancy_mode == "best":
                # obtener el estado de mayor trust
                best_state = max(succ, key=lambda x: x[3])[0]
            elif discrepancy_mode == "position":
                # crear diccionsrio del estado a su discrepancia
                most_trusted = {state[0] : i for
                                    i, state in enumerate(
                                        sorted(succ, key=lambda x: x[3], reverse=True)
                                    )
                                }
                assert [s[3] for s in succ].count(max(s[3] for s in succ)) == 1

            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    node_discrepancy = n.key[0][0]
                    if discrepancy_mode == "best":
                        if child_state != best_state:
                            node_discrepancy += 1
                    elif discrepancy_mode == "position":
                        node_discrepancy += most_trusted[child_state]

                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[0] = (node_discrepancy, child_node.h[1])  # CAMBIO: se usa el h en vez de f para el desempate

                    self.open.insert(child_node)
                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min:  # estaba en focal o cumple con el rango
                        self.preferred.insert(child_node)
                # elif path_cost == child_node.g:
                #     node_discrepancy = n.key[0][0]
                #     if discrepancy_mode == "best":
                #         if child_state != best_state:
                #             node_discrepancy += 1
                #     elif discrepancy_mode == "position":
                #         node_discrepancy += most_trusted[child_state]

                #     child_node.key[0] = (min(child_node.key[0][0], node_discrepancy), child_node.key[0][1])
                #     if child_node.heap_index[0]:
                #         self.preferred.insert(child_node)

            assert f_min <= self.open.top().key[1]
            if self.open.size and f_min < self.open.top().key[1]:
                # self.f_updates += 1
                # t_time = time.process_time()
                for i in range(1, self.open.size+1):
                    if focal_w*self.open.top().key[1] >= self.open.items[i].key[1] > focal_w*f_min:
                        self.preferred.insert(self.open.items[i])
                # self.update_time += time.process_time() - t_time

        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def our_search(self, focal_w=1.5):  #  focal_w ajusta el rango del focal_search
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.sub_open = MultiBinaryHeap(1)
        self.non_preferred = MultiBinaryHeap(2)
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.h[2] = initial_node.h[0]

        initial_node.key[0] = self.ftrustvalue(initial_node.g,initial_node.h[0], initial_node.trust)  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        initial_node.key[2] = initial_node.key[1]

        self.sub_open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        f_min = self.sub_open.top().key[1]
        while not self.preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            n = self.preferred.extract()
            m = self.sub_open.extract(n.heap_index[1])   # extrae m de la open
            assert (n==m)
            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            # print(n.key[1], n.key[0], self.preferred.size)
            succ = n.state.k_accs_successors()
            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        child_node.h[2] = child_node.h[1]
                        self.generated[child_state] = child_node
                        # print("+ new")
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    child_node.key[0] = self.ftrustvalue(child_node.g,child_node.h[0], child_node.trust)
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[2] = child_node.key[1]

                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min: # estaba en focal o cumple con el rango
                        if child_node.key[1] <= focal_w*f_min and child_node.heap_index[2]:
                            self.non_preferred.extract(child_node.heap_index[2])
                        self.preferred.insert(child_node)
                        self.sub_open.insert(child_node)
                    else:
                        self.non_preferred.insert(child_node)

            f_min = (self.sub_open.top() if self.sub_open.size else self.non_preferred.top()).key[1]
            while self.non_preferred.size and self.non_preferred.top().key[1] <= focal_w*f_min:
                u = self.non_preferred.extract()
                self.preferred.insert(u)
                self.sub_open.insert(u)

        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def our_revised_search(self, focal_w=1.5, mode="dpop"):
        # modes \in "dpop", "dfor", "list"  #  focal_w ajusta el rango del focal_search
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.sub_open = MultiBinaryHeap(1)
        if mode == "list":
            self.non_preferred = list()
        else:
            self.non_preferred = deque()
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]

        initial_node.key[0] = self.ftrustvalue(initial_node.g,initial_node.h[0], initial_node.trust)  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.sub_open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        while not self.preferred.is_empty():
            f_min = self.sub_open.top().key[1]
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            n = self.preferred.extract()
            m = self.sub_open.extract(n.heap_index[1])   # extrae m de la open
            assert (n==m)
            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            # print(n.key[1], n.key[0], self.preferred.size)
            succ = n.state.k_accs_successors()
            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                        # print("+ new")
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust * n.trust
                    child_node.key[0] = self.ftrustvalue(child_node.g,child_node.h[0], child_node.trust)
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node

                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min: # estaba en focal o cumple con el rango
                        # if child_node.key[1] <= focal_w*f_min and child_node.heap_index[2]:
                        #     self.non_preferred.extract(child_node.heap_index[2])
                        self.preferred.insert(child_node)
                        self.sub_open.insert(child_node)
                    else:
                        self.non_preferred.append(child_node)

            if f_min < self.sub_open.top().key[1]:
                f_min = self.sub_open.top().key[1]
                if mode == "list":
                    i=0
                    while 1:
                        if i >= len(self.non_preferred):
                            break
                        if self.non_preferred[i].key[1] <= focal_w*f_min:
                            self.non_preferred[i], self.non_preferred[-1] = self.non_preferred[-1], self.non_preferred[i]
                            self.preferred.insert(self.non_preferred[-1])
                            self.sub_open.insert(self.non_preferred[-1])
                            self.non_preferred = self.non_preferred[:-1]
                        else:
                            i += 1
                elif mode == "dfor":
                    d_out = deque()
                    for u in self.non_preferred:
                        if u.key[1] <= focal_w*f_min:
                            self.preferred.insert(u)
                            self.sub_open.insert(u)
                        else:
                            d_out.append(u)
                    self.non_preferred = d_out
                elif mode == "dpop":
                    d_out = deque()
                    while(len(self.non_preferred)):
                        u = self.non_preferred.pop()
                        if u.key[1] <= focal_w*f_min:
                            self.preferred.insert(u)
                            self.sub_open.insert(u)
                        else:
                            d_out.append(u)
                    self.non_preferred = d_out


        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def original_search(self, focal_w=1.5, focal_heuristic=-1):  #  focal_w ajusta el rango del focal_search
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
        initial_node.h[1] = initial_node.h[0]

        initial_node.key[0] = self.ftrustvalue(initial_node.g,initial_node.h[0], initial_node.trust)  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        while not self.preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            f_min = self.open.top().key[1]
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open
            assert (n==m)
            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.k_accs_successors()
            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        self.generated[child_state] = child_node
                        # print("+ new")
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust * n.trust
                    child_node.key[0] = self.h_focales(child_node.g,child_node.h[0], trust, n.trust, focal_heuristic)
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node

                    self.open.insert(child_node)
                    # CAMBIO: n.key[1] -> child_node.key[1]
                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min: # estaba en focal o cumple con el rango
                        self.preferred.insert(child_node)
            # print(self.expansions, self.preferred.size, self.open.size, '\t', f_min, self.open.top().key[1])
            # print(*[(self.open.items[i+1].key[1], "Y" if self.open.items[i+1].heap_index[0] else " ") for i in range(self.open.size)])
            # if f_min > self.open.top().key[1]:
            #     print(f_min, "!<=", self.open.top().key[1])
            if self.open.size and f_min < self.open.top().key[1]:
                self.f_updates += 1
                # t_time = time.process_time()
                for i in range(1, self.open.size+1):
                    if focal_w*self.open.top().key[1] >= self.open.items[i].key[1] > focal_w*f_min:
                        self.preferred.insert(self.open.items[i])
                # self.update_time += time.process_time() - t_time

        # print(*[self.open.items[i+1].key[1] for i in range(self.open.size)])
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        # print("none found")
        return None

    def k_accs_search(self, focal_w=1.5):  #  focal_w ajusta el rango del focal_search
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.sub_open = MultiBinaryHeap(1)
        self.non_preferred = MultiBinaryHeap(2)
        self.expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.h[2] = initial_node.h[0]

        initial_node.key[0] = self.ftrustvalue(initial_node.g,initial_node.h[0], initial_node.trust)  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        initial_node.key[2] = initial_node.key[1]

        self.preferred.insert(initial_node)
        self.sub_open.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        while not self.preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            # debug_status = debug_compare(FocalSearch._file_iter, self.sub_open.top().key[0], self.sub_open.size + self.non_preferred.size, 
            #     self.sub_open.top().key[1] if self.sub_open.size else -1,
            #     self.non_preferred.size, 
            #     self.non_preferred.top().key[1] if self.non_preferred.size else -1)
            if not self.preferred.is_empty():
                queue = self.preferred
                n = queue.extract()
                m = self.sub_open.extract(n.heap_index[1])
                assert (n==m)   # extrae m de la open
            else:
                self.non_pref += 1
                queue = self.non_preferred
                n = queue.extract()

            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            # print(n.key[1], n.key[0], self.preferred.size)
            succ = n.state.k_accs_successors()
            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        child_node.h[2] = child_node.h[0]
                        self.generated[child_state] = child_node
                        # print("+ new")
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    child_node.key[0] = self.ftrustvalue(child_node.g,child_node.h[0], child_node.trust)
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[2] = child_node.key[1]
                    # print(child_node.heap_index[:3])
                    assert bool(child_node.heap_index[1]) == bool(child_node.heap_index[0]) != bool(child_node.heap_index[2]) or not sum(child_node.heap_index[:3])

                    if child_node.heap_index[0]: # estaba en preferred
                        self.preferred.insert(child_node)  # solo actualiza en la practica
                        self.sub_open.insert(child_node)
                    else:
                        self.non_preferred.insert(child_node)
            
            # Obtener incumbente
            incumbent = self.sub_open.top() if self.sub_open.size != 0 else self.non_preferred.top()
            # Ingresar nodos a focal segun incumbente
            node = self.non_preferred.top()
            while (node is not None) and focal_w*incumbent.key[1] >= node.key[1]:
                t_node = self.non_preferred.extract()
                self.preferred.insert(t_node)
                self.sub_open.insert(t_node)
                node = self.non_preferred.top()


        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    # SECTOR LOOK AHEAD + FOCAL SEARCH
    def trustvalue(self, trust):# g, h, trust):
        # el negativo es para ordenarlo en el sentido contrario
        # return (10000*(g + self.weight*h) - g)/trust
        return -trust # /(g+h)


    def accs_look_ahead(self, node, distance):
        '''
            Explora el mejor sucesor de forma greedy buscando, y retornando la heurística,
            Como es greedy, el 'k' no influye
            Recordar que los nodos tienen el mismo h en las tres casillas
        '''
        current_node = node
        # best_h = current_node.h[0]  # new
        for _ in range(distance):
            if current_node.state.is_goal():
                return current_node.h[0]
            succ = current_node.state.k_accs_successors()
            self.ahead_expansions +=1
            parent_node = current_node
            parent_node.trust_key = float("-inf")  # aseguramos que los hijos posean mejor valor
            for child_state, action, cost, trust in succ:
                path_cost = parent_node.g + cost  # costo del camino encontrado hasta child_state
                ## inclusion naive (sin saber de open)
                child_node = MultiNode(child_state, parent_node)
                child_node.h[0] = self.heuristic(child_state)
                # if child_node.h[0] < best_h:  # new
                #     best = child_node.h[0]
                child_node.trust = trust
                child_node.trust_key = trust
                if child_node.trust_key > current_node.trust_key:
                    current_node = child_node
        return current_node.h[0]  # best_h # current_node.h[0]

    
    # def fvalue(self, g, h):
    #     return 10000*(g + self.weight*h) - g  # (g+h, h)

    def search_ahead(self, focal_w=1.5, ahead=1):  #  focal_w ajusta el rango del focal_search
        """
            focal search, pero con look ahead
        """
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.sub_open = MultiBinaryHeap(1)
        self.non_preferred = MultiBinaryHeap(2)
        self.expansions = 0
        self.ahead_expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.h[2] = initial_node.h[0]

        initial_node.key[0] = initial_node.h[0]  # asignamos el valor de h
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        initial_node.key[2] = initial_node.key[1]

        # self.open.insert(initial_node)
        self.non_preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 1
        self.non_pref = 0
        while not self.sub_open.is_empty() or not self.non_preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            if not self.preferred.is_empty():
                queue = self.preferred
                n = queue.extract()
                m = self.sub_open.extract(n.heap_index[1])   # extrae m de la open
            else:
                self.non_pref += 1
                queue = self.non_preferred
                n = queue.extract()

            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            # print(n.key[1], n.key[0], self.preferred.size)
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        child_node.h[2] = child_node.h[0]
                        self.generated[child_state] = child_node
                        # print("+ new")
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    child_node.key[0] = self.accs_look_ahead(child_node, ahead)
                    # print("DEBUG", child_node.key[0])
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[2] = child_node.key[1]

                    if child_node.heap_index[0]: # estaba en preferred
                        assert not child_node.heap_index[2]
                        self.preferred.insert(child_node)
                        self.sub_open.insert(child_node)
                    else:
                        assert not child_node.heap_index[0]
                        self.non_preferred.insert(child_node)
            
            # Obtener incumbente
            incumbent = self.sub_open.top() if self.sub_open.size != 0 else self.non_preferred.top()
            # Ingresar nodos a focal segun incumbente
            node = self.non_preferred.top()
            while (node is not None) and focal_w*incumbent.key[1] > node.key[1]:
                t_node = self.non_preferred.extract()
                self.preferred.insert(t_node)
                self.sub_open.insert(t_node)
                node = self.non_preferred.top()


        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    # INICIO FOCAL BEAM AHEAD

    # def beam_ahead(self, node, beam, distance):
    #     node.key[0] = 10000*(node.g + self.weight*node.h[0]) - node.g # actualizamos el f de child_node
    #     current_nodes = [(None,  node)]  # el primer elemento de la tupla es la prioridad del nodo para descartar en el beam
    #     for _ in range(distance):
    #         next_nodes = []
    #         for __, current_node in current_nodes:
    #             if current_node.state.is_goal():
    #                 return current_node.key
    #             succ = current_node.state.k_accs_successors()
    #             parent_node = current_node
    #             parent_node.trust = 0
    #             self.ahead_expansions += 1
    #             for child_state, action, cost, trust in succ:
    #                 path_cost = parent_node.g + cost  # costo del camino encontrado hasta child_state
    #                 ## inclusion naive (sin saber de open)
    #                 child_node = MultiNode(child_state, parent_node)
    #                 child_node.h[0] = self.heuristic(child_state)
    #                 child_node.action = action
    #                 child_node.parent = parent_node
    #                 child_node.g = path_cost
    #                 child_node.trust = trust
    #                 child_node.key[0] = 10000*(child_node.g + self.weight*child_node.h[0]) - child_node.g # actualizamos el f de child_node
    #                 child_node.trust_key = self.ftrustvalue(child_node.g,child_node.h[0], child_node.trust)# actualizamos el f de 
    #                 heappush(next_nodes, (-child_node.trust_key, child_node))  # mayor trust al inicio
    #         current_nodes = [heappop(next_nodes) for __ in 
    #                             range(min(len(next_nodes), beam))]
                                
    #     return current_nodes[0][1].key[0]

    def beam_ahead_search(self, focal_w=1.5, beam_size=2, ahead=2):  #  focal_w ajusta el rango del focal_search
        # focal := [f, f*focal_w]
        # preferred es focal
        # open = preferred U non_preferred  ; (U = union disjunta)
        self.start_time = time.process_time()
        self.preferred = MultiBinaryHeap(0)
        self.open = MultiBinaryHeap(1)
        self.non_preferred = MultiBinaryHeap(2)
        self.expansions = 0
        self.ahead_expansions = 0

        initial_node = MultiNode(self.initial_state)
        initial_node.g = 0
        initial_node.trust = 1.0
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.h[2] = initial_node.h[0]

        initial_node.key[0] = initial_node.h[0]  # asignamos el valor de h
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        initial_node.key[2] = initial_node.key[1]

        self.open.insert(initial_node)
        self.non_preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        current = 1
        self.non_pref = 0
        while not self.open.is_empty() or not self.preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            if not self.preferred.is_empty():
                queue = self.preferred
            else:
                self.non_pref += 1
                queue = self.non_preferred

            n = queue.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            # print(n.key[1], n.key[0], self.preferred.size)
            succ = n.state.k_accs_successors()
            self.expansions += 1
            t_childs = []  # los hijos aceptables
            for child_state, action, cost, trust in succ:
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
                        child_node.h[1] = child_node.h[0]
                        child_node.h[2] = child_node.h[0]
                        self.generated[child_state] = child_node
                        # print("+ new")
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.trust = trust # * n.trust
                    child_node.key[0] = self.accs_look_ahead(child_node, ahead)
                    # print("DEBUG", child_node.key[0])
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[2] = child_node.key[1]

                    self.open.insert(child_node)
                    if child_node.heap_index[0]: # estaba en preferred
                        # assert not child_node.heap_index[2]
                        self.preferred.insert(child_node)
                    elif child_node.heap_index[2]:  # estaba en open
                        # assert not child_node.heap_index[0]
                        self.non_preferred.insert(child_node)
                    else:
                        t_childs.append(child_node)
            
            # dejar hijos en preferred o non_preferred segun trust
            t_childs.sort(key = lambda x:-x.trust)
            for child in t_childs[:beam_size]:
                self.preferred.insert(child)
            for child in t_childs[beam_size:]:
                self.non_preferred.insert(child)
            
            # Obtener incumbente
            incumbent = self.open.top()
            # Ingresar nodos a focal segun incumbente
            node = self.non_preferred.top()
            while (node is not None) and focal_w*incumbent.key[1] > node.key[1]:
                self.preferred.insert(self.non_preferred.extract())
                node = self.non_preferred.top()


        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None

    def heuristic_search(self, focal_w=1.5):  #  focal_w ajusta el rango del focal_search
        """
        usa original_search de base
        """
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
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]

        initial_node.key[0] = initial_node.h[0]  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        while not self.preferred.is_empty():
            # print('A', [int(x.key[0]) if x is not None else None for x in self.preferred.items[:15] ])
            f_min = self.open.top().key[1]
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open
            assert (n==m)
            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.succ()
            self.expansions += 1
            # for child_state, action, cost, h_nn in succ:
            for child_state in succ:
                # print("? check", child_state.board)
                child_node = self.generated.get(child_state)
                cost = 1
                h_nn = self.heuristic(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = h_nn # h focal
                        child_node.h[1] = self.heuristic(child_state) # h admisible
                        self.generated[child_state] = child_node
                        # print("+ new")
                    # child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    child_node.key[0] = h_nn # h focal
                    child_node.key[1] = self.fvalue(child_node.g,child_node.h[1]) # actualizamos el f de child_node

                    self.open.insert(child_node)
                    # CAMBIO: n.key[1] -> child_node.key[1]
                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min: # estaba en focal o cumple con el rango
                        self.preferred.insert(child_node)
            # print(self.expansions, self.preferred.size, self.open.size, '\t', f_min, self.open.top().key[1])
            # print(*[(self.open.items[i+1].key[1], "Y" if self.open.items[i+1].heap_index[0] else " ") for i in range(self.open.size)])
            # if f_min > self.open.top().key[1]:
            #     print(f_min, "!<=", self.open.top().key[1])
            if self.open.size and f_min < self.open.top().key[1]:
                self.f_updates += 1
                # t_time = time.process_time()
                for i in range(1, self.open.size+1):
                    if focal_w*self.open.top().key[1] >= self.open.items[i].key[1] > focal_w*f_min:
                        self.preferred.insert(self.open.items[i])
                # self.update_time += time.process_time() - t_time

        # print(*[self.open.items[i+1].key[1] for i in range(self.open.size)])
        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        # print("none found")
        return None

    def heuristic_discrepancy_search(self, focal_w=1.5, discrepancy_mode="best"):  #  focal_w ajusta el rango del focal_search
        """
        USA EL original_search de esqueleto
        discrepancy_mode in ["best", "position"]
        best : el mejor es discrepancia 0, los otros 1
        position := discrepancia segun trust (0=mas confiable, y subiendo de a uno por su orden)
        focal search ordenado por (dicrepancia, f)
        """
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
        initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[1] = initial_node.h[0]
        initial_node.key[0] = (0, initial_node.h[0])  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])

        self.open.insert(initial_node)
        self.preferred.insert(initial_node)
        # para cada estado alguna vez generado, generated almacena
        # el Node que le corresponde
        self.generated = {}
        self.generated[self.initial_state] = initial_node
        self.non_pref = 0
        current = 1
        while not self.preferred.is_empty():
            f_min = self.open.top().key[1]
            n = self.preferred.extract()
            m = self.open.extract(n.heap_index[1])   # extrae m de la open

            
            if n.state.is_goal():
                self.end_time = time.process_time()
                self.solution = n
                return n

            succ = n.state.h_successors()

            # quedarse con los beam mejores estados ordenados por trusts
            if discrepancy_mode == "best":
                # obtener el estado de menor h
                best_state = min(succ, key=lambda x: x[3])[0]
            elif discrepancy_mode == "position":
                # crear diccionsrio del estado a su discrepancia
                most_trusted = {state[0] : i for
                                    i, state in enumerate(
                                        sorted(succ, key=lambda x: x[3])
                                    )
                                }
                # assert [s[3] for s in succ].count(max(s[3] for s in succ)) == 1

            self.expansions += 1
            for child_state, action, cost, h_nn in succ:
                # print("? check", child_state.board)
                child_node = self.generated.get(child_state)
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = h_nn
                        child_node.h[1] = self.heuristic(child_state)
                        self.generated[child_state] = child_node
                    child_node.action = action
                    child_node.parent = n
                    child_node.g = path_cost
                    # child_node.trust = h_nn
                    node_discrepancy = n.key[0][0]
                    if discrepancy_mode == "best":
                        if child_state != best_state:
                            node_discrepancy += 1
                    elif discrepancy_mode == "position":
                        node_discrepancy += most_trusted[child_state]

                    child_node.key[1] = self.fvalue(child_node.g, child_node.h[1]) # actualizamos el f de child_node
                    child_node.key[0] = (node_discrepancy,  child_node.h[1])

                    self.open.insert(child_node)
                    if child_node.heap_index[0] or child_node.key[1] <= focal_w*f_min:  # estaba en focal o cumple con el rango
                        self.preferred.insert(child_node)
                # elif path_cost == child_node.g:
                #     node_discrepancy = n.key[0][0]
                #     if discrepancy_mode == "best":
                #         if child_state != best_state:
                #             node_discrepancy += 1
                #     elif discrepancy_mode == "position":
                #         node_discrepancy += most_trusted[child_state]

                #     child_node.key[0] = (min(child_node.key[0][0], node_discrepancy), child_node.key[0][1])
                #     if child_node.heap_index[0]:
                #         self.preferred.insert(child_node)

            # assert f_min <= self.open.top().key[1]
            if self.open.size and f_min < self.open.top().key[1]:
                self.f_updates += 1
                # t_time = time.process_time()
                for i in range(1, self.open.size+1):
                    if focal_w*self.open.top().key[1] >= self.open.items[i].key[1] > focal_w*f_min:
                        self.preferred.insert(self.open.items[i])
                # self.update_time += time.process_time() - t_time

        self.end_time = time.process_time()      # en caso contrario, modifica la posicion de child_node en open
        return None