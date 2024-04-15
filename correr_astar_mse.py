from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle
from focal_search import FocalSearch

file_name = "grafos//grafo_NUEVOS_MSE_2023-11-10 12.54.23.991920_--can_prop=22--can_op=450--rango=1--max_add=20--min_ap=2.pickle"
# file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"

grafo = cargar_grafo(file_name)
# weights = [1.5, 2, 4]
weights = [10000]
objetivo = grafo.objetivo
op = grafo.op_disp
prop = grafo.prop_disp
valores_k = [2, 4]
mses = [0, 1, 2, 3, 4, 5]
archivo = "archivos terminal//terminal astar MSE -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"
# archivo = "logs_ejecuciones/exec_fs--" + file_name.replace("../storage/grafo_", "")[:-7] + ".txt"

open_archivo = open(archivo, "w")
open_archivo.close()
for k in valores_k:
    print(f"-------------------k: {k}-------------------")
    escribir_archivo(archivo, f"-------------------k: {k}-------------------")
    weight_15 = []
    weight_2 = []
    weight_4 = []
    if k == 2:
        heuristica = grafo.heuristics_k2
    else:
        heuristica = grafo.heuristics_k4
    for i in range(0, cantidad):
        print(f"PROBLEMA NUM {i + 1} - k: {k}")
        escribir_archivo(archivo, f"PROBLEMA NUM {i + 1} - k: {k}")
        inicial = grafo.iniciales[i]
        for weight in weights:
            print(f"-------------------W: {weight}-------------------")
            escribir_archivo(archivo, f"-------------------W: {weight}-------------------")
            tiempos = []
            nodos = []
            porcentajes = []
            for mse in range(0, len(mses)):
                print("\n" + f"MSE: {mses[mse]}")
                escribir_archivo(archivo, "\n" + f"MSE: {mses[mse]}")
                a_star = Astar(inicial, objetivo, op, heuristica[mse], prop, weight, "h*")
                inicio = time.process_time()
                sol, exp, tim = a_star.search()
                tiempo = time.process_time() - inicio
                print(f"Tiempo en realizar búsqueda A*: {tiempo}")
                escribir_archivo(archivo, f"Tiempo en realizar búsqueda A*: {tiempo}")
                print("nodos expandidos A*: " + str(exp) + "\n")
                escribir_archivo(archivo, "nodos expandidos A*: " + str(exp) + "\n")
                tiempos.append(tiempo)
                nodos.append(exp)
            resultado = Resultados(tiempos, nodos, [])
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
    nombre = file_name + f"--astar MSE--k={k}.pickle"
    file = open(nombre, "wb")
    pickle.dump(dato, file)