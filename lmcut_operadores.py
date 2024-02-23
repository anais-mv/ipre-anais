from grafo import cargar_grafo
from clase_datos import escribir_archivo
from SortedSet.sorted_set import SortedSet

file_name = "grafos//grafo_NUEVO_2023-08-27 22.33.24.589415_--can_prop=16--can_op=100--rango=5--max_add=2--min_ap=3.pickle"

grafo = cargar_grafo(file_name)
ops = SortedSet(grafo.op_disp)
props = grafo.prop_disp
archivo = "archivos terminal//OPERADORES LMCUT.txt"
nombres_ops = []
open_archivo = open(archivo, "w")
open_archivo.close()
for op in ops:
    nombre_op = "op"
    if "-" in str(op.id):
        nombre_op += f"_{str(op.id)[1:]}"
    else:
        nombre_op += str(op.id)
    print(f"{nombre_op} = Operator(op+{str(op.id)}, {op.prec}, {op.add}, {op.delet})")
    escribir_archivo(archivo, f"{nombre_op} = Operator(op+{str(op.id)}, {op.prec}, {op.add}, {op.delet})")
    nombres_ops.append(nombre_op)

string_lista = "["
for nombre in nombres_ops:
    if nombre != nombres_ops[-1]:
        string_lista += f"{nombre}, "
    else:
        string_lista += f"{nombre}]"
print(f"ops = {string_lista}")
escribir_archivo(archivo, f"ops = {string_lista}")

string_lista = "["
for prop in props:
    if prop != props[-1]:
        string_lista += f"{prop}, "
    else:
        string_lista += f"{prop}]"
print(f"facts = {string_lista}")
escribir_archivo(archivo, f"facts = {string_lista}")

objetivo = grafo.objetivo
inicial = grafo.iniciales[0]

print(f"final = {objetivo}")
escribir_archivo(archivo, f"final = {objetivo}")
print(f"inicial = {inicial}")
escribir_archivo(archivo, f"inicial = {inicial}")