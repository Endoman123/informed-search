from math import sqrt, inf
from queue import PriorityQueue

import ai

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

def uniform_search(map, start, goal):

    queue = PriorityQueue()
    queue.put((0, start))
    rows = len(map)
    cols = len(map[0])
    closed = []
    parent = {i: {j: None for j in range(cols)} for i in range(rows)}
    costs = {i: {j: inf for j in range(cols)} for i in range(rows)}
    while not queue.empty():
        pop = queue.get()
        s = pop[1]
        if all(a == b for a, b in zip(s, goal)):  # End goal
            print("it gets here")
            ret = {'cost': costs, 'map': [s]}
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
                path_cost = cost(map, s, s_p)

                if s_p not in closed and path_cost < costs[i][j]:
                    parent[i][j] = s
                    costs[i][j] = path_cost
                    in_fringe = False
                    with queue.mutex:
                        in_fringe = s_p in queue.queue
                    if not in_fringe:
                        queue.put((path_cost, s_p))

    print("Failed to find the goal")
    return