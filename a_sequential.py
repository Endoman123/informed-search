from queue import PriorityQueue

import ai


def a_sequential(map, start, end, w1=1.25, w2=2):
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
    closed = [[[False for j in range(120)] for i in range(160)]]
    queues = [PriorityQueue() for i in range(5)]
    for i in range(1, 5):
        queues[i].put((0, start.coordinates))
    while not queues[0].empty():
        (key, (main_x, main_y)) = queues[0].get()
        for index in range(1, 5):
            (key2, (x, y)) = queues[index].get()
            if closed[x][y]:
                continue
            if key2 <= (w2 * key):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if ai.isValid(x + i, y + j):
                            expand_vertex(x, y, x + i, y + j, map, end, closed, queues[index], index, start, w1)
                closed[x][y] = True
            else:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if ai.isValid(main_x+i, main_y + j):
                            expand_vertex(main_x, main_y, main_x + i, main_y + j, map, end, closed, queues[0], 0, start, w1)
                queues[index].put((key2, (x, y)))


def expand_vertex(x, y, x_new, y_new, map, end, closed, queue, i, start, w1):
    if ai.isDestination(x_new, y_new, end):
        ai.mark_destination(x, y, x_new, y_new, map)
    elif not closed[x_new][y_new] & map[x_new][y_new].isBlocked() is False:
        hOld = w1 * ai.getHValue(x, y, i, end, start)
        hNew = w1 * ai.getHValue(x_new, y_new, i, end, start)

        if x == x_new | y == y_new:
            gNew = ai.get_cost_regular(x, y, x_new, y_new, map)
        else:
            gNew = ai.get_cost_diagonal(x, y, x_new, y_new, map)

        admissible = ai.isAdmissible(hNew, hOld, gNew)
        gNew = ai.get_cost_regular(x, y, x_new, y_new, map)
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            queue.put((fNew, (x_new, y_new)))
            ai.update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)

