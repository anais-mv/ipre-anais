from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle
from SortedSet.sorted_set import SortedSet

file_name = "grafos//grafo_NUEVO_2023-08-27 22.33.24.589415_--can_prop=16--can_op=100--rango=5--max_add=2--min_ap=3.pickle"
# file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"

grafo = cargar_grafo(file_name)
# weights = [1.2, 1.5, 2, 4]
# weights = [1.2]
weights = [1]
weight_15 = []
weight_2 = []
weight_4 = []
weight_extra = []
objetivo = grafo.objetivo
print(objetivo)
op = SortedSet(grafo.op_disp)
heuristica = grafo.heuristics_k4[0]
prop = grafo.prop_disp
can_mse = 7
archivo = "archivos terminal//terminal astar LMCUT NUEVO -- " + file_name.replace("grafos//grafo_", "")[:-7] + ".txt"
# archivo = "logs_ejecuciones/exec_astar--" + file_name.replace("../storage/grafo_", "")[:-7] + ".txt"

g_problemas = []
open_archivo = open(archivo, "w")
open_archivo.close()
for i in range(0, cantidad):
    print(f"PROBLEMA NUM {i + 1}")
    escribir_archivo(archivo, f"PROBLEMA NUM {i + 1}")
    inicial = grafo.iniciales[i]
    for weight in weights:
        print(f"-------------------W: {weight}-------------------")
        escribir_archivo(archivo, f"-------------------W: {weight}-------------------")
        # a_star = Astar(inicial, objetivo, op, heuristica, prop, weight, "h*")
        a_star = Astar(inicial, objetivo, op, grafo.h_aristas, prop, weight, "h*")
        # a_star = Astar(inicial, objetivo, op, heuristica, prop, weight, "lmcut")
        inicio = time.process_time()
        sol, exp, tim = a_star.search()
        tiempo = time.process_time() - inicio
        tiempos_astar = [tiempo] * can_mse
        nodos_astar = [exp] * can_mse
        valores_g = [a_star.g_final] * can_mse
        g_problemas.append(a_star.g_final)
        print(f"Valor g: {a_star.g_final}")
        escribir_archivo(archivo, f"Valor g: {a_star.g_final}")
        print(f"Tiempo en realizar búsqueda A*: {tiempo}")
        escribir_archivo(archivo, f"Tiempo en realizar búsqueda A*: {tiempo}")
        print("nodos expandidos A*: " + str(exp))
        escribir_archivo(archivo, "nodos expandidos A*: " + str(exp))
        resultado = Resultados(tiempos_astar, nodos_astar)
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
file_name = file_name.replace("grafo","dato")
file_name = file_name.replace(".pickle", "")
nombre = file_name + "--a_star - LMCUT NUEVO.pickle"
# nombre = file_name + "--a_star.pickle"
# nombre = file_name + "--a_star - LISTA G.pickle"
file = open(nombre, "wb")
# pickle.dump(dato, file)
pickle.dump(dato, file)
    
