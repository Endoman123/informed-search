from queue import PriorityQueue

import ai


def a_star(map, start, end, w=0):
    if ai.isValid(start.coordinates[0], start.coordinates[1]) is False:
        print("Invalid Start")
        return
    if ai.isValid(end.coordinates[0], end.coordinates[1]) is False:
        print("Invalid End")
        return
    if start.isBlocked() | end.isBlocked():
        print(start.isBlocked())
        print("Blocked Node Chosen")
        return
    closed = [[False for j in range(120)] for i in range(160)]
    queue = PriorityQueue()
    queue.put((0, (start.coordinates[0], start.coordinates[1])))

    while queue.empty() is False:
        (f, (x, y)) = queue.pop()
        closed[x][y] = True
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ai.isValid(x + i, y + j):
                    expand_vertex_a_star(x, y, x + i, y + j, map, end, closed, queue, w)


def expand_vertex_a_star(x, y, x_new, y_new, map, end, closed, queue, w=0):
    if ai.isDestination(x_new, y_new, end):
        ai.mark_destination(x, y, x_new, y_new, map)
    elif not closed[x_new][y_new] & map[x_new][y_new].isBlocked() is False:
        if (x_new == x) | (y_new == y):
            gNew = ai.get_cost_regular(x, y, x_new, y_new, map)
        else:
            gNew = ai.get_cost_diagonal(x, y, x_new, y_new, map)
        hOld = ai.getHValue(x, y, 0, end)
        hNew = ai.getHValue(x_new, y_new, 0, end)
        admissible = ai.isAdmissible(hNew, hOld, ai.get_cost_diagonal(x, y, x_new, y_new, map))
        if w != 0:
            hNew *= w
        fNew = gNew + hNew
        if map[x_new][y_new].f < fNew:
            queue.put((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def update_vertex(x, y, x_new, y_new, map, f, g, h):
    map[x_new][y_new].f = f
    map[x_new][y_new].g = g
    map[x_new][y_new].h = h
    map[x_new][y_new].parent_x = x
    map[x_new][y_new].parent_y = y
