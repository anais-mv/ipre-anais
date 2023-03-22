from binary_heap import BinaryHeap
import time


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
        nodo_inicial.key = nodo_inicial.g + nodo_inicial.largo  # asignamos f con peso alto
        self.open.insert(nodo_inicial)  # agregamos el nodo a la open
        self.vistos.add(nodo_inicial.prop)
        while not self.open.is_empty():
            estado = self.open.extract()
            # print("h:", estado.largo, "g:", estado.g, "f:", estado.largo + estado.g)
            if estado.prop == self.final.prop:
                self.tiempo_final = time.process_time() - self.tiempo_inicio
                # print("solución encontrada")
                self.recuperar_camino(estado)
                self.camino = list(reversed(self.camino))
                print("g: " + str(estado.g))
                print("can vistos: " + str(len(self.vistos)))
                return self.camino, self.expansions, self.tiempo_final
            if estado.prop not in self.closed:
                self.expansions += 1
                self.closed.add(estado.prop)
                sucesores = estado.succ()
                for hijo in sucesores:
                    costo_camino = estado.g + 1
                    nuevo = True if hijo.prop not in self.vistos else False
                    if nuevo or costo_camino < hijo.g:
                        hijo.largo = self.heuristic[hijo.prop]
                        if nuevo:
                            self.vistos.add(hijo.prop)
                        hijo.g = costo_camino
                        hijo.key = 10000*(hijo.g + hijo.largo) - hijo.g
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
