import gridworld
from ai import *
from math import *
from queue import PriorityQueue

# A* pathfinding algorithms

# Weighted
# map: Gridworld terrain map
# start: Tuple representing start coordinates in (x, y)
# goal: Tuple representing goal coordinates in (x, y)
# h: Heuristic function, default h_pythagorean
# w: Weight, default 1.0
def weighted(map, start, goal, w = 1, h = h_pythagorean):
    rows = len(map)
    cols = len(map[0])

    fringe = PriorityQueue()
    closed = []
    parent = {i: {j: None for j in range(cols)} for i in range(rows)}

    f = {i: {j: inf for j in range(cols)} for i in range(rows)}
    g = {i: {j: inf for j in range(cols)} for i in range(rows)}
    h = {i: {j: h(v = (j, i), goal = goal) for j in range(cols)} for i in range(rows)}

    f[start[1]][start[0]] = 0 + w * h[start[1]][start[0]]
    g[start[1]][start[0]] = 0

    fringe.put((f[start[1]][start[0]], start))

    while not fringe.empty():
        pop = fringe.get()

        s = pop[1]

        if all(a == b for a, b in zip(s, goal)):  # End goal
            ret = {'f': f, 'g': g, "h": h, 'map': [s]}
            while parent[s[1]][s[0]] != None:
                s = parent[s[1]][s[0]]
                ret['map'].insert(0, s)

            return ret

        closed += [s]
        for i in range(max(0, s[1] - 1), min(rows, s[1] + 2)):
            for j in range(max(0, s[0] - 1), min(cols, s[0] + 2)):
                s_p = (j, i)
                if s_p == s:
                    continue

                c_g = g[s[1]][s[0]] if w != 0 else 0
                g_temp =  + cost(map, s, s_p)

                if s_p not in closed and g_temp < g[i][j]:
                    parent[i][j] = s
                    g[i][j] = g_temp
                    f[i][j] = g[i][j] + w * h[i][j]

                    in_fringe = False
                    with fringe.mutex:
                        in_fringe = s_p in fringe.queue

                    if not in_fringe:
                        fringe.put((f[i][j], s_p))

    print("failed")
    return None

# Uniform-cost
# map: Gridworld terrain map
# start: Tuple representing start coordinates in (x, y)
# goal: Tuple representing goal coordinates in (x, y)
def uniform(map, start, goal):
    return weighted(map, start, goal, 0, lambda **kwargs: 0) 

# Sequential-Heuristic
# map: Gridworld terrain map
# start: Tuple representing start coordinate in (x, y)
# goal: Tuple representing goal coordinate in (x, y)
# w1: Overall weight, default 1.25
# w2: Inadmissable-favored weight, default 2
def sequential(map, start, goal, w1 = 1.25, w2 = 2):
    rows = len(map)
    cols = len(map[0])
    n_h = len(list_h)

    fringes = [PriorityQueue() for i in range(5)]
    closed = []
    parent = {k: {i: {j: None for j in range(cols)} for i in range(rows)} for k in range(n_h)}

    f = {k: {i: {j: inf for j in range(cols)} for i in range(rows)} for k in range(n_h)}
    g = {k: {i: {j: inf for j in range(cols)} for i in range(rows)} for k in range(n_h)}
    h = {k: {i: {j: list_h[k](start = start, goal = goal, v = (j, i)) for j in range(cols)} for i in range(rows)} for k in range(n_h)}

    for i in range(n_h):
        f[i][start[1]][start[0]] = 0 + w1 * h[i][start[1]][start[0]]
        g[i][start[1]][start[0]] = 0
        fringes[i].put((f[i][start[1]][start[0]], start))

    while not fringes[0].empty():
        for index in range(1, n_h):
            minkey = fringes[0].queue[0][0]
            minkey2 = fringes[index].queue[0][0]

            # 0th key or ith key has the current smallest fscore 
            min_i = index if minkey2 <= w2 * minkey else 0

            fringe = fringes[min_i]
            c_p = parent[min_i]
            c_f = f[min_i]
            c_g = g[min_i]
            c_h = h[min_i]
            w = 1 if min_i == 0 else w1 

            pop = fringe.get()
            s = pop[1]

            if all(a == b for a, b in zip(s, goal)):  # End goal
                ret = {'f': c_f, 'g': c_g, "h": c_h, 'map': [s]}
                while c_p[s[1]][s[0]] != None:
                    s = c_p[s[1]][s[0]]
                    ret['map'].insert(0, s)

                return ret

            for i in range(max(0, s[1] - 1), min(rows, s[1] + 2)):
                for j in range(max(0, s[0] - 1), min(cols, s[0] + 2)):
                    s_p = (j, i)

                    if s_p == s:
                        continue

                    g_temp = c_g[s[1]][s[0]] + cost(map, s, s_p)

                    if s_p not in closed and g_temp < c_g[i][j]:
                        c_p[i][j] = s
                        c_g[i][j] = g_temp
                        c_f[i][j] = c_g[i][j] + w * c_h[i][j]

                        in_fringe = False
                        with fringe.mutex:
                            in_fringe = s_p in fringe.queue

                        if not in_fringe:
                            fringe.put((c_f[i][j], s_p))

    print("failed")
    return None
