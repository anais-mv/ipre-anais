from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle
from focal_search import FocalSearch
import numpy as np
from random import randint

file_name = "grafos//grafo_NUEVO_2023-08-27 22.33.24.589415_--can_prop=16--can_op=100--rango=5--max_add=2--min_ap=3.pickle"
# file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"

grafo = cargar_grafo(file_name)
weights = [1.2, 1.5, 2, 4]

weight_15 = []
weight_2 = []
weight_4 = []
weight_extra = []

objetivo = grafo.objetivo
op = grafo.op_disp
heuristica = grafo.heuristics_k4[0]
prop = grafo.prop_disp
can_mse = 1

nombre_h_random = file_name.replace("grafo", "h_random")
h_random = cargar_grafo(nombre_h_random)
archivo = "archivos terminal//terminal fds best RANDOM -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"

heuristica = grafo.heuristics_k4
open_archivo = open(archivo, "w")
open_archivo.close()
for i in range(0, cantidad):
    print(f"PROBLEMA NUM {i + 1}")
    escribir_archivo(archivo, f"PROBLEMA NUM {i + 1}")
    inicial = grafo.iniciales[i]
    for weight in weights:
        print(f"-------------------W: {weight}-------------------")
        escribir_archivo(archivo, f"-------------------W: {weight}-------------------")
        # a_star = Astar(inicial, objetivo, op, h_random, prop, weight, "h*")
        perfect_heuristic = Astar(inicial, objetivo, op, h_random, prop, 1, "h*").h_function
        # h_aristas = Astar(inicial, objetivo, op, grafo.h_aristas, prop, 1, "h*").h_function
        lm_cut = Astar(inicial, objetivo, op, h_random, prop, 1, "lmcut").h_function
        # a_star = Astar(inicial, objetivo, op, grafo.h_aristas, prop, weight, "lmcut")
        # inicio = time.process_time()
        # sol, exp, tim = a_star.search()
        # tiempo = time.process_time() - inicio
        inicio = time.process_time()
        fs = FocalSearch(inicial, perfect_heuristic, lm_cut, heuristica[0], 1000)
        result = fs.heuristic_discrepancy_search(weight, "best")
        tiempo = time.process_time() - inicio
        exp = fs.expansions
        print(f"Tiempo en realizar: {tiempo}")
        print("nodos expandidos: " + str(exp))
        escribir_archivo(archivo, f"Tiempo en realizar: {tiempo}")
        escribir_archivo(archivo, "nodos expandidos: " + str(exp))
        # resultado = Resultados(tiempos_astar, nodos_astar)
        if weight == 1.5:
            weight_15.append([tiempo, exp])
        elif weight == 2:
            weight_2.append([tiempo, exp])
        elif weight == 4:
            weight_4.append([tiempo, exp])
        else:
            weight_extra.append([tiempo, exp])
    print("\n")
    escribir_archivo(archivo, "\n")
# file_name = file_name.replace("grafo","dato")
# file_name = file_name.replace(".pickle", "")
# nombre = file_name + "--a_star - LMCUT.pickle"
# nombre = file_name + "--a_star.pickle"
# file = open(nombre, "wb")
# pickle.dump(dato, file)

weights_totales = [weight_extra, weight_15, weight_2, weight_4]
for i in range(0, 4):
    weight_actual = weights_totales[i]
    tiempos_w = [res[0] for res in weight_actual]
    exp_w = [res[1] for res in weight_actual]
    print(f"w =  {weights[i]}")
    print(f"tiempo promedio: {np.mean(tiempos_w)}")
    print(f"exp promedio:  {np.mean(exp_w)}")
    print("\n")
    escribir_archivo(archivo, f"w =  {weights[i]}")
    escribir_archivo(archivo, f"tiempo promedio: {np.mean(tiempos_w)}")
    escribir_archivo(archivo, f"exp promedio:  {np.mean(exp_w)}")
    escribir_archivo(archivo, "\n")