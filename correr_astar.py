from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle

# file_name = "grafos//grafo_2023-10-14 12.48.22.125997_--can_prop=20--can_op=1500--rango=5--max_add=2--min_ap=10.pickle"
file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"

grafo = cargar_grafo(file_name)
weights = [1.5, 2, 4]
weight_15 = []
weight_2 = []
weight_4 = []
objetivo = grafo.objetivo
op = grafo.op_disp
heuristica = grafo.heuristics_k2[0]
prop = grafo.prop_disp
# archivo = "archivos terminal//terminal astar -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"
archivo = "logs_ejecuciones/exec_astar--" + file_name.replace("../storage/grafo_", "")[:-7] + ".txt"

open_archivo = open(archivo, "w")
open_archivo.close()
for i in range(0, cantidad):
    print(f"PROBLEMA NUM {i + 1}")
    escribir_archivo(archivo, f"PROBLEMA NUM {i + 1}")
    inicial = grafo.iniciales[i]
    for weight in weights:
        print(f"-------------------W: {weight}-------------------")
        escribir_archivo(archivo, f"-------------------W: {weight}-------------------")
        a_star = Astar(inicial, objetivo, op, heuristica, prop, weight, "ph_2")
        inicio = time.process_time()
        sol, exp, tim = a_star.search()
        tiempo = time.process_time() - inicio
        tiempos_astar = [tiempo] * 6
        nodos_astar = [exp] * 6
        valores_g = [a_star.g_final] * 6
        print(f"Tiempo en realizar búsqueda A*: {tiempo}")
        escribir_archivo(archivo, f"Tiempo en realizar búsqueda A*: {tiempo}")
        print("nodos expandidos A*: " + str(exp))
        escribir_archivo(archivo, "nodos expandidos A*: " + str(exp))
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
    
