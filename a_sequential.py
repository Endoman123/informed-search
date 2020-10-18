import ai
import gridworld
from ai import *
from math import *
from queue import PriorityQueue

# A* Sequential search
# map: Gridworld terrain map
# start: Tuple representing start coordinate in (x, y)
# goal: Tuple representing goal coordinate in (x, y)
# w1: Weight 1, default 1.25
# w2: Weight 2, default 2
def a_sequential(map, start, goal, w1 = 1.25, w2 = 2):
    rows = len(map)
    cols = len(map[0])

    fringes = [PriorityQueue() for i in range(5)]
    closed = []
    parent = {i: {j: None for j in range(cols)} for i in range(rows)}

    f = {k: {i: {j: inf for j in range(cols)} for i in range(rows)} for k in range(5)}
    g = {k: {i: {j: inf for j in range(cols)} for i in range(rows)} for k in range(5)}
    h = {k: {i: {j: inf for j in range(cols)} for i in range(rows)} for k in range(5)}

    for i in range(5):
        for x in range(rows):
            for y in range(cols):
                h[i][x][y] = ai.getHValue(x, y, i, goal, start)

    for i in range(5):
        f[i][start[1]][start[0]] = 0 + w1 * h[i][start[1]][start[0]]
        g[i][start[1]][start[0]] = 0
        fringes[i].put((f[i][start[1]][start[0]], start))

    while not fringes[0].empty():
        for index in range(1, 5):
            minkey = fringes[0].queue[0][0]
            minkey2 = fringes[index].queue[0][0]

            if minkey2 <= w2 * minkey:
                pop2 = fringes[index].get()
                s2 = pop2[1]
                if all(a == b for a, b in zip(s2, goal)):  # End goal
                    ret = {'f': f, 'g': g, "h": h, 'map': [s2]}
                    while parent[s2[1]][s2[0]] != None:
                        s2 = parent[s2[1]][s2[0]]
                        ret['map'].insert(0, s2)

                    print("Found the destination")
                    return ret
                for i in range(max(0, s2[1] - 1), min(rows, s2[1] + 2)):
                    for j in range(max(0, s2[0] - 1), min(cols, s2[0] + 2)):

                        s_p = (j, i)
                        if s_p == s2:
                            continue

                        g_temp = g[index][s2[1]][s2[0]] + cost(map, s2, s_p)

                        if s_p not in closed and g_temp < g[index][i][j]:
                            parent[i][j] = s2
                            g[index][i][j] = g_temp
                            f[index][i][j] = g[index][i][j] + w1 * h[index][i][j]

                            in_fringe = False
                            with fringes[index].mutex:
                                in_fringe = s_p in fringes[index].queue

                            if not in_fringe:
                                fringes[index].put((f[index][i][j], s_p))
            else:
                pop = fringes[0].get()
                s = pop[1]
                if all(a == b for a, b in zip(s, goal)):  # End goal
                    ret = {'f': f, 'g': g, "h": h, 'map': [s]}
                    while parent[s[1]][s[0]] != None:
                        s = parent[s[1]][s[0]]
                        ret['map'].insert(0, s)

                    print("Found the destination")
                    return ret

                for i in range(max(0, s[1] - 1), min(rows, s[1] + 2)):
                    for j in range(max(0, s[0] - 1), min(cols, s[0] + 2)):
                        s_p = (j, i)
                        if s_p == s:
                            continue

                        g_temp = g[0][s[1]][s[0]] + cost(map, s, s_p)

                        print(g[0][i][j])
                        print(g_temp)
                        if s_p not in closed and g_temp < g[0][i][j]:
                            parent[i][j] = s
                            g[0][i][j] = g_temp
                            f[0][i][j] = g[0][i][j] + h[0][i][j]

                            in_fringe = False
                            with fringes[0].mutex:
                                in_fringe = s_p in fringes[0].queue

                            if not in_fringe:
                                fringes[0].put((f[0][i][j], s_p))
                            break
    print("Failed")
    return None
