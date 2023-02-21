from collections import defaultdict


class DefaultHeuristic:
    def __init__(self):
        self.no_encontrado = 0

    def default_heuristic(self):
        # self.no_encontrado += 1
        return 99999999


def default_heuristic():
    # self.no_encontrado += 1
    return 99999999


class Heuristica:
    def __init__(self, operadores, estados):
        self.open = []
        self.vistos = set()
        self.inicial = estados[-1]
        self.operadores = operadores
        self.explorados = 0
        self.estados = estados
        self.heuristica = defaultdict(default_heuristic)
        self.iniciar()

    def sgte_estado(self):
        siguiente = self.open.pop(0)
        return siguiente

    def explorar(self):
        print("CANTIDAD DE OPERADORES: " + str(len(self.operadores)))
        self.open.append(self.inicial)
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
                        # op_original = self.obtener_op_original(operador)
                        # if op_original.es_aplicable(hijo):
                        #     padre = hijo.aplicar_operador(op_original)
                        #     if padre == estado:
                        #         if hijo.prop not in self.vistos:
                        #             self.open.append(hijo)
                        #             self.vistos.add(hijo.prop)
                        #             self.heuristica[str(hijo.prop)] = hijo.largo
            # if self.explorados % 500 == 0:
            #     print("explorados: " + str(self.explorados))
            if len(self.open) == 0:
                self.continuar = False

    def iniciar(self):
        self.heuristica[self.inicial.prop] = 0
        self.explorar()
        print("can heuristica: " + str(len(self.heuristica)))
        # for estado in self.estados:
        #     if estado.prop not in self.vistos:
        #         self.heuristica[estado.prop] = 1000000000
