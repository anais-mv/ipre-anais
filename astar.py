# from binary_heap import BinaryHeap
import time
from multi_node import MultiNode
from multi_binary_heap import MultiBinaryHeap


class Astar(object):
    def __init__(self, inicial, final, op, heuristica):
        super(Astar, self).__init__()
        self.expansions = 0
        self.vistos = {}
        self.closed = set()
        self.camino = []
        self.inicial = inicial
        self.final = final
        self.heuristica = heuristica
        self.operadores = op
        self.open = MultiBinaryHeap()
        self.no_encontrado = 0

    def heuristic(self, estado):
        return self.heuristica[estado.prop]

    def search(self):
        self.tiempo_inicio = time.process_time()
        nodo_inicial = MultiNode(self.inicial)
        nodo_inicial.g = 0  # asignamos g
        nodo_inicial.h = self.heuristic(self.inicial)  # asignamos h
        nodo_inicial.key = [nodo_inicial.g + nodo_inicial.h] * MultiBinaryHeap.Max  # asignamos f
        self.open.insert(nodo_inicial)  # agregamos el nodo a la open
        self.vistos[self.inicial.prop] = nodo_inicial
        while not self.open.is_empty():
            n = self.open.extract()
            if n.state.is_goal():
                self.tiempo_final = time.process_time() - self.tiempo_inicio
                # print("solución encontrada")
                self.recuperar_camino(n.state)
                self.camino = list(reversed(self.camino))
                print("g: " + str(n.g))
                print("can vistos: " + str(len(self.vistos)))
                return self.camino, self.expansions, self.tiempo_final
            if n.state.prop not in self.closed:
                self.expansions += 1
                self.closed.add(n.state.prop)
                sucesores = n.state.succ()
                for hijo in sucesores:
                    child_node = self.vistos.get(hijo.prop)
                    # vistos get retorna none si no está en vistos (si es nuevo)
                    is_new = child_node is None  # es la primera vez que veo a child_state
                    costo_camino = n.g + 1
                    if is_new or costo_camino < child_node.g:
                        if is_new:
                            child_node = MultiNode(hijo, n)
                            child_node.h = self.heuristic(hijo)
                            self.vistos[hijo.prop] = child_node
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
