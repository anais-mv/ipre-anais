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
    print(f"PROMEDIO EXPANSIONES: {grafo.promedio_exp}")

    cmd_args = "".join(sys.argv[1:])
    file_name = f"grafos//grafo_{datetime.now()}_{cmd_args}.pickle"
    file_name = file_name.replace(":", ".")
    grafo.guardar_grafo(file_name)

    inicio = time.process_time()
    estados_2 = cargar_grafo(file_name)
    # print(f"Tiempo en cargar grafo: {time.process_time() - inicio}")

    # BÚSQUEDA
    estado_objetivo = grafo.obtener_estado_objetivo()
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

    for i in range(0, cantidad):
        print(f"PROBLEMA NUM {i + 1}")
        h_perfect = bus_heuristica.heuristica
        grafo.estado_inicial = grafo.obtener_aleatorio_inicial()
        correr_fs(h_perfect, grafo, grafo.estado_inicial, estado_objetivo, op_disp, prop_disp, file_name, i)
