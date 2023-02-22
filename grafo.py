from clases import Estado
from copy import copy
from operadores import prop_disponibles, operadores_disponibles, OP_PREDEFINIDOS
import random
# from parametros import min_operadores
# from operadores import can_operadores
import pickle

# min_aplicables = random.randint(min_operadores, can_operadores)
# min_aplicables = random.randint(0, can_operadores)
# print(min_aplicables, len(operadores_disponibles))
min_aplicables = 5
if OP_PREDEFINIDOS:
    GRAFO_PREDEFINIDO = True
else:
    GRAFO_PREDEFINIDO = False


def crear_estado(prop):
    # prop = las proposiciones que existen en el sistema
    # empezamos con un set vacío de proposiciones
    # print(prop)
    proposiciones = set()
    # la cantidad de proposiciones es al azar
    # print("creando estado")
    # print(type(prop))
    # print(len(prop))
    can = random.randint(0, len(prop))
    # print(can)
    copia = copy(prop)
    # se escogen las proposiciones que tendrá el estado
    for i in range(0, can):
        proposicion = int(random.choice(copia))
        copia.remove(proposicion)
        proposiciones.add(proposicion)
    # se crea el estado
    estado = Estado(proposiciones)
    return estado


def crear_estado_inicial(prop, min_op_aplicables, operadores):
    # min_op_aplicables = la cantidad mínima de operadores aplicables en el estado para poder
    #                     usarlo como estado inicial
    # operadores = los operadores que existen en el sistema
    estado = crear_estado(prop)
    op_aplicables = 0
    # vemos cuantos operadores de los existentes se pueden aplicar en él
    for operador in operadores:
        if operador.es_aplicable(estado) is True:
            op_aplicables += 1
    # si la cantidad de operadores aplicables es mayor o igual a la cantidad mínima
    # lo devolvemos como estado inicial
    # print(op_aplicables)
    if op_aplicables >= min_op_aplicables:
        # print("tenemos " + str(op_aplicables) + " operadores aplicables")
        return estado
    # sino creamos otro
    else:
        return crear_estado_inicial(prop, min_op_aplicables, operadores)


# FUNCIÓN RECURSIVA ELIMINADA
def agregar_estado(padre, estados_prop, estados):
    hijos = []
    for operador in operadores_disponibles:
        if operador.es_aplicable(padre):
            hijo = padre.aplicar_operador(operador)
            if hijo.prop not in estados_prop:
                estados_prop.append(hijo.prop)
                hijos.append(hijo)
                estados.append(hijo)
    if len(hijos) != 0:
        for hijo in hijos:
            return agregar_estado(hijo, estados_prop, estados)
    else:
        return estados


def obtener_proposiciones(estado):
    return estado.prop


maximo = False
if GRAFO_PREDEFINIDO:
    file = open("grafo.json", "rb")
    estados = pickle.load(file)
    file.close()
    estado_inicial = estados[0]
else:
    estado_inicial = crear_estado_inicial(prop_disponibles, min_aplicables, operadores_disponibles)
    estados_prop = [estado_inicial.prop]
    estados = [estado_inicial]
    open_ = [estado_inicial]
    while len(open_) != 0 and maximo is False:
        estado = open_.pop(0)
        for operador in operadores_disponibles:
            if operador.es_aplicable(estado):
                hijo = estado.aplicar_operador(operador)
                # print(type(hijo))
                # print("can actual: " + str(len(estados)))
                if hijo.prop not in estados_prop:
                    estados.append(hijo)
                    open_.append(hijo)
                    estados_prop.append(hijo.prop)
                    if len(estados) % 50000 == 0:
                        print(len(estados))
    file = open("grafo.json", "wb")
    pickle.dump(estados, file)
    file.close()


# try:
#     estados = agregar_estado(estado_inicial, [estado_inicial.prop], [estado_inicial])
# except RecursionError:
#     print("error de recursión")
#     print("mínimo aplicables: " + str(min_aplicables))
#     print("operadores: " + str(can_operadores))
#     print(estado_inicial)
#     print("nuevo intento: ")

# bien = 0
# for estado in estados:
#     cuenta = estados.count(estado)
#     if cuenta == 1:
#         bien += 1

print("cantidad estados: " + str(len(estados)))
estado_objetivo = random.choice(estados)
# estado_objetivo = estados[-1]
