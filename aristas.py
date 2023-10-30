from grafo import cargar_grafo
from operadores import crear_operadores
from planning_problem import Operador

def nuevos_operadores(grafo, can_prop, can_op, rango, max_add):
    can_op = can_op // 2
    set_operadores = set()
    set_final = set()
    for op in grafo.op_disp:
        set_final.add(op)
        set_operadores.add((op.prec, op.add, op.delet))
    nuevos, _ = crear_operadores(can_prop, can_op, rango, max_add)
    can_nuevos = 0
    for op in nuevos:
        tupla_op = (op.prec, op.add, op.delet)
        if tupla_op not in set_operadores:
            set_final.add(op)
            can_nuevos += 1
    print(f"operadores nuevos: {can_nuevos}")
    return set_final

def revisar_h_diferentes(grafo, perfect, aristas):
    dif = 0
    for estado in perfect:
        h_perfect = perfect[estado]
        h_aristas = aristas[estado]
        if h_perfect != h_aristas:
            dif += 1
    print(f"Porcentaje de heurísticas diferentes: {round(dif/len(perfect) * 100, 2)}")

def nuevos_operadores_alternativo(grafo):
    set_operadores = set()
    set_final = set()
    can_nuevos = 0
    for op in grafo.op_disp:
        set_final.add(op)
        set_operadores.add((op.prec, op.add, op.delet))
    # print((op.prec, op.add, op.delet))
    for op in grafo.op_disp:
        nuevo_prec = set()
        for prop in op.prec:
            if prop in op.add or prop in op.delet:
                nuevo_prec.add(prop)
        nuevo_prec = frozenset(nuevo_prec)
        if (nuevo_prec, op.add, op.delet) not in set_operadores:
            nuevo = Operador("*" + str(op.id), nuevo_prec, op.add, op.delet)
            set_final.add(nuevo)
            can_nuevos += 1
            prec = nuevo.prec.union(nuevo.add)
            prec_inverso = set()
            for proposicion in prec:
                if proposicion not in nuevo.delet:
                    prec_inverso.add(proposicion)
            nuevo_inverso = Operador("-" + str(nuevo.id), nuevo_prec, nuevo.delet, nuevo.add)
            if (nuevo_inverso.prec, nuevo_inverso.add, nuevo_inverso.delet) not in set_operadores:
                set_final.add(nuevo_inverso)
                can_nuevos += 1
    # print((nuevo_prec, op.add, op.delet))
    # print((nuevo_inverso.prec, nuevo_inverso.add, nuevo_inverso.delet))
    print(f"operadores nuevos: {can_nuevos}")
    return set_final
    