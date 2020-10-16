from queue import PriorityQueue

import ai


def uniform_search(map, start, end):
    if ai.isValid(start.coordinates[0], start.coordinates[1]) is False:
        print("Invalid Start")
        return
    if ai.isValid(end.coordinates[0], end.coordinates[1]) is False:
        print("Invalid End")
        return
    if start.isBlocked() or end.isBlocked():
        print("Blocked Node Chosen")
        return
    queue = PriorityQueue()
    queue.put((0, start.coordinates))

    closed = [[False for j in range(120)] for i in range(160)]
    while not queue.empty():
        (f, (x, y)) = queue.get()
        closed[x][y] = True
        if ai.isDestination(x, y, end):
            ai.trace(map, end)
            return
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ai.isValid(x + i, y + j) and closed[x + i][y + j] is False and map[x + i][
                    y + j].isBlocked() is False:
                    if x == j | y == i:
                        cost = ai.get_cost_diagonal(x, y, x + i, y + j, map)
                        map[x + i][y + j].parent_x = x
                        map[x + i][y + j].parent_y = y
                        queue.put((cost, (x + i, y + j)))
    print("Failed to find the goal")
    return
