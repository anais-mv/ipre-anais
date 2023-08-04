from planning_problem import Estado
from copy import copy
# from operadores import prop_disponibles, operadores_disponibles, OP_PREDEFINIDOS, can_prop
from operadores import OP_PREDEFINIDOS
import random
import pickle
import numpy as np


if OP_PREDEFINIDOS:
    GRAFO_PREDEFINIDO = True
else:
    GRAFO_PREDEFINIDO = False


def prop_positivos(prop):
    prop_final = []
    for proposicion in prop:
        if int(proposicion) > 0:
            prop_final.append(proposicion)
    return prop_final


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
    # se agregan las proposiciones negativas
    for i in range(1, len(prop) + 1):
        num_str = str(i)
        if num_str not in proposiciones:
            negativo = -i
            proposiciones.add(str(negativo))
    # se crea el estado
    estado = Estado(proposiciones, operadores)
    return estado


def crear_estado_inicial(prop, min_op_aplicables, operadores):
    # min_op_aplicables = la cantidad mínima de operadores aplicables en el estado para poder
    #                     usarlo como estado inicial
    # operadores = los operadores que existen en el sistema
    prop = prop_positivos(prop)
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
        self.expansiones = 0
        # self.max = max_succ
        self.crear_grafo()

    def crear_grafo(self):
        self.estado_inicial = crear_estado_inicial(self.prop_disp, self.min_ap, self.op_disp)
        self.estados = {self.estado_inicial}
        open_ = [self.estado_inicial]
        self.contador = 0
        aplicados_lista = []
        while len(open_) != 0:
            estado = open_.pop(0)
            hijos_estado = 0
            aplicados = 0
            for operador in self.op_disp:
                if operador.es_aplicable(estado):
                # if operador.es_aplicable(estado) and hijos_estado < self.max:
                    hijo = estado.aplicar_operador(operador)
                    if hijo not in self.estados:
                        aplicados += 1
                        hijos_estado += 1
                        self.contador += 1
                        hijo.lugar = self.contador
                        self.estados.add(hijo)
                        open_.append(hijo)
                        if len(self.estados) % 50000 == 0:
                            print(len(self.estados))
            if hijos_estado != 0:
                self.expansiones += 1
                aplicados_lista.append(aplicados)
        self.estadisticas["can_op"] = len(self.op_disp)
        self.estadisticas["can_prop"] = len(self.prop_disp)
        self.promedio_exp = np.mean(aplicados_lista)

    def guardar_grafo(self, nombre):
        file = open(nombre, "wb")
        pickle.dump(self, file)
        file.close()

    def obtener_estado_objetivo(self):
        lista_estados = list(self.estados)
        for estado in lista_estados:
            if estado.lugar == self.contador:
                # print(estado.lugar)
                estado_objetivo = estado
        # estado_objetivo = random.choice(lista_estados)
        return estado_objetivo
    
    def obtener_aleatorio_inicial(self):
        lista_estados = list(self.estados)
        inicial = random.choice(lista_estados)
        return inicial


def cargar_grafo(nombre):
    file = open(nombre, "rb")
    estados = pickle.load(file)
    file.close()
    return estados
