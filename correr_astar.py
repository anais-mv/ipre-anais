from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos
import pickle

file_name = "grafos//grafo_2023-09-13 14.25.29.283928_--can_prop=21--can_op=200--rango=3--max_add=4--min_ap=2.pickle"
grafo = cargar_grafo(file_name)
weights = [1.5, 2, 4]
weight_15 = []
weight_2 = []
weight_4 = []
objetivo = grafo.objetivo
op = grafo.op_disp
heuristica = grafo.heuristics_k2[0]
prop = grafo.prop_disp
for i in range(0, cantidad):
    print(f"PROBLEMA NUM {i + 1}")
    inicial = grafo.iniciales[i]
    for weight in weights:
        print(f"-------------------W: {weight}-------------------")
        a_star = Astar(inicial, objetivo, op, heuristica, prop, weight, "lmcut")
        inicio = time.process_time()
        sol, exp, tim = a_star.search()
        tiempo = time.process_time() - inicio
        tiempos_astar = [tiempo] * 6
        nodos_astar = [exp] * 6
        valores_g = [a_star.g_final] * 6
        print(f"Tiempo en realizar búsqueda A*: {tiempo}")
        print("nodos expandidos A*: " + str(exp))
        resultado = Resultados(tiempos_astar, nodos_astar)
        if weight == 1.5:
            weight_15.append(resultado)
        elif weight == 2:
            weight_2.append(resultado)
        else:
            weight_4.append(resultado)
    print("\n")

dato = Datos(weight_15, weight_2, weight_4)
file_name = file_name.replace("grafo","dato")
file_name = file_name.replace(".pickle", "")
nombre = file_name + "--a_star.pickle"
file = open(nombre, "wb")
pickle.dump(dato, file)
    
