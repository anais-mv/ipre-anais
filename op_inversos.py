from operadores import operadores_disponibles
from clases import Operador
# from time import time


proposiciones_operadores = set()
nuevos_operadores = set()
# can_op = 0
# inicio = time()
# print("operadores originales: " + str(len(operadores_disponibles)))
for operador in operadores_disponibles:
    # print("creando inverso")
    prec = operador.prec.union(operador.add)
    nuevo_prec = set()
    for proposicion in prec:
        if proposicion not in operador.delet:
            nuevo_prec.add(proposicion)
    nuevo_op = Operador(operador.id, nuevo_prec, operador.delet, operador.add)
    nuevos_operadores.add(nuevo_op)
# tiempo = time() - inicio
# print("tiempo crear operadores: " + str(tiempo))
