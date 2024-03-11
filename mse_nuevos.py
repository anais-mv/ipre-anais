from grafo import cargar_grafo, h_menor
from clase_datos import escribir_archivo
from planning_problem import Estado
import random
import time
from aristas import nuevos_operadores, revisar_h_diferentes, nuevos_operadores_alternativo
from astar_heuristicas import Heuristica

def can_prop(grafo):
    mayores = []
    for estado in grafo.estados:
        lista_props = list(estado.prop)
        props = [int(num) for num in lista_props]
        mayor_estado = max(props)
        mayores.append(mayor_estado)
    return max(mayores)

print("OLA")
file_name = "grafos//grafo_2023-11-10 12.54.23.991920_--can_prop=22--can_op=450--rango=1--max_add=20--min_ap=2.pickle"
grafo = cargar_grafo(file_name)
final_archivo = file_name.replace("pickle", "txt").replace("grafos//","")
archivo = f"archivos terminal// main {final_archivo}"
open_archivo = open(archivo, "w")
open_archivo.close()
valores_k = [2, 4]
# mses = [0, 1, 2, 3, 4, 5]
mses = [0, 2.5, 5, 10, 20, 100, 200]
# mses = [0, 0.25, 0.5, 1, 1.75, 2.5]
dic_h = grafo.perfect_heuristic.heuristica
cantidad = 30
print("CAN:", len(dic_h))

estado_objetivo = list(grafo.estados)[0].goal
print(dic_h[estado_objetivo.prop])

iniciales = []
for i in range(0, cantidad):
        iniciales.append(grafo.obtener_aleatorio_inicial())
grafo.iniciales = iniciales

# valores_k = [2, 4]
valores_k = [4]
# k = 2 # exponent for k multiplied to c
for k in valores_k:
    print(f"-------------------k: {k}------------------- \n")
    escribir_archivo(archivo, f"-------------------k: {k}------------------- \n")
    sum_h = sum([dic_h[estado]**(2*k) for estado in dic_h])/len(dic_h)
    mse_heuristics = []
    for mse in mses:
        mse_ = 0
        new_heuristic = dict()
        c = (mse/sum_h)**(1/2)
        for state in dic_h:
            depth = dic_h[state]
            if depth == 0:
                h_nn = 0
            else:
                error = c * random.gauss(0, 1) * (depth**k) 
                h_nn = depth + error # * random.choice([-1, 1])
                if h_nn < 0:
                    # h_nn = 1
                    h_nn = depth - error
            mse_ += (h_nn - depth)**2
            new_heuristic[state] = h_nn
        mse_heuristics.append(new_heuristic)
        print("\nMSE Real:", mse_/len(dic_h))
        print("MSE Esperado:", mse)
        escribir_archivo(archivo, f"\nMSE Real: {mse_/len(dic_h)}")
        escribir_archivo(archivo, f"MSE Esperado: {mse}")
    if k == 2:
        grafo.heuristics_k2 = mse_heuristics
    else:
        grafo.heuristics_k4 = mse_heuristics

# calculando porcentaje de coincidencias
# perfect_heuristic_k2 = grafo.heuristics_k2[0]
perfect_heuristic_k4 = grafo.heuristics_k4[0]
percentages_k2, percentages_k4 = [], []
op_disp = grafo.op_disp

for i in range(0, len(mses)):
    heuristic_k4 = grafo.heuristics_k4[i]
    total_k2, total_k4, coincidentes_k2, coincidentes_k4 = 0, 0, 0, 0
    for info in heuristic_k4:
        total_k4 += 1
        succ_mse = []
        succ_perfect = []
        estado = Estado(info, op_disp)
        succ = estado.succ()
        for sucesor in succ:
            h_mse = heuristic_k4[sucesor]
            h_perfect = perfect_heuristic_k4[sucesor]
            succ_mse.append((sucesor, h_mse))
            succ_perfect.append((sucesor, h_perfect))
        succ_mse.sort(key=h_menor)
        succ_perfect.sort(key=h_menor)
        if succ_mse[0][0] == succ_perfect[0][0]:
            coincidentes_k4 += 1
    # percentage_k2 = (coincidentes_k2/total_k2) *100
    percentage_k4 = (coincidentes_k4/total_k4) *100
    # percentages_k2.append(percentage_k2)
    percentages_k4.append(percentage_k4)
    # print(f"\nporcentaje coincidentes k = 2 mse = {mses[i]}: {percentage_k2}")
    print(f"porcentaje coincidentes k = 4 mse = {mses[i]}: {percentage_k4}")
    # escribir_archivo(archivo, f"\nporcentaje coincidentes k = 2 mse = {mses[i]}: {percentage_k2}")
    escribir_archivo(archivo, f"porcentaje coincidentes k = 4 mse = {mses[i]}: {percentage_k4}")
print("\n")
escribir_archivo(archivo, "\n")
# grafo.percentages_k2 = percentages_k2
grafo.percentages_k4 = percentages_k4

grafo.guardar_grafo(file_name)
grafo.objetivo = estado_objetivo

inicio = time.process_time()
print("Creando aristas...")
# op_aristas = nuevos_operadores(grafo, args.can_prop, args.can_op, args.rango, args.max_add)
# op_aristas = nuevos_operadores_alternativo(grafo, archivo)
op_aristas = nuevos_operadores(grafo, can_prop(grafo), 3000, 3, 2)
print(f"Tiempo en crear aristas: {time.process_time() - inicio}")
escribir_archivo(archivo, f"Tiempo en crear aristas: {time.process_time() - inicio}")
    
inicio = time.process_time()
# print("Creando heurística aristas...")
grafo.h_aristas = Heuristica(op_aristas, grafo.estados, estado_objetivo).heuristica
print(f"Tiempo en crear heurística aristas: {time.process_time() - inicio}")
escribir_archivo(archivo, f"Tiempo en crear heurística aristas: {time.process_time() - inicio}")

revisar_h_diferentes(grafo, dic_h, grafo.h_aristas, archivo)

grafo.guardar_grafo(file_name)