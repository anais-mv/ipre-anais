# from binary_heap import BinaryHeap
import time
from binary_heap import BinaryHeap
from node import Node
from multi_node import MultiNode
from multi_binary_heap import MultiBinaryHeap
from pyperplan.pddl.pddl import Domain 
from pyperplan.task import Task, Operator
from planning_problem import Estado

from pyperplan.heuristics.blind import BlindHeuristic
from pyperplan.heuristics.lm_cut import LmCutHeuristic
from pyperplan.search.searchspace import SearchNode
from pyperplan.heuristics.relaxation import hFFHeuristic


class Astar(object):
    def __init__(self, inicial, final, op, heuristica, prop, weight, h_type="lmcut"):
        super(Astar, self).__init__()
        self.expansions = 0
        self.vistos = {}
        self.closed = set()
        self.camino = []
        self.inicial = inicial.prop
        self.final = final.prop
        self.heuristica = heuristica
        self.operadores = op
        # self.open = BinaryHeap()
        self.no_encontrado = 0
        self.pyperplan_operators = []
        self.weight = weight
        for op in self.operadores:
            op_pyperplan = Operator("op"+str(op.id), op.prec, op.add, op.delet)
            self.pyperplan_operators.append(op_pyperplan)
        self.pyperplan_task = Task("task", set(prop), self.inicial, self.final, self.pyperplan_operators)
        if h_type == "lmcut":
            self.h_function = LmCutHeuristic(self.pyperplan_task)
        elif h_type == "h*":
            self.h_function = self.perfect_heuristic
        elif h_type == "hff":
            self.h_function = hFFHeuristic(self.pyperplan_task)
        elif h_type == "ph_2":
            self.h_function = self.perfect_heuristic_div2
        elif h_type == "zero":
            def zero(state):
                return 0
            self.h_function = zero 

    def perfect_heuristic(self, estado):
        return self.heuristica[estado.state]
    
    def perfect_heuristic_div2(self, estado):
        return self.heuristica[estado.state]/2
    
    def pyperplan_lmcut_heuristic(self, estado):
        sn = estado.to_pyperplan_search_node()
        return self.h_lmcut(sn)

    def is_goal(self, estado):
        for prop in self.final:
            if prop not in estado:
                return False
        return True

    def search(self):
        self.open = BinaryHeap()
        self.tiempo_inicio = time.process_time()
        nodo_inicial = Node(self.inicial)
        nodo_inicial.g = 0  # asignamos g
        nodo_inicial.h = self.h_function(nodo_inicial)
        nodo_inicial.key = nodo_inicial.g + nodo_inicial.h  # asignamos f
        self.open.insert(nodo_inicial)  # agregamos el nodo a la open
        self.vistos[self.inicial] = nodo_inicial
        while not self.open.is_empty():
            n = self.open.extract()
            if self.is_goal(n.state):
                self.tiempo_final = time.process_time() - self.tiempo_inicio
                self.camino = list(reversed(self.camino))
                self.g_final = n.g
                print("g: " + str(n.g))
                return self.camino, self.expansions, self.tiempo_final
            if n.state not in self.closed:
                self.expansions += 1
                self.closed.add(n.state)
                estado_n = Estado(n.state, self.operadores)
                sucesores = estado_n.succ()
                for hijo in sucesores:
                    child_node = self.vistos.get(hijo)
                    # vistos get retorna none si no está en vistos (si es nuevo)
                    is_new = child_node is None  # es la primera vez que veo a child_state
                    costo_camino = n.g + 1
                    if is_new or costo_camino < child_node.g:
                        if is_new:
                            child_node = Node(hijo, n)
                            child_node.h = self.h_function(child_node)
                            self.vistos[hijo] = child_node
                        child_node.g = costo_camino
                        # child_node_key = [self.weight*(child_node.g + child_node.h) - child_node.g]
                        child_node.key = 10000*(child_node.g + self.weight*child_node.h) - child_node.g
                        # child_node.key = child_node_key * MultiBinaryHeap.Max
                        self.open.insert(child_node)
        self.tiempo_final = time.process_time()
        return None

    def recuperar_camino(self, estado):
        if estado is not None:
            padre = estado.padre
        op = estado.op_anterior
        if op is not None:
            self.camino.append(op)
        if padre != self.inicial and padre is not None:
            self.recuperar_camino(padre)
