class Node:
    def __init__(self, search_state, parent=None, action=''):
        self.state = search_state
        self.parent = parent
        if parent:             # compatibilidad con DFS/BFS
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.action = action    # es el nombre de la accion
        self.key = -1           # es la funcion f
        self.g = 10000000000    # la funcion g de A*
        self.heap_index = 0     # la posición de este nodo en el heap (0 si es que no está en el heap)
        self.h = -1             # la funcion h de A*
        self.closed = False  # Usado para ARA*. True si el nodo está closed
        self.path_disc = 0

    def __repr__(self):
        return self.state.__repr__()

    def trace(self):
        s = ''
        if self.parent:
            s = self.parent.trace()
            s += '-' + self.action + '->'
        s += str(self.state)
        return s

    def trace2(self):
        s = ''
        if self.parent:
            s = self.parent.trace2()
            #s += '-' + self.action + '->'
        s += str(self.Deepcube_to_Korf(self.state.board))+"\n"
        return s

    def trace_states(self, cost_optimal):
        s = ''
        if self.parent:
            s = self.parent.trace_states(cost_optimal)
        s += str(self.state.board) + " = " + str(cost_optimal-self.g) + "\n"
        return s

    
