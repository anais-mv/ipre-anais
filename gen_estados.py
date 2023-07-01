from clases import Estado
from operadores import prop_disponibles, operadores_disponibles
import random
from copy import copy


def crear_estado(prop):
    proposiciones = []
    can = random.randint(0, len(prop))
    copia = copy(prop)
    for i in range(0, can):
        proposicion = random.choice(copia)
        copia.remove(proposicion)
        proposiciones.append(proposicion)
    estado = Estado(proposiciones)
    return estado


estado = crear_estado(prop_disponibles)
aplicar = random.randint(0, len(operadores_disponibles))
copia_op = copy(operadores_disponibles)
for i in range(0, aplicar):
    op = random.choice(copia_op)
    copia_op.remove(op)
    print("----------------------APLICANDO OPERADOR----------------------")
    print(op)
    print(estado.prop)
    estado.aplicar_operador(op)
    print(estado.prop)
