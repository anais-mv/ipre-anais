from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle
from focal_search import FocalSearch

# file_name = "grafos//grafo_2023-10-29 22.24.59.055363_--can_prop=10--can_op=450--rango=5--max_add=3--min_ap=10.pickle"
file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"

grafo = cargar_grafo(file_name)
weights = [1.5, 2, 4]
objetivo = grafo.objetivo
op = grafo.op_disp
prop = grafo.prop_disp
valores_k = [2, 4]
mses = [0, 5, 10, 20, 100, 200]
# archivo = "archivos terminal//terminal fds random -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"
archivo = "logs_ejecuciones/exec_fdsrandom--" + file_name.replace("../storage/grafo_", "")[:-7] + ".txt"
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
                perfect_heuristic = Astar(inicial, objetivo, op, heuristica[mse], prop, 1, "h*").h_function
                # lm_cut = Astar(inicial, objetivo, op, heuristica[mse], prop, 1, "lmcut").h_function
                h_aristas = Astar(inicial, objetivo, op, grafo.h_aristas, prop, 1, "h*").h_function
                inicio = time.process_time()
                fs = FocalSearch(inicial, perfect_heuristic, h_aristas, heuristica[0], 1000)
                result = fs.heuristic_discrepancy_search_random(weight, "best")
                tiempo = time.process_time() - inicio
                tiempos.append(tiempo)
                nodos.append(fs.expansions)
                porcentajes.append(fs.percentage)
                print(f"nodos expandidos focal discrepancy random: {fs.expansions}")
                escribir_archivo(archivo, f"nodos expandidos focal discrepancy random: {fs.expansions}")
                print(f"tiempo focal discrepancy random: {tiempo}")
                escribir_archivo(archivo, f"tiempo focal discrepancy random: {tiempo}")
            resultado = Resultados(tiempos, nodos, porcentajes)
            if weight == 1.5:
                weight_15.append(resultado)
            elif weight == 2:
                weight_2.append(resultado)
            else:
                weight_4.append(resultado)
        print("\n")

    dato = Datos(weight_15, weight_2, weight_4)
    print(dato.datos_w15)
    file_name = file_name.replace("grafo","dato")
    file_name = file_name.replace(".pickle", "")
    nombre = file_name + f"--fds_random--k={k}.pickle"
    file = open(nombre, "wb")
    pickle.dump(dato, file)