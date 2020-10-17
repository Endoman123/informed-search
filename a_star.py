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


def h_pythagorean(v, goal):
    return sum((a - b) ** 2 for a, b in zip(goal, v))


def cost(map, s, s_prime):
    v = map[s[1]][s[0]]
    v_prime = map[s_prime[1]][s_prime[0]]
    ret = inf

    if v.isBlocked() or v_prime.isBlocked():  # You cannot transition between blocked cells
        return ret

    f_v = 1
    f_vp = 1

    if not any(a == b for a, b in zip(s, s_prime)):  # Diagonal
        f_v = sqrt(2)
        f_vp = sqrt(2)

    elif v.isHighway() and v_prime.isHighway():  # On a highway
        f_v /= 4
        f_vp /= 4

    f_v *= 2 if v.isHardToTraverse() else 1
    f_vp *= 2 if v_prime.isHardToTraverse() else 1

    ret = f_v + f_vp
    ret /= 2

    return ret


# A* pathfinding algorithm
def a_star(map, start, goal, h=h_pythagorean, w = 0):
    print("You getting in here?")
    rows = len(map)
    cols = len(map[0])

    fringe = PriorityQueue()
    closed = []
    parent = {i: {j: None for j in range(cols)} for i in range(rows)}

    f = {i: {j: inf for j in range(cols)} for i in range(rows)}
    g = {i: {j: inf for j in range(cols)} for i in range(rows)}
    h = {i: {j: h((j, i), goal) for j in range(cols)} for i in range(rows)}
    if w != 0:
        f[start[1]][start[0]] = 0 + w * h[start[1]][start[0]]
    else :
        f[start[1]][start[0]] = 0 + h[start[1]][start[0]]
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

            print("Found the destination")
            return ret

        closed += [s]
        for i in range(max(0, s[1] - 1), min(rows, s[1] + 2)):
            for j in range(max(0, s[0] - 1), min(cols, s[0] + 2)):
                s_p = (j, i)
                if s_p == s:
                    continue

                g_temp = g[s[1]][s[0]] + cost(map, s, s_p)

                if s_p not in closed and g_temp < g[i][j]:
                    parent[i][j] = s
                    g[i][j] = g_temp
                    if w != 0:
                        f[i][j] = g[i][j] + w * h[i][j]
                    else:
                        f[i][j] = g[i][j] + h[i][j]

                    in_fringe = False
                    with fringe.mutex:
                        in_fringe = s_p in fringe.queue

                    if not in_fringe:
                        fringe.put((f[i][j], s_p))

    print("failed")
    return None