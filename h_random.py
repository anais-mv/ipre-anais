from astar import Astar
import time
from grafo import cargar_grafo
from main import cantidad
from clase_datos import Resultados, Datos, escribir_archivo
import pickle
from focal_search import FocalSearch
import numpy as np
from random import randint

def guardar_h(nombre, h):
    file = open(nombre, "wb")
    pickle.dump(h, file)
    file.close()

file_name = "grafos//grafo_NUEVO_2023-08-27 22.33.24.589415_--can_prop=16--can_op=100--rango=5--max_add=2--min_ap=3.pickle"
# file_name = "../storage/grafo_2023_09_13_14_25_29_283928_can_prop=21_can_op=200_rango=3.pickle"

grafo = cargar_grafo(file_name)

h_random = dict()
# for estado in grafo.estados:
for key in grafo.h_aristas:
    h_random[key] = randint(0, 100)

file_name = file_name.replace("grafo", "h_random")
guardar_h(file_name, h_random)
