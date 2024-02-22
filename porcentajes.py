from grafo import cargar_grafo, h_menor
from planning_problem import Estado

file_name = "grafos//grafo_NUEVO_2023-09-08 15.25.57.150078_--can_prop=17--can_op=80--rango=3--max_add=2--min_ap=3 ARISTAS.pickle"
grafo = cargar_grafo(file_name)

perfect_heuristic_k4 = grafo.heuristics_k4[0]
percentages_k2, percentages_k4 = [], []
op_disp = grafo.op_disp
mses = [0, 2.5, 5, 10, 20, 100, 200]


for i in range(0, 7):
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

# grafo.percentages_k2 = percentages_k2
grafo.percentages_k4 = percentages_k4

grafo.guardar_grafo(file_name)