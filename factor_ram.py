from grafo import cargar_grafo
import numpy as np

file_name = "grafos//grafo_NUEVO_2023-08-27 22.33.24.589415_--can_prop=16--can_op=100--rango=5--max_add=2--min_ap=3.pickle"
grafo = cargar_grafo(file_name)
print(grafo.estado_inicial)

grafo_estados = {grafo.estado_inicial}
open_ = [grafo.estado_inicial]
contador = 0
aplicados_lista = []
expansiones = 0
while len(open_) != 0:
    estado = open_.pop(0)
    hijos_estado = 0
    aplicados = 0
    for operador in grafo.op_disp:
        if operador.es_aplicable(estado):
        # if operador.es_aplicable(estado) and hijos_estado < self.max:
            hijo = estado.aplicar_operador(operador)
            if hijo not in grafo_estados:
                aplicados += 1
                hijos_estado += 1
                contador += 1
                hijo.lugar = contador
                grafo_estados.add(hijo)
                open_.append(hijo)
                if len(grafo_estados) % 10000 == 0:
                    print(len(grafo_estados))
    if hijos_estado != 0:
        expansiones += 1
        aplicados_lista.append(aplicados)
promedio_exp = np.mean(aplicados_lista)
maximo_exp = max(aplicados_lista)
mediana_exp = np.median(aplicados_lista)

print(f"PROMEDIO FACTOR RAMIFICACIÓN: {promedio_exp}")
print(f"MÁXIMA RAMIFICACIÓN: {maximo_exp}")
print(f"MEDIANA FACTOR RAMIFICACIÓN: {mediana_exp}")