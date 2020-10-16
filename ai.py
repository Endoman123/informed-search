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
    return 0

def cost(map, s, s_prime):
    v = map[s[1]][s[0]]
    v_prime = map[s_prime[1]][s_prime[0]]
    ret = 9001 
    
    if v_prime.isBlocked() or v.isBlocked(): # You cannot transition between blocked cells
        return ret
    
    f_v = 1
    f_vp = 1

    if not any(a == b for a, b in zip(s, s_prime)): # Diagonal
        f_v = sqrt(2) 
        f_vp = sqrt(2) 

    elif v.isHighway() and v_prime.isHighway(): # On a highway
        f_v /= 4
        f_vp /= 4

    f_v *= 2 if v.isHardToTraverse() else 1
    f_vp *= 2 if v_prime.isHardToTraverse() else 1

    ret = f_v + f_vp
    ret /= 2

    return ret


# A* pathfinding algorithm
def a_star(map, start, goal, h = h_pythagorean):
    rows = len(map)
    cols = len(map[0])

    fringe = PriorityQueue()
    closed = [] 
    parent = {i: {j: None for j in range(cols)} for i in range(rows)}  
   
    g = {i: {j: inf for j in range(cols)} for i in range(rows)}
    g[start[1]][start[0]] = 0 
   
    fringe.put((h(start), start))

    while not fringe.empty():
        s = fringe.get()[1]
        if s == goal:
            print("finished")
            return closed

        closed += [s]

        for i in range(max(0, s[1] - 1), min(rows, s[1] + 2)):
            for j in range(max(0, s[0] - 1), min(cols, s[0] + 2)): 
                if (j, i) == s:
                    continue

                s_p = (j, i) 
                g_temp = g[s[1]][s[0]] + cost(map, s, s_p)

                if g_temp < g[i][j]:
                    parent[i][j] = s
                    g[i][j] = g_temp

                    in_fringe = False
                    with fringe.mutex:
                        in_fringe = s_p in fringe.queue
                        print(in_fringe)

                    if not in_fringe:
                        fringe.put((g[i][j] + h(s_p), s_p)) 

    print(closed)
    return None
