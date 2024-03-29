from copy import copy


class Operador:
    def __init__(self, id_prop, prec, add, delet):
        self.id = int(id_prop)
        self.prec = frozenset(prec)
        self.add = frozenset(add)
        self.delet = frozenset(delet)

    def __gt__(self, other):
        return int(self.id) > int(other.id)
    
    def __lt__(self, other):
        return int(self.id) < int(other.id)
    
    def __ge__(self, other):
        return int(self.id) >= int(other.id)
    
    def __le__(self, other):
        return int(self.id) <= int(other.id)

    def __str__(self):
        texto_id = "OPERADOR NUM " + str(self.id) + "\n"
        texto_pre = "PRECONDICIONES:" + "\n" + str(self.prec) + "\n"
        texto_add = "ADD:" + "\n" + str(self.add) + "\n"
        texto_del = "DEL:" + "\n" + str(self.delet)
        texto = texto_id + texto_pre + texto_add + texto_del
        return texto

    def es_aplicable(self, estado):
        for proposicion in self.prec:
            if proposicion not in estado.prop:
                return False
        for proposicion in self.add:
            if proposicion in estado.prop:
                return False
        return True


class Estado:
    def __init__(self, proposiciones, ops, padre=None, op_anterior=None, dict=None, goal=None, posibles=None):
        self.prop = frozenset(proposiciones)
        self.padre = padre
        self.op_anterior = op_anterior
        self.largo = 0
        self.g = 10000000000
        self.key = -1
        self.heap_index = 0
        self.operadores = ops
        self.dict = dict
        self.goal = goal
        self.posibles = posibles
        self.lugar = None
        self.h_nn = None
        self.busqueda_inversa = False

    def __hash__(self):
        return hash(self.prop)

    def is_goal(self):
        if self.goal is None:
            print("none")
            print(self.prop)
            print(self.padre)
        return True if self.goal == self else False

    def succ(self):
        sucesores = []
        for op in self.operadores:
            if op.es_aplicable(self):
                hijo = self.aplicar_operador(op)
                sucesores.append(hijo.prop)
        if self.posibles is not None:
            print("HOLA")
            return self.revisar_succ(sucesores)
        else:
            return sorted(sucesores)
    
    def revisar_succ(self, succ):
        sucesores = []
        for sucesor in succ:
            if sucesor in self.posibles:
                sucesores.append(sucesor)
        return sucesores

    def aplicar_operador(self, op):
        permiso = op.es_aplicable(self)
        if permiso is False:
            print("El estado no cuenta con todas las precondiciones del operador")
        else:
            # si el operador es aplicable agregamos y eliminamos las proposiciones correspondientes
            # creamos una lista con las proposiciones agregadas
            nuevas_proposiciones = self.agregar_proposiciones(op.add, set(copy(self.prop)))
            # creamos una lista con las proposiciones eliminadas
            nuevas_proposiciones = self.borrar_proposiciones(op.delet, nuevas_proposiciones)
            # creamos el estado hijo
            estado_hijo = Estado(nuevas_proposiciones, self.operadores, self, op, goal=self.goal)
            return estado_hijo

    def agregar_proposiciones(self, prop_add, copia):
        for proposicion in prop_add:
            if proposicion not in copia:
                copia.add(proposicion)
        return copia

    def borrar_proposiciones(self, prop_del, proposiciones):
        for proposicion in prop_del:
            if proposicion in proposiciones:
                proposiciones.remove(proposicion)
        return proposiciones

    def heuristic(self):
        return self.dict[self.prop]

    def __str__(self):
        return str(self.prop)

    def __eq__(self, otro):
        return True if self.prop == otro.prop else False
