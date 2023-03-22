import random
from copy import copy
from clases import Operador
import numpy as np
from parametros import min_prop, max_prop, min_operadores, max_operadores, rango, max_add
import pickle

can_prop = random.randint(min_prop, max_prop)
can_operadores = random.randint(min_operadores, max_operadores)
prop_disponibles = list(np.linspace(1, can_prop, can_prop))
OP_PREDEFINIDOS = False


def crear_prec(can, proposiciones):
    prec = set()
    copia = copy(proposiciones)
    for i in range(0, can):
        proposicion = random.choice(copia)
        copia.remove(proposicion)
        prec.add(proposicion)
    return (prec, copia)


def crear_add(can, proposiciones):
    add = set()
    copia = copy(proposiciones)
    for i in range(0, can):
        proposicion = random.choice(copia)
        copia.remove(proposicion)
        add.add(proposicion)
    return add


def crear_del(can, proposiciones):
    delet = set()
    copia = copy(proposiciones)
    for i in range(0, can):
        proposicion = random.choice(copia)
        copia.remove(proposicion)
        delet.add(proposicion)
    return delet


def crear_operadores(max_p, min_p, max_op, min_op, rango, max_add):
    can_prop = random.randint(min_p, max_p)
    prop_disponibles = list(np.linspace(1, can_prop, can_prop))
    can_operadores = random.randint(min_op, max_op)
    operadores_disponibles = set()
    set_operadores = set()
    for i in range(0, can_operadores):
        can_prec = random.randint(1, can_prop - rango)
        prec, prop_sin_prec = crear_prec(can_prec, prop_disponibles)
        if max_add > len(prop_sin_prec):
            can_add = random.randint(1, len(prop_sin_prec))
        else:
            can_add = random.randint(1, max_add)
        add = crear_add(can_add, prop_sin_prec)
        can_del = random.randint(0, can_prec)  # esto es porque del debe ser un subconjunto de prec
        delet = crear_del(can_del, list(prec))  # solo escogemos proposiciones que estén en prec
        operador = Operador(i, prec, add, delet)
        operadores_disponibles.add(operador)
        set_operadores.add((operador.prec, operador.add, operador.delet))
    # OPERADORES INVERSOS
    nuevos_operadores = set()
    for operador in operadores_disponibles:
        prec = operador.prec.union(operador.add)
        nuevo_prec = set()
        for proposicion in prec:
            if proposicion not in operador.delet:
                nuevo_prec.add(proposicion)
        nuevo_op = Operador(operador.id, nuevo_prec, operador.delet, operador.add)
        if (nuevo_op.prec, nuevo_op.add, nuevo_op.delet) not in set_operadores:
            nuevos_operadores.add(nuevo_op)
    for op in nuevos_operadores:
        operadores_disponibles.add(op)
    datos = (prop_disponibles, can_prop, can_operadores)
    return operadores_disponibles, datos


if OP_PREDEFINIDOS:
    file = open("op.json", "rb")
    operadores_disponibles = pickle.load(file)
    file.close()
else:
    operadores_disponibles = set()
    set_operadores = set()
    for i in range(0, can_operadores):
        can_prec = random.randint(1, can_prop - rango)
        prec, prop_sin_prec = crear_prec(can_prec, prop_disponibles)
        # print("cantidad de prop disp: " + str(len(prop_disponibles)))
        # can_add = random.randint(0, len(prop_sin_prec)) # CAMBIAR CANTIDAD DE PROPOSICIONES EN ADD
        if max_add > len(prop_sin_prec):
            can_add = random.randint(1, len(prop_sin_prec))
        else:
            can_add = random.randint(1, max_add)
        add = crear_add(can_add, prop_sin_prec)
        can_del = random.randint(0, can_prec)  # esto es porque del debe ser un subconjunto de prec
        delet = crear_del(can_del, list(prec))  # solo escogemos proposiciones que estén en prec
        operador = Operador(i, prec, add, delet)
        operadores_disponibles.add(operador)
        set_operadores.add((operador.prec, operador.add, operador.delet))
    # OPERADORES INVERSOS
    proposiciones_operadores = set()
    nuevos_operadores = set()
    for operador in operadores_disponibles:
        prec = operador.prec.union(operador.add)
        nuevo_prec = set()
        for proposicion in prec:
            if proposicion not in operador.delet:
                nuevo_prec.add(proposicion)
        nuevo_op = Operador(operador.id, nuevo_prec, operador.delet, operador.add)
        if (nuevo_op.prec, nuevo_op.add, nuevo_op.delet) not in set_operadores:
            nuevos_operadores.add(nuevo_op)
    for op in nuevos_operadores:
        operadores_disponibles.add(op)
    file = open("op.json", "wb")
    pickle.dump(operadores_disponibles, file)
    file.close()
