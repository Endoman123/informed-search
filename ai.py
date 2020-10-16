import gridworld
from math import *
from queue import PriorityQueue

class AIVertex:
    vertex = None
    coordinate = (-1, -1)
    parent = None

    def __init__(self, v, x, y):
        self.vertex = v
        self.coordinate = (x, y) 

def h_pythagorean(v):
     
    pass

def cost(map, s, s_prime):
    return -1


# A* pathfinding algorithm
def a_star(map, start, goal, h = None):
    rows = len(map)
    cols = len(map[0])

    fringe = PriorityQueue()
    closed = [] 
    parent = {i: {j: None for j in range(cols)} for i in range(rows)}  
   
    g = {i: {j: inf for j in range(cols)} for i in range(rows)}

    g[start[0]][start[1]] = 0 
    
   
    fringe.put((start_coord, h(start)))

    while not fringe.empty():
        s = fringe.get()

        if s == goal:
            return

        closed += [s]

        for i in range(max(0, s[1] - 1), min(rows, s[1] + 2)):
            for j in range(max(0, s[0] - 1), min(cols, s[0] + 2)):
                s_p = (i, j)

                if s_p not in closed:
                    with fringe.mutex:
                        if s_p not in fringe.queue:
                            g[s_p[1]][s_p[0]] = inf
                            parent[s_p[1]][s_p[0]] = None 
                    if g[s[1]][s[0]] + cost(map, s, s_p) < g[s_p[1]][s_p[0]]: 
                        g[s_p[1]][s_p[0]] = g[s[1]][s[0]] + cost(map, s, s_p)
                        parent[s_p[1]][s_p[0]] = s
                        if 
