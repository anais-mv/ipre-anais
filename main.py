import argparse
from operadores import crear_operadores
from grafo import Grafo, cargar_grafo
from astar_heuristicas import Heuristica
from astar import Astar
import sys
from datetime import datetime
import time
from focal_search import FocalSearch
from multi_node import MultiNode
import random
from creacion_problemas import correr_fs

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
        if k == 2:
            grafo.heuristics_k2 = mse_heuristics
        else:
            grafo.heuristics_k4 = mse_heuristics

    grafo.guardar_grafo(file_name)
            # mse_ = mse_/(len(dic_h))
    # for i in range(0, cantidad):
    #     print(f"PROBLEMA NUM {i + 1}")
    #     h_perfect = bus_heuristica.heuristica
    #     grafo.estado_inicial = grafo.obtener_aleatorio_inicial()
    #     correr_fs(h_perfect, grafo, grafo.estado_inicial, estado_objetivo, op_disp, prop_disp, file_name, i, grafo.promedio_exp)
