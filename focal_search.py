from multi_binary_heap import MultiBinaryHeap
from multi_node import MultiNode
import time
import sys
from heapq import heappush, heappop  # para beam_ahead
# from common.debug import debug_compare
from math import log2
from collections import deque
from planning_problem import Estado
import random

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
        self.initial_state = initial_state.prop
        self.weight = weight
        self.heuristic = heuristic
        self.goal = initial_state.goal.prop
        self.operadores = initial_state.operadores
        self.mse = 0.0

    def is_goal(self, state):
        for prop in self.goal:
            if prop not in state:
                return False
        return True

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

            
            # if n.state.is_goal():
            if self.is_goal(n.state):
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

    # SECTOR LOOK AHEAD + FOCAL SEARCH
    def trustvalue(self, trust):# g, h, trust):
        # el negativo es para ordenarlo en el sentido contrario
        # return (10000*(g + self.weight*h) - g)/trust
        return -trust # /(g+h)

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
        # initial_node.h[0] = self.heuristic(self.initial_state)
        initial_node.h[0] = self.heuristic(initial_node)
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

            if self.is_goal(n.state):
                self.end_time = time.process_time()
                self.solution = n
                return n

            estado_n = Estado(n.state, self.operadores)
            succ = estado_n.succ()
            self.expansions += 1
            # for child_state, action, cost, h_nn in succ:
            for child_state in succ:
                # print("? check", child_state.board)
                child_node = self.generated.get(child_state)
                cost = 1
                # H ADMISIBLE -- CAMBIAR
                h_nn = self.heuristic(MultiNode(child_state, n))
                is_new = child_node is None  # es la primera vez que veo a child_state
                path_cost = n.g + cost  # costo del camino encontrado hasta child_state
                if is_new or path_cost < child_node.g:
                    # si vemos el estado child_state por primera vez o lo vemos por
                    # un mejor camino, entonces lo agregamos a open
                    if is_new:  # creamos el nodo de child_state
                        child_node = MultiNode(child_state, n)
                        child_node.h[0] = h_nn # h focal
                        # child_node.h[1] = self.heuristic(child_state) # h admisible
                        child_node.h[1] = self.heuristic(child_node)
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
        depth = initial_node.depth
        initial_node.g = 0
        initial_node.h[0] = depth + self.constant_c * random.gauss(0, 1) * (depth**self.constant_k)
        initial_node.h[1] = self.heuristic(initial_node)
        initial_node.key[0] = (0, initial_node.h[0])  # asignamos el valor f
        initial_node.key[1] = self.fvalue(initial_node.g,initial_node.h[1])
        initial_node.h_nn = initial_node.h[1]

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
            self.mse += (n.h[0] - n.depth)**2

            
            if self.is_goal(n.state):
                self.end_time = time.process_time()
                self.solution = n
                return n

            estado_n = Estado(n.state, self.operadores)
            succ = estado_n.succ()
            succ_h_nn = []
            for sucesor in succ:
                nodo_sucesor = MultiNode(sucesor)
                depth = nodo_sucesor.depth
                h_nn = depth + self.constant_c * random.gauss(0, 1) * (depth**self.constant_k)
                succ_h_nn.append((sucesor, "action name", 1, h_nn))

            # quedarse con los beam mejores estados ordenados por trusts
            if discrepancy_mode == "best":
                # obtener el estado de menor h
                best_state = min(succ_h_nn, key=lambda x: x[3])[0]
            elif discrepancy_mode == "position":
                # crear diccionsrio del estado a su discrepancia
                most_trusted = {state[0] : i for
                                    i, state in enumerate(
                                        sorted(succ_h_nn, key=lambda x: x[3])
                                    )
                                }
                # assert [s[3] for s in succ].count(max(s[3] for s in succ)) == 1

            self.expansions += 1
            for child_state, action, cost, h_nn in succ_h_nn:
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
                        child_node.h[1] = self.heuristic(child_node)
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