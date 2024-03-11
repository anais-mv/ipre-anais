from grafo import Grafo, cargar_grafo
from astar_heuristicas import Heuristica
from aristas import nuevos_operadores, revisar_h_diferentes, nuevos_operadores_alternativo
import time

def can_prop(grafo):
    mayores = []
    for estado in grafo.estados:
        lista_props = list(estado.prop)
        props = [int(num) for num in lista_props]
        mayor_estado = max(props)
        mayores.append(mayor_estado)
    return max(mayores)

file_name = "grafos//grafo_2023-11-10 12.54.23.991920_--can_prop=22--can_op=450--rango=1--max_add=20--min_ap=2.pickle"
grafo = cargar_grafo(file_name)
estado_objetivo = list(grafo.estados)[0].goal
grafo.objetivo = estado_objetivo
dic_h = grafo.perfect_heuristic.heuristica

inicio = time.process_time()
print("Creando aristas...")
# op_aristas = nuevos_operadores(grafo, args.can_prop, args.can_op, args.rango, args.max_add)
# op_aristas = nuevos_operadores_alternativo(grafo)
nuevos_op = nuevos_operadores(grafo, can_prop(grafo), 10000, 3, 2)
lista_op_aristas = list(nuevos_op) # + list(op_aristas)
op_aristas = set(lista_op_aristas)
print("nuevos total:", len(op_aristas))

print(f"Tiempo en crear aristas: {time.process_time() - inicio}")
    
inicio = time.process_time()
# print("Creando heurística aristas...")
grafo.h_aristas = Heuristica(op_aristas, grafo.estados, estado_objetivo).heuristica
print(f"Tiempo en crear heurística aristas: {time.process_time() - inicio}")

revisar_h_diferentes(grafo, dic_h, grafo.h_aristas)

file_name.replace(".pickle", "")
# grafo.guardar_grafo(file_name + " ARISTAS.pickle")
grafo.guardar_grafo(file_name)