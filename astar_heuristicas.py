from collections import defaultdict


class DefaultHeuristic:
    def __init__(self):
        self.no_encontrado = 0

    def default_heuristic(self):
        return 99999999


def default_heuristic():
    return 99999999


class Heuristica:
    def __init__(self, operadores, estados, obj):
        self.open = []
        self.vistos = set()
        self.inicial = obj
        self.operadores = operadores
        self.explorados = 0
        self.estados = estados
        self.heuristica = defaultdict(default_heuristic)
        self.iniciar()

    def zero_heuristic(self, estado):
        return 0

    def sgte_estado(self):
        siguiente = self.open.pop(0)
        return siguiente

    def explorar(self):
        self.open.append(self.inicial)
        self.vistos.add(self.inicial.prop)
        self.heuristica[self.inicial.prop] = 0
        while len(self.open) != 0:
            estado = self.sgte_estado()
            self.explorados += 1
            for operador in self.operadores:
                if operador.es_aplicable(estado):
                    hijo = estado.aplicar_operador(operador)
                    hijo.largo = estado.largo + 1
                    if hijo.prop not in self.vistos:
                        self.open.append(hijo)
                        self.vistos.add(hijo.prop)
                        if hijo in self.estados:
                            self.heuristica[hijo.prop] = hijo.largo
            if len(self.open) == 0:
                self.continuar = False

    def iniciar(self):
        self.heuristica[self.inicial.prop] = 0
        self.explorar()
