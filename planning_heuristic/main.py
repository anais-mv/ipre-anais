from pyperplan.pddl.pddl import Domain 
from pyperplan.task import Task, Operator

from pyperplan.heuristics.blind import BlindHeuristic
from pyperplan.search.searchspace import SearchNode

#from strips_hgn.planning.pyperplan_api import get_domain_and_task
#from strips_hgn.utils import Number

# asi se representa el task 
# https://github.com/aibasel/pyperplan/blob/main/pyperplan/task.py

#los op son (nombre, pre, add, del) 
op1 = Operator("op1", set((1,2)), set((3,4)), set((1,2)))
op2 = Operator("op2", set((3,4)), set((1,2)), set((3,4)))

#la Task es name, facts, initial_state, goals, operators):
t1 = Task("t1", set((1,2,3,4)), set((1,2)), set((3,4)), set((op1,op2))  )

h  = BlindHeuristic(t1)

nodo1 = SearchNode(set((1,2)), None, "ac1", 0)
hstate = h(nodo1)
print("heuristic nodo 1", hstate)

nodo2 = SearchNode(set((3,4)), None, "ac2", 0)
hstate = h(nodo2)
print("heuristic nodo 1", hstate)
