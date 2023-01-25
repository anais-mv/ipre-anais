from operadores import operadores_disponibles
from clases import Operador
import itertools
from time import time


def pot(lista):
    combinaciones = set()
    for L in range(len(lista) + 1):
        for subset in itertools.combinations(lista, L):
            combinaciones.add(frozenset(subset))
    # print("cantidad combinaciones: " + str(len(combinaciones)))
    return combinaciones


def obtener_proposiciones_estado(estado):
    return estado.prop


proposiciones_operadores = set()
nuevos_operadores = set()
# can_op = 0
inicio = time()
print("operadores originales: " + str(len(operadores_disponibles)))
for operador in operadores_disponibles:
    prec = operador.prec.union(operador.add)
    nuevo_prec = set()
    for proposicion in prec:
        if proposicion not in operador.delet:
            nuevo_prec.add(proposicion)
    combinaciones_delet = pot(operador.add)
    for combinacion in combinaciones_delet:
        nuevo_op = Operador(operador.id, nuevo_prec, operador.delet, combinacion)
        # can_op += 1
        proposiciones_op = {nuevo_op.prec, nuevo_op.add, nuevo_op.delet}
        if proposiciones_op not in proposiciones_operadores:
            proposiciones_operadores.add(frozenset(proposiciones_op))
            nuevos_operadores.add(nuevo_op)
tiempo = time() - inicio
print("tiempo crear operadores: " + str(tiempo))
