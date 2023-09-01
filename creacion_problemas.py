from astar import Astar
from focal_search import FocalSearch
import time
import random


def correr_fs(heuristica, grafo, inicial, objetivo, op, prop, file_name, iteracion, prom):
    weights = [1.5, 2, 4]
    mses = [0, 5, 10, 20, 100, 200]
    valores_k = [2, 4]
    # k = 2 # exponent for k multiplied to c
    for k in valores_k:
        print(f"-------------------k: {k}------------------- \n")
        dic_h = heuristica
        sum_h = sum([dic_h[estado]**(2*k) for estado in dic_h])/len(dic_h)
        mse_heuristics = []
        for weight in weights:
            tiempos_focal = []
            tiempos_focal_discrepancy_pos = []
            tiempos_focal_discrepancy_best = []
            nodos_focal = []
            nodos_focal_discrepancy_pos = []
            nodos_focal_discrepancy_best = []
            g_focal = []
            g_focal_discrepancy_pos = []
            g_focal_discrepancy_best = []
            per_fs = []
            per_fdpos = []
            per_fdbest = []
            # a_star_ph = Astar(inicial, objetivo, op, dic_h, prop, weight, "h*").perfect_heuristic
            print(f"-------------------W: {weight}-------------------")
            a_star = Astar(inicial, objetivo, op, heuristica, prop, weight, "lmcut")
            inicio = time.process_time()
            sol, exp, tim = a_star.search()
            tiempo_astar = time.process_time() - inicio
            tiempos_astar = [tiempo_astar] * 6
            nodos_astar = [exp] * 6
            valores_g = [a_star.g_final] * 6
            print(f"Tiempo en realizar búsqueda A*: {tiempo_astar}")
            print("nodos expandidos A*: " + str(exp))
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
                mse_ = mse_/(len(dic_h))
                print(f"c:= {c} ; k:= {k}")
                print("Error cuadrático medio")
                print("\t Real    :", mse_)
                print("\t Esperado:", mse)
                # print("A* mse:", mse_)
                a_star = Astar(inicial, objetivo, op, new_heuristic, prop, 1, "h*")
                sol, exp, tim = a_star.search()
                print("NODOS EXPANDIDOS A* H ARRUINADA:", exp)
                lm_cut = Astar(inicial, objetivo, op, new_heuristic, prop, 1, "lmcut").h_function
                # lm_cut = Astar(inicial, objetivo, op, new_heuristic, prop, 1, "zero").h_function # H ZERO
                inicio = time.process_time()
                fs = FocalSearch(grafo.estado_inicial, a_star.perfect_heuristic, lm_cut, dic_h, 1000)
                result = fs.heuristic_search(weight)
                g_focal.append(result.g)
                tiempo_focal = time.process_time() - inicio
                tiempos_focal.append(tiempo_focal)
                nodos_focal.append(fs.expansions)
                per_fs_d = round(fs.percentage*100, 4)
                per_fs.append(per_fs_d)
                print("nodos expandidos focal:", fs.expansions, "- g:", result.g, "-", per_fs_d, "%")
                inicio = time.process_time()
                fs = FocalSearch(grafo.estado_inicial, a_star.perfect_heuristic, lm_cut, dic_h, 1000)
                result = fs.heuristic_discrepancy_search(weight, "position")
                g_focal_discrepancy_pos.append(result.g)
                tiempo_focal_discrepancy = time.process_time() - inicio
                tiempos_focal_discrepancy_pos.append(tiempo_focal_discrepancy)
                nodos_focal_discrepancy_pos.append(fs.expansions)
                per_fdpos_d = round(fs.percentage*100, 4)
                per_fdpos.append(per_fdpos_d)
                print("nodos expandidos focal discrepancy position:", fs.expansions, "- g:", result.g, "-", per_fdpos_d, "%")
                inicio = time.process_time()
                fs = FocalSearch(grafo.estado_inicial, a_star.perfect_heuristic, lm_cut, dic_h, 1000)
                result = fs.heuristic_discrepancy_search(weight, "best")
                g_focal_discrepancy_best.append(result.g)
                tiempo_focal_discrepancy = time.process_time() - inicio
                tiempos_focal_discrepancy_best.append(tiempo_focal_discrepancy)
                nodos_focal_discrepancy_best.append(fs.expansions)
                per_fdbest_d = round(fs.percentage*100, 4)
                per_fdbest.append(per_fdbest_d)
                print("nodos expandidos focal discrepancy best:", fs.expansions, "- g:", result.g, "-", per_fdbest_d, "%")
                print("\n")

            grafo.mse_heuristics = mse_heuristics
            grafo.guardar_grafo(file_name)
            file_name_datos = file_name.replace("grafo", "dato")
            file_name_datos = file_name_datos.replace(".pickle", "")
            file_name_datos += "--weight=" + str(weight) + "--k=" + str(k)
            file_name_datos += "__" + str(iteracion) + ".txt"
            archivo = open(file_name_datos, "w")
            archivo.write("Valores g: " + str(valores_g) + "\n")
            archivo.write("Tiempo Astar: " + str(tiempos_astar) + "\n")
            archivo.write("Nodos Astar: " + str(nodos_astar) + "\n")
            archivo.write("Tiempo Focal: " + str(tiempos_focal) + "\n")
            archivo.write("Nodos Focal: " + str(nodos_focal) + "\n")
            archivo.write(f"G Focal: {g_focal}" + "\n")
            archivo.write(f"Porcentaje Focal: {per_fs}" + "\n")
            archivo.write("Tiempo Focal Discrepancy Position: " + str(tiempos_focal_discrepancy_pos) + "\n")
            archivo.write("Nodos Focal Discrepancy Position: " + str(nodos_focal_discrepancy_pos) + "\n")
            archivo.write(f"G Focal Discrepancy Position: {g_focal_discrepancy_pos}" + "\n")
            archivo.write(f"Porcentaje Focal Discrepancy Position: {per_fdpos}" + "\n")
            archivo.write("Tiempo Focal Discrepancy Best: " + str(tiempos_focal_discrepancy_best) + "\n")
            archivo.write("Nodos Focal Discrepancy Best: " + str(nodos_focal_discrepancy_best) + "\n")
            archivo.write(f"G Focal Discrepancy Best: {g_focal_discrepancy_best}" + "\n")
            archivo.write(f"Porcentaje Focal Discrepancy Best: {per_fdbest}" + "\n")
            archivo.write("Factor de expansión promedio: " + str(prom))
            archivo.close()

