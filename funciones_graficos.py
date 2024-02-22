import matplotlib.pyplot as plt
import numpy as np

mse = [0, 5, 10, 20, 100, 200]

def obtener_array_string(lista):
    lista = lista.replace("[","").replace("]","").split(",")
    lista = [float(num) for num in lista]
    return np.array(lista)

def obtener_lista_archivo(nombre):
    archivo = open(nombre, "r")
    lista = archivo.readlines()
    archivo.close()
    nueva_lista = []
    for elemento in lista:
        nueva_lista.append(elemento.strip("\n"))
    return nueva_lista

def obtener_lista_grafico(lista_listas, indice):
    final = []
    for elemento in lista_listas:
        final.append(elemento[indice])
    return final

def obtener_datos(lista_archivos):
    mse = [0, 5, 10, 20, 100, 200]
    
    expansiones_a_0 = []
    expansiones_a_5 = []
    expansiones_a_10 = []
    expansiones_a_20 = []
    expansiones_a_100 = []
    expansiones_a_200 = [] 
    
    tiempo_a_0 = []
    tiempo_a_5 = []
    tiempo_a_10 = []
    tiempo_a_20 = []
    tiempo_a_100 = []
    tiempo_a_200 = []

    expansiones_fs_0 = []
    expansiones_fs_5 = []
    expansiones_fs_10 = []
    expansiones_fs_20 = []
    expansiones_fs_100 = []
    expansiones_fs_200 = []

    tiempo_fs_0 = []
    tiempo_fs_5 = []
    tiempo_fs_10 = []
    tiempo_fs_20 = []
    tiempo_fs_100 = []
    tiempo_fs_200 = []

    expansiones_fsd_pos_0 = []
    expansiones_fsd_pos_5 = []
    expansiones_fsd_pos_10 = []
    expansiones_fsd_pos_20 = []
    expansiones_fsd_pos_100 = []
    expansiones_fsd_pos_200 = []

    tiempo_fsd_pos_0 = []
    tiempo_fsd_pos_5 = []
    tiempo_fsd_pos_10 = []
    tiempo_fsd_pos_20 = []
    tiempo_fsd_pos_100 = []
    tiempo_fsd_pos_200 = []
    
    expansiones_fsd_best_0 = []
    expansiones_fsd_best_5 = []
    expansiones_fsd_best_10 = []
    expansiones_fsd_best_20 = []
    expansiones_fsd_best_100 = []
    expansiones_fsd_best_200 = []

    tiempo_fsd_best_0 = []
    tiempo_fsd_best_5 = []
    tiempo_fsd_best_10 = []
    tiempo_fsd_best_20 = []
    tiempo_fsd_best_100 = []
    tiempo_fsd_best_200 = []
    
    for nombre in lista_archivos:
        archivo = obtener_lista_archivo(nombre)
        for linea in archivo:
            if "Nodos Focal:" in linea:
                lista = linea.replace("Nodos Focal: ", "")
                lista = obtener_array_string(lista)
                expansiones_fs_0.append(lista[0])
                expansiones_fs_5.append(lista[1])
                expansiones_fs_10.append(lista[2])
                expansiones_fs_20.append(lista[3])
                expansiones_fs_100.append(lista[4])
                expansiones_fs_200.append(lista[5])
            elif "Nodos Focal Discrepancy Position:" in linea:
                lista = linea.replace("Nodos Focal Discrepancy Position: ", "")
                lista = obtener_array_string(lista)
                expansiones_fsd_pos_0.append(lista[0])
                expansiones_fsd_pos_5.append(lista[1])
                expansiones_fsd_pos_10.append(lista[2])
                expansiones_fsd_pos_20.append(lista[3])
                expansiones_fsd_pos_100.append(lista[4])
                expansiones_fsd_pos_200.append(lista[5])
            elif "Nodos Focal Discrepancy Best:" in linea:
                lista = linea.replace("Nodos Focal Discrepancy Best: ", "")
                lista = obtener_array_string(lista)
                expansiones_fsd_best_0.append(lista[0])
                expansiones_fsd_best_5.append(lista[1])
                expansiones_fsd_best_10.append(lista[2])
                expansiones_fsd_best_20.append(lista[3])
                expansiones_fsd_best_100.append(lista[4])
                expansiones_fsd_best_200.append(lista[5])
            elif "Nodos Astar:" in linea:
                lista = linea.replace("Nodos Astar: ", "")
                lista = obtener_array_string(lista)
                expansiones_a_0.append(lista[0])
                expansiones_a_5.append(lista[1])
                expansiones_a_10.append(lista[2])
                expansiones_a_20.append(lista[3])
                expansiones_a_100.append(lista[4])
                expansiones_a_200.append(lista[5])
            elif "Tiempo Focal:" in linea:
                lista = linea.replace("Tiempo Focal: ", "")
                lista = obtener_array_string(lista)
                tiempo_fs_0.append(lista[0])
                tiempo_fs_5.append(lista[1])
                tiempo_fs_10.append(lista[2])
                tiempo_fs_20.append(lista[3])
                tiempo_fs_100.append(lista[4])
                tiempo_fs_200.append(lista[5])
            elif "Tiempo Focal Discrepancy Position:" in linea:
                lista = linea.replace("Tiempo Focal Discrepancy Position: ", "")
                lista = obtener_array_string(lista)
                tiempo_fsd_pos_0.append(lista[0])
                tiempo_fsd_pos_5.append(lista[1])
                tiempo_fsd_pos_10.append(lista[2])
                tiempo_fsd_pos_20.append(lista[3])
                tiempo_fsd_pos_100.append(lista[4])
                tiempo_fsd_pos_200.append(lista[5])
            elif "Tiempo Focal Discrepancy Best:" in linea:
                lista = linea.replace("Tiempo Focal Discrepancy Best: ", "")
                lista = obtener_array_string(lista)
                tiempo_fsd_best_0.append(lista[0])
                tiempo_fsd_best_5.append(lista[1])
                tiempo_fsd_best_10.append(lista[2])
                tiempo_fsd_best_20.append(lista[3])
                tiempo_fsd_best_100.append(lista[4])
                tiempo_fsd_best_200.append(lista[5])
            elif "Tiempo Astar:" in linea:
                lista = linea.replace("Tiempo Astar: ", "")
                lista = obtener_array_string(lista)
                tiempo_a_0.append(lista[0])
                tiempo_a_5.append(lista[1])
                tiempo_a_10.append(lista[2])
                tiempo_a_20.append(lista[3])
                tiempo_a_100.append(lista[4])
                tiempo_a_200.append(lista[5])
            elif "Valores g:" in linea:
                lista = linea.replace("Valores g: ", "")
                lista = obtener_array_string(lista)
                valor_g = lista[0]
    tiempos_fs = [tiempo_fs_0, tiempo_fs_5, tiempo_fs_10, tiempo_fs_20, tiempo_fs_100, tiempo_fs_200]
    tiempos_fsd_pos = [tiempo_fsd_pos_0, tiempo_fsd_pos_5, tiempo_fsd_pos_10, tiempo_fsd_pos_20, tiempo_fsd_pos_100, tiempo_fsd_pos_200]
    tiempos_fsd_best = [tiempo_fsd_best_0, tiempo_fsd_best_5, tiempo_fsd_best_10, tiempo_fsd_best_20, tiempo_fsd_best_100, tiempo_fsd_best_200]
    tiempos_a = [tiempo_a_0, tiempo_a_5, tiempo_a_10, tiempo_a_20, tiempo_a_100, tiempo_a_200]
    expansiones_fs = [expansiones_fs_0, expansiones_fs_5, expansiones_fs_10, expansiones_fs_20, expansiones_fs_100, expansiones_fs_200]
    expansiones_fsd_pos = [expansiones_fsd_pos_0, expansiones_fsd_pos_5, expansiones_fsd_pos_10, expansiones_fsd_pos_20, expansiones_fsd_pos_100, expansiones_fsd_pos_200]
    expansiones_fsd_best = [expansiones_fsd_best_0, expansiones_fsd_best_5, expansiones_fsd_best_10, expansiones_fsd_best_20, expansiones_fsd_best_100, expansiones_fsd_best_200]
    expansiones_a = [expansiones_a_0, expansiones_a_5, expansiones_a_10, expansiones_a_20, expansiones_a_100, expansiones_a_200]
    return (tiempos_a, tiempos_fs, tiempos_fsd_pos, tiempos_fsd_best, expansiones_a, expansiones_fs, expansiones_fsd_pos, expansiones_fsd_best, valor_g)

def datos_porcentajes(lista_archivos):
    per_fs_0 = []
    per_fs_5 = []
    per_fs_10 = []
    per_fs_20 = []
    per_fs_100 = []
    per_fs_200 = []
    
    per_fds_pos_0 = []
    per_fds_pos_5 = []
    per_fds_pos_10 = []
    per_fds_pos_20 = []
    per_fds_pos_100 = []
    per_fds_pos_200 = []
    
    per_fds_best_0 = []
    per_fds_best_5 = []
    per_fds_best_10 = []
    per_fds_best_20 = []
    per_fds_best_100 = []
    per_fds_best_200 = []
    
    for nombre in lista_archivos:
        archivo = obtener_lista_archivo(nombre)
        for linea in archivo:
            if "Porcentaje Focal:" in linea:
                lista = linea.replace("Porcentaje Focal: ", "")
                lista = obtener_array_string(lista)
                per_fs_0.append(lista[0])
                per_fs_5.append(lista[1])
                per_fs_10.append(lista[2])
                per_fs_20.append(lista[3])
                per_fs_100.append(lista[4])
                per_fs_200.append(lista[5])
            elif "Porcentaje Focal Discrepancy Position:" in linea:
                lista = linea.replace("Porcentaje Focal Discrepancy Position: ", "")
                lista = obtener_array_string(lista)
                per_fds_pos_0.append(lista[0])
                per_fds_pos_5.append(lista[1])
                per_fds_pos_10.append(lista[2])
                per_fds_pos_20.append(lista[3])
                per_fds_pos_100.append(lista[4])
                per_fds_pos_200.append(lista[5])
            elif "Porcentaje Focal Discrepancy Best:" in linea:
                lista = linea.replace("Porcentaje Focal Discrepancy Best: ", "")
                lista = obtener_array_string(lista)
                per_fds_best_0.append(lista[0])
                per_fds_best_5.append(lista[1])
                per_fds_best_10.append(lista[2])
                per_fds_best_20.append(lista[3])
                per_fds_best_100.append(lista[4])
                per_fds_best_200.append(lista[5])
    per_fs = [per_fs_0, per_fs_5, per_fs_10, per_fs_20, per_fs_100, per_fs_200]
    per_fds_pos = [per_fds_pos_0, per_fds_pos_5, per_fds_pos_10, per_fds_pos_20, per_fds_pos_100, per_fds_pos_200]
    per_fds_best = [per_fds_best_0, per_fds_best_5, per_fds_best_10, per_fds_best_20, per_fds_best_100, per_fds_best_200]
    return (per_fs, per_fds_pos, per_fds_best)

def graficar_per(archivo, w, num):
    archivo_ = "datos//" + archivo
    valores_k = [2, 4]
    for k in valores_k:
        archivo = archivo_ + "--k=" + str(k) + "__"
        lista_archivos = [archivo + str(i) + ".txt" for i in range(0, num)]
        per_fs, per_fds_pos, per_fds_best = datos_porcentajes(lista_archivos)
        promedio_fs = [np.mean(per) for per in per_fs]
        promedio_fds_pos = [np.mean(per) for per in per_fds_pos]
        promedio_fds_best = [np.mean(per) for per in per_fds_best]

        # gráfico porcentaje vs mse
        fig,ax = plt.subplots(dpi=144, figsize = [10,4])
        # fig.tight_layout(pad=3)
        ax.plot([1,2,3,4,5,6], promedio_fs, label="FS", c="red")
        ax.plot([1,2,3,4,5,6], promedio_fds_pos, label="FDS pos", c="blue")
        ax.plot([1,2,3,4,5,6], promedio_fds_best, label="FDS best", c="green")
        ax.set_xticks([1,2,3,4,5,6], mse)
        ax.legend(fontsize=8)
        ax.set_xlabel("Heuristic MSE", fontsize=10)
        ax.set_ylabel("Percentages (%)", fontsize=10)
        ax.set_title(f"% vs MSE - W: {w} - k: {k}", fontsize=10)

def graficar(archivo, w, num, log=False, astar=True):
    nombre = archivo
    archivo_ = "datos//" + archivo
    valores_k = [2, 4]
    for k in valores_k:
        archivo = archivo_ + "--k=" + str(k) + "__"
        lista_archivos = [archivo + str(i) + ".txt" for i in range(0, num)]
        tiempos_a, tiempos_fs, tiempos_fsd_pos, tiempos_fsd_best, expansiones_a, expansiones_fs, expansiones_fsd_pos, expansiones_fsd_best, valor_g = obtener_datos(lista_archivos)
        promedio_tiempo_a = [np.mean(tiempo) for tiempo in tiempos_a]
        promedio_tiempo_fs = [np.mean(tiempo) for tiempo in tiempos_fs]
        promedio_tiempo_fds_pos = [np.mean(tiempo) for tiempo in tiempos_fsd_pos]
        promedio_tiempo_fds_best = [np.mean(tiempo) for tiempo in tiempos_fsd_best]
        promedio_exp_a = [np.mean(exp) for exp in expansiones_a]
        promedio_exp_fs = [np.mean(exp) for exp in expansiones_fs]
        promedio_exp_fds_pos = [np.mean(exp) for exp in expansiones_fsd_pos]
        promedio_exp_fds_best = [np.mean(exp) for exp in expansiones_fsd_best]
        valores_g = [valor_g, valor_g, valor_g, valor_g, valor_g, valor_g]

        # gráfico tiempo vs mse
        fig,ax = plt.subplots(dpi=144, figsize = [10,4], ncols=2)
        fig.tight_layout(pad=3)
        if astar:
            ax[0].plot([1,2,3,4,5,6], promedio_tiempo_a, label="A*", c="purple")
        ax[0].plot([1,2,3,4,5,6], promedio_tiempo_fs, label="FS", c="red")
        ax[0].plot([1,2,3,4,5,6], promedio_tiempo_fds_pos, label="FDS pos", c="blue")
        ax[0].plot([1,2,3,4,5,6], promedio_tiempo_fds_best, label="FDS best", c="green")
        ax[0].set_xticks([1,2,3,4,5,6], mse)
        # ax[0].legend(fontsize=8, loc="upper left")
        ax[0].legend(fontsize=8)
        ax[0].set_xlabel("Heuristic MSE", fontsize=10)
        ax[0].set_ylabel("Runtime (s)", fontsize=10)
        ax[0].set_title(f"Mean Time vs MSE - W: {w} - k: {k}", fontsize=10)
        if log:
            plt.yscale("log")

        # gráfico expansiones vs mse
        # fig,ax = plt.subplots(dpi=144, figsize = [6,4])
        if astar:
            ax[1].plot([1,2,3,4,5,6], promedio_exp_a, label="A*", c="purple")
        ax[1].plot([1,2,3,4,5,6], promedio_exp_fs, label="FS", c="red")
        ax[1].plot([1,2,3,4,5,6], promedio_exp_fds_pos, label="FDS pos", c="blue")
        ax[1].plot([1,2,3,4,5,6], promedio_exp_fds_best, label="FDS best", c="green")
        # ax.plot([1,2,3,4,5,6], valores_g, label="g", c="orange", ls="--")
        ax[1].set_xticks([1,2,3,4,5,6], mse)
        # ax[1].legend(fontsize=8, loc="upper left")
        ax[1].legend(fontsize=8)
        ax[1].set_xlabel("Heuristic MSE", fontsize=10)
        ax[1].set_ylabel("Expansions", fontsize=10)
        ax[1].set_title(f"Mean Expansions vs MSE - W: {w} - k: {k}", fontsize=10)
        if log:
            plt.yscale("log")
    graficar_per(nombre, w, num)
    
def graficar_nuevomse(astar, fs_k2, fs_k4, pos_k2, pos_k4, best_k2, best_k4, w, log=False):
    astar = astar.sacar_promedio(w)
    fs_k2_p = fs_k2.sacar_promedio(w)
    fs_k4_p = fs_k4.sacar_promedio(w)
    pos_k2_p = pos_k2.sacar_promedio(w)
    pos_k4_p = pos_k4.sacar_promedio(w)
    best_k2_p = best_k2.sacar_promedio(w)
    best_k4_p = best_k4.sacar_promedio(w)
    
    for i in range(0, 2):
        if i == 0:
            fs, pos, best = fs_k2_p, pos_k2_p, best_k2_p
        else:
            fs, pos, best = fs_k4_p, pos_k4_p, best_k4_p
        # gráfico tiempo vs mse
        fig,ax = plt.subplots(dpi=144, figsize = [10,4], ncols=2)
        fig.tight_layout(pad=3)
        ax[0].plot([1,2,3,4,5,6], astar[0], label="A*", c="purple")
        ax[0].plot([1,2,3,4,5,6], fs[0], label="FS", c="red")
        ax[0].plot([1,2,3,4,5,6], pos[0], label="FDS pos", c="blue")
        ax[0].plot([1,2,3,4,5,6], best[0], label="FDS best", c="green")
        ax[0].set_xticks([1,2,3,4,5,6], mse)
        # ax[0].legend(fontsize=8, loc="upper left")
        ax[0].legend(fontsize=8)
        ax[0].set_xlabel("Heuristic MSE", fontsize=10)
        ax[0].set_ylabel("Runtime (s)", fontsize=10)
        ax[0].set_title(f"Mean Time vs MSE - W: {w} - k: {(i + 1)*2}", fontsize=10)
        if log:
            plt.yscale("log")
        # gráfico expansiones vs mse
        fig.tight_layout(pad=3)
        ax[1].plot([1,2,3,4,5,6], astar[1], label="A*", c="purple")
        ax[1].plot([1,2,3,4,5,6], fs[1], label="FS", c="red")
        ax[1].plot([1,2,3,4,5,6], pos[1], label="FDS pos", c="blue")
        ax[1].plot([1,2,3,4,5,6], best[1], label="FDS best", c="green")
        ax[1].set_xticks([1,2,3,4,5,6], mse)
        # ax[0].legend(fontsize=8, loc="upper left")
        ax[1].legend(fontsize=8)
        ax[1].set_xlabel("Heuristic MSE", fontsize=10)
        ax[1].set_ylabel("Expansions", fontsize=10)
        ax[1].set_title(f"Mean Expansions vs MSE - W: {w} - k: {(i + 1)*2}", fontsize=10)
        if log:
            plt.yscale("log")
    # graficar_per_k(fs_k2, fs_k4, pos_k2, pos_k4, best_k2, best_k4, w, log)

def cargar(archivo):
    file = open(archivo, "rb")
    clase = pickle.load(file)
    file.close()
    return clase
