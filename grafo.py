from planning_problem import Estado
from copy import copy
# from operadores import prop_disponibles, operadores_disponibles, OP_PREDEFINIDOS, can_prop
from operadores import OP_PREDEFINIDOS
import random
import pickle


if OP_PREDEFINIDOS:
    GRAFO_PREDEFINIDO = True
else:
    GRAFO_PREDEFINIDO = False


def crear_estado(prop, operadores):
    # prop = las proposiciones que existen en el sistema
    # empezamos con un set vacío de proposiciones
    proposiciones = set()
    # la cantidad de proposiciones es al azar
    can = random.randint(0, len(prop))
    copia = copy(prop)
    # se escogen las proposiciones que tendrá el estado
    for i in range(0, can):
        proposicion = str(random.choice(copia))
        copia.remove(proposicion)
        proposiciones.add(proposicion)
    # se crea el estado
    estado = Estado(proposiciones, operadores)
    return estado


def crear_estado_inicial(prop, min_op_aplicables, operadores):
    # min_op_aplicables = la cantidad mínima de operadores aplicables en el estado para poder
    #                     usarlo como estado inicial
    # operadores = los operadores que existen en el sistema
    estado = crear_estado(prop, operadores)
    op_aplicables = 0
    # vemos cuantos operadores de los existentes se pueden aplicar en él
    for operador in operadores:
        if operador.es_aplicable(estado) is True:
            op_aplicables += 1
    # si la cantidad de operadores aplicables es mayor o igual a la cantidad mínima
    # lo devolvemos como estado inicial
    if op_aplicables >= min_op_aplicables:
        return estado
    # sino creamos otro
    else:
        return crear_estado_inicial(prop, min_op_aplicables, operadores)


class Grafo():
    def __init__(self, proposiciones_disp, minimo_aplicable, op_disponibles, est):
        self.estadisticas = None
        self.prop_disp = proposiciones_disp
        self.min_ap = minimo_aplicable
        self.op_disp = op_disponibles
        self.estadisticas = est
        self.crear_grafo()

    def crear_grafo(self):
        self.estado_inicial = crear_estado_inicial(self.prop_disp, self.min_ap, self.op_disp)
        self.estados = {self.estado_inicial}
        open_ = [self.estado_inicial]
        while len(open_) != 0:
            estado = open_.pop(0)
            for operador in self.op_disp:
                if operador.es_aplicable(estado):
                    hijo = estado.aplicar_operador(operador)
                    if hijo not in self.estados:
                        self.estados.add(hijo)
                        open_.append(hijo)
                        if len(self.estados) % 50000 == 0:
                            print(len(self.estados))
        self.estadisticas["can_op"] = len(self.op_disp)
        self.estadisticas["can_prop"] = len(self.prop_disp)

    def guardar_grafo(self, nombre):
        file = open(nombre, "wb")
        pickle.dump(self, file)
        file.close()

    def obtener_estado_objetivo(self):
        lista_estados = list(self.estados)
        estado_objetivo = random.choice(lista_estados)
        return estado_objetivo


def cargar_grafo(nombre):
    file = open(nombre, "rb")
    estados = pickle.load(file)
    file.close()
    return estados
