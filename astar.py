# from binary_heap import BinaryHeap
import time
from multi_node import MultiNode
from multi_binary_heap import MultiBinaryHeap
from pyperplan.pddl.pddl import Domain 
from pyperplan.task import Task, Operator
from planning_problem import Estado

from pyperplan.heuristics.blind import BlindHeuristic
from pyperplan.heuristics.lm_cut import LmCutHeuristic
from pyperplan.search.searchspace import SearchNode


class Astar(object):
    def __init__(self, inicial, final, op, heuristica, prop):
        super(Astar, self).__init__()
        self.expansions = 0
        self.vistos = {}
        self.closed = set()
        self.camino = []
        self.inicial = inicial.prop
        self.final = final.prop
        self.heuristica = heuristica
        self.operadores = op
        self.open = MultiBinaryHeap()
        self.no_encontrado = 0
        self.pyperplan_operators = []
        for op in self.operadores:
            op_pyperplan = Operator("op"+str(op.id), op.prec, op.add, op.delet)
            self.pyperplan_operators.append(op_pyperplan)
        self.pyperplan_task = Task("task", set(prop), self.inicial, self.final, self.pyperplan_operators)
        self.h_lmcut = LmCutHeuristic(self.pyperplan_task)

    def heuristic(self, estado):
        return self.heuristica[estado.prop]

    def search(self):
        self.tiempo_inicio = time.process_time()
        nodo_inicial = MultiNode(self.inicial)
        nodo_inicial.g = 0  # asignamos g
        # nodo_inicial.h = self.heuristic(self.inicial)  # asignamos h
        sn = nodo_inicial.to_pyperplan_search_node()
        nodo_inicial.h = self.h_lmcut(sn)
        nodo_inicial.key = [nodo_inicial.g + nodo_inicial.h] * MultiBinaryHeap.Max  # asignamos f
        self.open.insert(nodo_inicial)  # agregamos el nodo a la open
        self.vistos[self.inicial] = nodo_inicial
        while not self.open.is_empty():
            n = self.open.extract()
            # if n.state.is_goal():
            if n.state == self.pyperplan_task.goals:
                self.tiempo_final = time.process_time() - self.tiempo_inicio
                # print("solución encontrada")
                # self.recuperar_camino(n.state)
                self.camino = list(reversed(self.camino))
                print("g: " + str(n.g))
                print("can vistos: " + str(len(self.vistos)))
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
                            child_node = MultiNode(hijo, n)
                            # child_node.h = self.heuristic(hijo)
                            child_node.h = self.h_lmcut(child_node.to_pyperplan_search_node())
                            # print("heuristic hlmcut:", child_node.h)
                            self.vistos[hijo] = child_node
                        child_node.g = costo_camino
                        child_node_key = [10000*(child_node.g + child_node.h) - child_node.g]
                        child_node.key = child_node_key * MultiBinaryHeap.Max
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
