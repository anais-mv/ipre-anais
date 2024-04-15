from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo, Valores_g
import pickle
from focal_search import FocalSearch

import argparse
parser = argparse.ArgumentParser(description='Run')
parser.add_argument('graph_path', type=str, help='la ubicacion del archivo del grafo')
    
args = parser.parse_args()
#file_name = "grafos//grafo_2023-11-10 12.54.23.991920_--can_prop=22--can_op=450--rango=1--max_add=20--min_ap=2.pickle"
file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"
file_name = f"../storage/{args.graph_path}"

grafo = cargar_grafo(file_name)
weights = [1.2, 1.5, 2, 4]
objetivo = grafo.objetivo
op = grafo.op_disp
prop = grafo.prop_disp
# valores_k = [2, 4]
valores_k = [4]
mses = [0, 2.5, 5, 10, 20, 100, 200]
# mses = [0, 0.25, 0.5, 1, 1.75, 2.5]
archivo = "archivos terminal//terminal fds best H ARISTAS -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"
archivo = "logs_ejecuciones/exec_fdsbest--" + file_name.replace("../storage/", "")[:-7] + ".txt"

g_problemas = []
for weight in weights:
   valor_g = Valores_g(weight) 
   g_problemas.append(valor_g)
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
            for valor in g_problemas:
                if valor.weight == weight:
                    valor_g = valor
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
                result = fs.heuristic_discrepancy_search(weight, "best")
                tiempo = time.process_time() - inicio
                tiempos.append(tiempo)
                nodos.append(fs.expansions)
                porcentajes.append(fs.percentage)
                valor_g.all_mse[mse].append(result.g)
                print(f"Valor g: {result.g}")
                escribir_archivo(archivo, f"Valor g: {result.g}")
                print(f"nodos expandidos focal discrepancy best: {fs.expansions}")
                escribir_archivo(archivo, f"nodos expandidos focal discrepancy best: {fs.expansions}")
                print(f"tiempo focal discrepancy best: {tiempo}")
                escribir_archivo(archivo, f"tiempo focal discrepancy best: {tiempo}")
            resultado = Resultados(tiempos, nodos, porcentajes)
            if weight == 1.5:
                weight_15.append(resultado)
            elif weight == 2:
                weight_2.append(resultado)
            elif weight == 4:
                weight_4.append(resultado)
            else:
                weight_extra.append(resultado)
        print("\n")

    if len(weight_extra) > 0:
        dato = Datos(weight_15, weight_2, weight_4, weight_extra)
    else:
        dato = Datos(weight_15, weight_2, weight_4)
    print(dato.datos_w15)
    file_name = file_name.replace("grafo","dato")
    file_name = file_name.replace(".pickle", "")
    nombre = file_name + f"--fds_best--k={k} H ARISTAS.pickle"
    file = open(nombre, "wb")
    pickle.dump(dato, file)
    nombre_g = file_name + f"--fds_best--k={k} LISTA G H ARISTAS.pickle"
    file_g = open(nombre_g, "wb")
    pickle.dump(g_problemas, file_g)
