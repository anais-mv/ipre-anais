from grafo import cargar_grafo, h_menor
from planning_problem import Estado
file_name = "grafos//grafo_2023-10-29 22.59.49.274734_--can_prop=20--can_op=500--rango=5--max_add=3--min_ap=10.pickle"
grafo = cargar_grafo(file_name)
op_disp = grafo.op_disp
perfect_heuristic_k2 = grafo.heuristics_k2[0]
perfect_heuristic_k4 = perfect_heuristic_k2
heuristic_k2 = grafo.mse_provisorio_k2[1]
heuristic_k4 = grafo.mse_provisorio_k4[1]
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
print(f"\nporcentaje coincidentes k = 2 mse = 2.5: {percentage_k2}")
print(f"porcentaje coincidentes k = 4 mse = 2.5: {percentage_k4}")