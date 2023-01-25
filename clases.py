from copy import copy


class Operador:
    def __init__(self, id_prop, prec, add, delet):
        self.id = id_prop
        self.prec = frozenset(prec)
        self.add = frozenset(add)
        self.delet = frozenset(delet)

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
        return True


class Estado:
    def __init__(self, proposiciones, padre=None, op_anterior=None):
        self.prop = frozenset(proposiciones)
        self.padre = padre
        self.op_anterior = op_anterior
        self.largo = 0
        self.g = 10000000000
        self.key = -1
        self.heap_index = 0

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
            estado_hijo = Estado(nuevas_proposiciones, self, op)
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
        # nuevas_proposiciones = set()
        # for proposicion in copia:
        #     if proposicion not in prop_del:
        #         nuevas_proposiciones.add(proposicion)
        # return nuevas_proposiciones

    def __str__(self):
        return str(self.prop)

    def __eq__(self, otro):
        return True if self.prop == otro.prop else False
