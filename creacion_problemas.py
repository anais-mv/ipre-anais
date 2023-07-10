from astar import Astar
from focal_search import FocalSearch
import time
import random


def correr_fs(heuristica, grafo, inicial, objetivo, op, prop, file_name, iteracion):
    posibles = []
    for estado in grafo.estados:
        posibles.append(estado.prop)
    weight = 1000
    mses = [0, 5, 10, 20, 100, 200] # AGREGAR 0
    k = 4 # exponent for k multiplied to c
    dic_h = heuristica
    sum_h = sum([dic_h[estado]**(2*k) for estado in dic_h])/len(dic_h)
    valores_g = []
    mse_heuristics = []
    tiempos_astar = []
    nodos_astar = []
    tiempos_focal = []
    nodos_focal = []
    tiempos_focal_discrepancy = []
    nodos_focal_discrepancy = []
    inicio = time.process_time()
    for mse in mses:
        mse_ = 0
        new_heuristic = dict()
        c = (mse/sum_h)**(1/2)
        for state in dic_h:
            depth = dic_h[state]
            h_nn = depth + c * random.gauss(0, 1) * (depth**k)
            mse_ += (h_nn - depth)**2
            new_heuristic[state] = h_nn
        mse_heuristics.append(new_heuristic)
        mse_ = mse_/(len(dic_h))
        print(f"c:= {c} ; k:= {k}")
        print("Error cuadrático medio")
        print("\t Real    :", mse_)
        print("\t Esperado:", mse)
        print("A* mse:", mse_)
        inicio = time.process_time()
        a_star = Astar(inicial, objetivo, op, new_heuristic, prop, posibles, "h*")
        lm_cut = Astar(inicial, objetivo, op, new_heuristic, prop, posibles, "lmcut").h_function
        sol, exp, tim = a_star.search()
        tiempo_astar = time.process_time() - inicio
        tiempos_astar.append(tiempo_astar)
        nodos_astar.append(exp)
        valores_g.append(a_star.g_final)
        print(f"Tiempo en realizar búsqueda A*: {tiempo_astar}")
        print("nodos expandidos: " + str(exp))
        inicio = time.process_time()
        fs = FocalSearch(grafo.estado_inicial, a_star.perfect_heuristic, lm_cut, 1000)
        result = fs.heuristic_search(weight)
        tiempo_focal = time.process_time() - inicio
        tiempos_focal.append(tiempo_focal)
        nodos_focal.append(fs.expansions)
        print("nodos expandidos focal:", fs.expansions)
        inicio = time.process_time()
        fs = FocalSearch(grafo.estado_inicial, a_star.perfect_heuristic, lm_cut, 1000)
        result = fs.heuristic_discrepancy_search(weight, "position")
        tiempo_focal_discrepancy = time.process_time() - inicio
        tiempos_focal_discrepancy.append(tiempo_focal_discrepancy)
        nodos_focal_discrepancy.append(fs.expansions)
        print("nodos expandidos focal discrepancy:", fs.expansions)
        print("\n")

    grafo.mse_heuristics = mse_heuristics
    grafo.guardar_grafo(file_name)
    file_name_datos = file_name.replace("grafo", "dato")
    file_name_datos = file_name_datos.replace(".pickle", "")
    file_name_datos += "__" + str(iteracion) + ".txt"
    archivo = open(file_name_datos, "w")
    archivo.write("Valores g: " + str(valores_g) + "\n")
    archivo.write("Tiempo Astar: " + str(tiempos_astar) + "\n")
    archivo.write("Nodos Astar: " + str(nodos_astar) + "\n")
    archivo.write("Tiempo Focal: " + str(tiempos_focal) + "\n")
    archivo.write("Nodos Focal: " + str(nodos_focal) + "\n")
    archivo.write("Tiempo Focal Discrepancy: " + str(tiempos_focal_discrepancy) + "\n")
    archivo.write("Nodos Focal Discrepancy: " + str(nodos_focal_discrepancy) + "\n")
    archivo.close()

