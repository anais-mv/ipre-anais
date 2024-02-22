from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle
from focal_search import FocalSearch

file_name = "grafos//grafo_NUEVO_2023-08-27 22.33.24.589415_--can_prop=16--can_op=100--rango=5--max_add=2--min_ap=3.pickle"
# file_name = "../storage/grafo_2023_10_29_22_59_49_274734_can_prop=20_can_op=500_rango=5.pickle"

grafo = cargar_grafo(file_name)
weights = [1.2, 1.5, 2, 4]
# weights = [1.2]
objetivo = grafo.objetivo
op = grafo.op_disp
prop = grafo.prop_disp
# valores_k = [2, 4]
valores_k = [4]
mses = [0, 2.5, 5, 10, 20, 100, 200]
# mses = [0, 0.25, 0.5, 1, 1.75, 2.5]
archivo = "archivos terminal//terminal fds pos LISTA G -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"
# archivo = "logs_ejecuciones/exec_fdspos--" + file_name.replace("../storage/grafo_", "")[:-7] + ".txt"

g_12, g_15, g_2, g_4 = [], [], [], []
open_archivo = open(archivo, "w")
open_archivo.close()
for k in valores_k:
    print(f"-------------------k: {k}-------------------")
    escribir_archivo(archivo, f"-------------------k: {k}-------------------")
    weight_15 = []
    weight_2 = []
    weight_4 = []
    weight_extra = []
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
                lm_cut = Astar(inicial, objetivo, op, heuristica[mse], prop, 1, "lmcut").h_function
                # h_aristas = Astar(inicial, objetivo, op, grafo.h_aristas, prop, 1, "h*").h_function
                inicio = time.process_time()
                fs = FocalSearch(inicial, perfect_heuristic, lm_cut, heuristica[0], 1000)
                result = fs.heuristic_discrepancy_search(weight, "position")
                tiempo = time.process_time() - inicio
                tiempos.append(tiempo)
                nodos.append(fs.expansions)
                porcentajes.append(fs.percentage)
                print(f"Valor g: {result.g}")
                escribir_archivo(archivo, f"Valor g: {result.g}")
                print(f"nodos expandidos focal discrepancy pos: {fs.expansions}")
                escribir_archivo(archivo, f"nodos expandidos focal discrepancy pos: {fs.expansions}")
                print(f"tiempo focal discrepancy pos: {tiempo}")
                escribir_archivo(archivo, f"tiempo focal discrepancy pos: {tiempo}")
            resultado = Resultados(tiempos, nodos, porcentajes)
            if weight == 1.5:
                weight_15.append(resultado)
                g_15.append(result.g)
            elif weight == 2:
                weight_2.append(resultado)
                g_2.append(result.g)
            elif weight == 4:
                weight_4.append(resultado)
                g_4.append(result.g)
            else:
                weight_extra.append(resultado)
                g_12.append(result.g)
                print("len", len(weight_extra))
        print("\n")

    if len(weight_extra) > 0:
        dato = Datos(weight_15, weight_2, weight_4, weight_extra)
    else:
        dato = Datos(weight_15, weight_2, weight_4)
    print(dato.datos_w15)
    file_name = file_name.replace("grafo","dato")
    file_name = file_name.replace(".pickle", "")
    nombre = file_name + f"--fds_pos--k={k} LMCUT NUEVO.pickle"
    file = open(nombre, "wb")
    pickle.dump(dato, file)
    nombre_g = file_name + f"--fds_pos--k={k} LISTA G.pickle"
    file_g = open(nombre_g, "wb")
    g_problemas = [g_12, g_15, g_2, g_4]
    pickle.dump(g_problemas, file_g)
