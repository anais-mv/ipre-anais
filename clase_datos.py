import numpy as np

class Resultados:
    def __init__(self, tiempos, nodos, per=None):
        self.tiempos = tiempos
        self.nodos = nodos
        self.per = per

    def __str__(self):
        str_tiempo = "Tiempos: " + str(self.tiempos)
        str_nodos = "Nodos: " + str(self.nodos)
        return str_tiempo + "\n" + str_nodos

class Datos:
    def __init__(self, w15, w2, w4, w_extra=None):
        self.datos_w15 = w15
        self.datos_w2 = w2
        self.datos_w4 = w4
        self.datos_wextra = w_extra

    def sacar_promedio(self, peso):
        if peso == 1.5:
            datos = self.datos_w15
        elif peso == 2:
            datos = self.datos_w2
        elif peso == 4:
            datos = self.datos_w4
        else:
            datos = self.datos_wextra
        tiempo_0, tiempo_5, tiempo_10, tiempo_20, tiempo_100, tiempo_200 = [], [], [], [], [], []
        nodos_0, nodos_5, nodos_10, nodos_20, nodos_100, nodos_200 = [], [], [], [], [], []
        for dato in datos:
            tiempos = dato.tiempos
            nodos = dato.nodos
            tiempo_0.append(tiempos[0])
            nodos_0.append(nodos[0])
            tiempo_5.append(tiempos[1])
            nodos_5.append(nodos[1])
            tiempo_10.append(tiempos[2])
            nodos_10.append(nodos[2])
            tiempo_20.append(tiempos[3])
            nodos_20.append(nodos[3])
            tiempo_100.append(tiempos[4])
            nodos_100.append(nodos[4])
            tiempo_200.append(tiempos[5])
            nodos_200.append(nodos[5])
        lista_tiempos = [tiempo_0, tiempo_5, tiempo_10, tiempo_20, tiempo_100, tiempo_200]
        lista_nodos = [nodos_0, nodos_5, nodos_10, nodos_20, nodos_100, nodos_200]
        tiempos = [np.mean(lista) for lista in lista_tiempos]
        nodos = [np.mean(lista) for lista in lista_nodos]
        return tiempos, nodos
    
class Valores_g():
    def __init__(self, weight):
        self.weight = weight
        self.mse_0 = []
        self.mse_25 = []
        self.mse_5 = []
        self.mse_10 = []
        self.mse_20 = []
        self.mse_100 = []
        self.mse_200 = []
        self.all_mse = [self.mse_0, self.mse_25, self.mse_5, self.mse_10, self.mse_20, self.mse_100, self.mse_200]

    
def escribir_archivo(nombre, escribir):
    file = open(nombre, "a")
    file.write(escribir + "\n")
    file.close()

