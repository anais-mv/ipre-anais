import matplotlib.pyplot as plt
import numpy as np
import pickle

def cargar(archivo):
    file = open(archivo, "rb")
    clase = pickle.load(file)
    file.close()
    return clase

def lista_de_lista(n):
    lista = []
    for i in range(0, n):
        lista.append([])
    return lista

def eliminar_vacias(lista):
    final = []
    for elemento in lista:
        if len(elemento) > 0:
            final.append(elemento)
    return final

def graficar_mse(i, grafo, mse_values):
    mse_k2 = lista_de_lista(100)
    mse_k4 = lista_de_lista(100)
    for estado in grafo.heuristics_k2[0]:
        h_perfect = grafo.heuristics_k2[0][estado]
        indice = int(h_perfect)
        # k = 2
        h_nn = grafo.heuristics_k2[i][estado]
        err_k2 = (h_nn - h_perfect)**2
        mse_k2[indice].append(err_k2)
        # k = 4
        h_nn = grafo.heuristics_k4[i][estado]
        err_k4 = (h_nn - h_perfect)**2
        mse_k4[indice].append(err_k4)
    mse_k2 = eliminar_vacias(mse_k2)
    mse_k4 = eliminar_vacias(mse_k4)
    mean_mse_k2 = [np.mean(mse) for mse in mse_k2]
    mean_mse_k4 = [np.mean(mse) for mse in mse_k4]
    h_perfect = [i for i in range(0, len(mean_mse_k2))]
    
    fig, ax = plt.subplots(dpi=144, figsize=[10, 4])
    ax.plot(h_perfect, mean_mse_k2, label="k = 2")
    ax.plot(h_perfect, mean_mse_k4, label="k = 4")
    ax.set_title(f"MSE = {mse_values[i]}", size=20)
    ax.set_xlabel(r"$h*$", size=20)
    ax.set_ylabel(r"$\overline{(h_{nn} - h*)^2}$", size=20)
    ax.legend(fontsize=15)