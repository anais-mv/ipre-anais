import argparse
from operadores import crear_operadores
from grafo import Grafo, cargar_grafo
from astar_heuristicas import Heuristica
from astar import Astar
import sys
from datetime import datetime
import time
from focal_search import FocalSearch
print("hola")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--max_prop', type=int, default=100,
                        help='cantidad máxima de proposiciones')
    parser.add_argument('--min_prop', type=int, default=80,
                        help='cantidad mínima de proposiciones')
    parser.add_argument('--max_op', type=int, default=100,
                        help='cantidad máxima de operadores')
    parser.add_argument('--min_op', type=int, default=50,
                        help='cantidad mínima de operadores')
    parser.add_argument('--rango', type=int, default=3,
                        help='rango maximo de cantidad de precondiciones')
    parser.add_argument('--max_add', type=int, default=3,
                        help='cantidad máxima de proposiciones en add por c/operador')
    parser.add_argument('--min_ap', type=int, default=3,
                        help='cantidad mínima de operadores aplicables del estado inicial')
    args = parser.parse_args()
    estadisticas = vars(args)
    op_disp, datos = crear_operadores(args.max_prop, args.min_prop, args.max_op,
                                      args.min_prop, args.rango, args.max_add)
    prop_disp = datos[0]

    inicio = time.process_time()

    grafo = Grafo(prop_disp, args.min_ap, op_disp, estadisticas)
    estados = grafo.estados
    time_crear_grafo = time.process_time() - inicio
    print(f"Tiempo en crear grafo: {time_crear_grafo}")
    print(f"CANTIDAD DE OPERADORES: {len(op_disp)}")
    print(f"CANTIDAD DE ESTADOS: {len(grafo.estados)}")

    cmd_args = "".join(sys.argv[1:])
    file_name = f"grafos//grafo_{datetime.now()}_{cmd_args}.pickle"
    file_name = file_name.replace(":", ".")
    grafo.guardar_grafo(file_name)

    inicio = time.process_time()
    estados_2 = cargar_grafo(file_name)
    print(f"Tiempo en cargar grafo: {time.process_time() - inicio}")

    # BÚSQUEDA
    estado_objetivo = grafo.obtener_estado_objetivo()
    for e in estados:
        e.goal = estado_objetivo
    inicio = time.process_time()
    bus_heuristica = Heuristica(op_disp, grafo.estados, estado_objetivo)
    print(f"Tiempo en crear heurística: {time.process_time() - inicio}")

    # A*
    inicio = time.process_time()
    a_star = Astar(grafo.estado_inicial, estado_objetivo, op_disp, bus_heuristica.heuristica, prop_disp)
    sol, exp, tim = a_star.search()
    print(f"Tiempo en realizar búsqueda A*: {time.process_time() - inicio}")
    print("nodos expandidos: " + str(exp))

    # FOCAL SEARCH
    print("Iniciando FS")
    # fs = FocalSearch(grafo.estado_inicial, bus_heuristica.zero_heuristic, 2)
    fs = FocalSearch(grafo.estado_inicial, a_star.heuristic, 2)
    result = fs.heuristic_search(2)
    print(result)
    print("nodos expandidos focal:", fs.expansions)
    
    # FDS BEST
    print("Iniciando FDS BEST")
    fs = FocalSearch(grafo.estado_inicial, a_star.heuristic, 2)
    result = fs.heuristic_discrepancy_search(2, "best")
    print(result)
    print("nodos expandidos fds best:", fs.expansions)

    # FDS POSITION
    print("Iniciando FDS POSITION")
    fs = FocalSearch(grafo.estado_inicial, a_star.heuristic, 2)
    result = fs.heuristic_discrepancy_search(2, "position")
    print(result)
    print("nodos expandidos fds position:", fs.expansions)
