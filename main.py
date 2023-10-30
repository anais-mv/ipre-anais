import argparse
from operadores import crear_operadores
from grafo import Grafo, cargar_grafo, h_menor
from astar_heuristicas import Heuristica
from astar import Astar
import sys
from datetime import datetime
import time
from focal_search import FocalSearch
from multi_node import MultiNode
import random
from creacion_problemas import correr_fs
from planning_problem import Estado
from aristas import nuevos_operadores, revisar_h_diferentes, nuevos_operadores_alternativo

cantidad = 30

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--can_prop', type=int, default=100,
                        help='cantidad de proposiciones')
    # LA CANTIDAD DE OPERADORES SERÁ DOBLE YA QUE CADA OP TIENE SU INVERSO
    parser.add_argument('--can_op', type=int, default=100,
                        help='cantidad de operadores')
    parser.add_argument('--rango', type=int, default=3,
                        help='rango maximo de cantidad de precondiciones')
    parser.add_argument('--max_add', type=int, default=3,
                        help='cantidad máxima de proposiciones en add por c/operador')
    parser.add_argument('--min_ap', type=int, default=3,
                        help='cantidad mínima de operadores aplicables del estado inicial')
    args = parser.parse_args()
    estadisticas = vars(args)
    op_disp, datos = crear_operadores(args.can_prop, args.can_op, args.rango, args.max_add)
    prop_disp = datos[0]

    inicio = time.process_time()
    grafo = Grafo(prop_disp, args.min_ap, op_disp, estadisticas)
    estados = grafo.estados
    time_crear_grafo = time.process_time() - inicio
    print(f"Tiempo en crear grafo: {time_crear_grafo}")
    print(f"CANTIDAD DE OPERADORES: {len(op_disp)}")
    print(f"CANTIDAD DE ESTADOS: {len(grafo.estados)}")
    print(f"PROMEDIO FACTOR RAMIFICACIÓN: {grafo.promedio_exp}")
    print(f"MÁXIMA RAMIFICACIÓN: {grafo.maximo_exp}")
    print(f"MEDIANA FACTOR RAMIFICACIÓN: {grafo.mediana_exp}")

    inicio = time.process_time()
    # estados_2 = cargar_grafo(file_name)
    # print(f"Tiempo en cargar grafo: {time.process_time() - inicio}")

    # BÚSQUEDA
    estado_objetivo = grafo.obtener_estado_objetivo()
    grafo.objetivo = estado_objetivo
    posibles = []
    for estado in grafo.estados:
        posibles.append(estado.prop)
    
    for e in estados:
        e.goal = estado_objetivo
        e.posibles = posibles

    inicio = time.process_time()
    bus_heuristica = Heuristica(op_disp, grafo.estados, estado_objetivo)
    grafo.perfect_heuristic = bus_heuristica
    print(f"Tiempo en crear heurística: {time.process_time() - inicio}")

    iniciales = []

    for i in range(0, cantidad):
        iniciales.append(grafo.obtener_aleatorio_inicial())

    grafo.iniciales = iniciales
    cmd_args = "".join(sys.argv[1:])
    file_name = f"grafos//grafo_{datetime.now()}_{cmd_args}.pickle"
    file_name = file_name.replace(":", ".")
    dic_h = bus_heuristica.heuristica
    # grafo.guardar_grafo(file_name)

    # weights = [1.5, 2, 4]
    mses = [0, 5, 10, 20, 100, 200]
    valores_k = [2, 4]
    # k = 2 # exponent for k multiplied to c
    for k in valores_k:
        print(f"-------------------k: {k}------------------- \n")
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
        if k == 2:
            grafo.heuristics_k2 = mse_heuristics
        else:
            grafo.heuristics_k4 = mse_heuristics
    
    # calculando porcentaje de coincidencias
    perfect_heuristic_k2 = grafo.heuristics_k2[0]
    perfect_heuristic_k4 = grafo.heuristics_k4[0]
    percentages_k2, percentages_k4 = [], []

    for i in range(0, 6):
        heuristic_k2 = grafo.heuristics_k2[i]
        heuristic_k4 = grafo.heuristics_k4[i]
        total_k2, total_k4, coincidentes_k2, coincidentes_k4 = 0, 0, 0, 0
        for info in heuristic_k2:
            total_k2 += 1
            succ_mse = []
            succ_perfect = []
            estado = Estado(info, op_disp)
            succ = estado.succ()
            for sucesor in succ:
                h_mse = heuristic_k2[sucesor]
                h_perfect = perfect_heuristic_k2[sucesor]
                succ_mse.append((sucesor, h_mse))
                succ_perfect.append((sucesor, h_perfect))
            succ_mse.sort(key=h_menor)
            succ_perfect.sort(key=h_menor)
            if succ_mse[0][0] == succ_perfect[0][0]:
                coincidentes_k2 += 1
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
        percentage_k2 = (coincidentes_k2/total_k2) *100
        percentage_k4 = (coincidentes_k4/total_k4) *100
        percentages_k2.append(percentage_k2)
        percentages_k4.append(percentage_k4)
        print(f"\nporcentaje coincidentes k = 2 mse = {mses[i]}: {percentage_k2}")
        print(f"porcentaje coincidentes k = 4 mse = {mses[i]}: {percentage_k4}")
    print("\n")
    grafo.percentages_k2 = percentages_k2
    grafo.percentages_k4 = percentages_k4

    inicio = time.process_time()
    print("Creando aristas...")
    # op_aristas = nuevos_operadores(grafo, args.can_prop, args.can_op, args.rango, args.max_add)
    op_aristas = nuevos_operadores_alternativo(grafo)
    print(f"Tiempo en crear aristas: {time.process_time() - inicio}")
    
    inicio = time.process_time()
    # print("Creando heurística aristas...")
    grafo.h_aristas = Heuristica(op_aristas, grafo.estados, estado_objetivo).heuristica
    print(f"Tiempo en crear heurística aristas: {time.process_time() - inicio}")

    revisar_h_diferentes(grafo, dic_h, grafo.h_aristas)

    grafo.guardar_grafo(file_name)
