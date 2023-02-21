from grafo import estados, estado_inicial, estado_objetivo
from operadores import operadores_disponibles
# from op_inversos import nuevos_operadores
from astar_heuristicas import Heuristica
from binary_heap import BinaryHeap
import time


inicio = time.process_time()
busqueda = Heuristica(operadores_disponibles, estados)
tiempo_total = time.process_time() - inicio
print("tiempo crear heurística: " + str(tiempo_total))


class Astar(object):
    def __init__(self, inicial, final, op, heuristica):
        super(Astar, self).__init__()
        self.expansions = 0
        self.vistos = set()
        self.closed = set()
        self.camino = []
        self.inicial = inicial
        self.final = final
        self.heuristic = heuristica
        self.operadores = op
        self.open = BinaryHeap()
        self.no_encontrado = 0

    def search(self):
        self.tiempo_inicio = time.process_time()
        nodo_inicial = self.inicial
        nodo_inicial.g = 0  # asignamos g
        nodo_inicial.largo = self.heuristic[self.inicial.prop]  # asignamos h
        nodo_inicial.key = nodo_inicial.g + nodo_inicial.largo*1000  # asignamos f con peso alto
        self.open.insert(nodo_inicial)  # agregamos el nodo a la open
        self.vistos.add(nodo_inicial.prop)
        while not self.open.is_empty():
            estado = self.open.extract()
            if estado == estado_objetivo:
                self.tiempo_final = time.process_time() - self.tiempo_inicio
                # print("solución encontrada")
                self.recuperar_camino(estado)
                self.camino = list(reversed(self.camino))
                print("g: " + str(estado.g))
                print("can vistos: " + str(len(self.vistos)))
                return self.camino, self.expansions, self.tiempo_final
            if estado.prop not in self.closed:
                op_aplicados = 0
                self.expansions += 1
                self.closed.add(estado.prop)
                for op in self.operadores:
                    if op.es_aplicable(estado):
                        op_aplicados += 1
                        hijo = estado.aplicar_operador(op)
                        costo_camino = estado.g + op_aplicados
                        nuevo = True if hijo.prop not in self.vistos else False
                        if nuevo or costo_camino < hijo.g:
                            if nuevo:
                                self.vistos.add(hijo.prop)
                                hijo.largo = self.heuristic[hijo.prop]
                                if hijo.largo == 99999999:
                                    self.no_encontrado += 1
                            hijo.g = costo_camino
                            hijo.key = hijo.g + hijo.largo
                            self.open.insert(hijo)
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


a_star = Astar(estado_inicial, estado_objetivo, operadores_disponibles, busqueda.heuristica)
sol, exp, tim = a_star.search()
# print("probando solución")
print("can no encontrado: " + str(a_star.no_encontrado))
estado_actual = estado_inicial
for op in sol:
    estado_actual = estado_actual.aplicar_operador(op)
if estado_actual.prop == estado_objetivo.prop:
    print("CORRECTO")
    print("nodos expandidos: " + str(exp))
    print("tiempo: " + str(tim))
else:
    print("INCORRECTO")
