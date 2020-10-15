import gridworld
import math
from math import sqrt


def isValid(row, col):
    return (row >= 0) & (row < 120) & (col >= 0) & (col < 160)


def isDestination(row, col, goal):
    if row == goal.coordinates[0] & col == goal.coordinates[1]:
        return True
    else:
        return False


def trace(map, goal):
    x, y = goal.coordinates
    path = []
    while map[x][y].parent_x != -1 & map[x][y].parent_y != -1:
        path.append(map[x][y])
        temp_x = map[x][y].parent_x
        temp_y = map[x][y].parent_y
        x = temp_x
        y = temp_y
    print(path)
    return path

def getHValue(x, y, i, goal, start):
    if i == 0:
        hValue = pythagorean(x, y, goal)
    elif i == 1:
        hValue = manhattan_distance(x,y, goal)
    elif i == 2:
        hValue = getHValDiagonalDistance(x, y, goal)
    elif i == 3:
        hValue = getHValCustom(x, y, goal, start)
    else:
        hValue = getHValManhattanDistance(x, y, goal)

def manhattan_distance(x, y, goal):
    end_x, end_y = goal.coordinates
    return abs(end_x - x) + abs(end_y - y)


def pythagorean(x, y, goal):
    end_x, end_y = goal.coordinates
    h = math.sqrt(((end_x - x) * (end_x - x)) + ((end_y - y) * (end_y - y)))
    return h


def getHValDiagonalDistance(x, y, goal):
    end_x, end_y = goal.coordinates
    h = max(abs(x - end_x), abs(y - end_y))
    return h

<<<<<<< Updated upstream
def getHValManhattanDistanceHex (x, y, goal):
    end_x, end_y = goal.coordinates
    dx = end_x - x
    dy = end_y - y
    if ((dx > 0 and dy > 0) or (dx < 0 and dy < 0)):
        h = abs(dx + dy)
    else:
        h = max(abs(dx), abs(dy))
    return h  
    
def getHValCustom (x, y, goal, start):
=======
def getHValCustom(x, y, goal, start):
>>>>>>> Stashed changes
    end_x, end_y = goal.coordinates
    begin_x, begin_y = start.coordinates
    stDistance = sqrt(pow(end_x - begin_x, 2) + pow(end_y - begin_y, 2))
    h = abs(stDistance - (sqrt(pow(x - begin_x, 2) + pow(y - begin_y, 2))))
    return h


def getHValManhattanDistance(x, y, goal):
    end_x, end_y = goal.coordinates
    h = abs(x - end_x) + abs(y - end_y)
    return h


def a_sequential(map, start, end):
    print(start.coordinates)
    if isValid(start.coordinates[0], start.coordinates[1]) is False:
        print("Invalid Start")
        return
    if isValid(end.coordinates[0], end.coordinates[1]) is False:
        print("Invalid End")
        return
    if start.isBlocked() | end.isBlocked():
        print(start.isBlocked())
        print("Blocked Node Chosen")
        return
    w1 = 1.25
    w2 = 2.0
    closed = [[[False for j in range(120)] for i in range(160)] for k in range(6)]
    queues = [PriorityQueue() for i in range(6)]
    for i in range(6):
        queues[i].put((0, start.coordinates))

    while not queues[0].empty():
        closed
        (key, (main_x, main_y)) = queues[0].get()
        for i in range(1, 6):
            (key2, (x, y)) = queues[i].get()
            closed[i][x][y] = True
            if key2 <= w2 * key:
                if isDestination(x, y, end):
                    print("Destination Found")
                    trace(map, end)
                    return
                else:
                    if isValid(x - 1, y):
                        expand_vertex_regular(x, y, x - 1, y, map, end, closed, queues[i], i)
                        # South
                    if isValid(x + 1, y):
                        # Check if it's the destination
                        expand_vertex_regular(x, y, x + 1, y, map, end, closed, queues[i], i)
                        # East
                    if isValid(x, y + 1):
                        # Check if it's the destination
                        expand_vertex_regular(x, y, x, y + 1, map, end, closed, queues[i], i)
                        # West
                    if isValid(x, y - 1):
                        expand_vertex_regular(x, y, x, y - 1, map, end, closed, queues[i], i)
                    # North-East
                    if isValid(x - 1, y + 1):
                        expand_vertex_diagonal(x, y, x - 1, y + 1, map, end, closed, queues[i], i)
                        # North West
                    if isValid(x - 1, y - 1):
                        expand_vertex_diagonal(x, y, x - 1, y - 1, map, end, closed, queues[i], i)
                        # South-East
                    if isValid(x + 1, y + 1):
                        expand_vertex_diagonal(x, y, x + 1, y + 1, map, end, closed, queues[i], i)
                        # South-West
                    if isValid(x + 1, y - 1):
                        # Check if it's the destination
                        expand_vertex_diagonal(x, y, x + 1, y - 1, map, end, closed, queues[i], i)
            else:
                if isDestination(main_x, main_y, end):
                    print("Destination Found")
                    trace(map, end)
                    return
                else:
                    if isValid(x - 1, y):
                        expand_vertex_regular(x, y, x - 1, y, map, end, closed, queues[0], 0)
                        # South
                    if isValid(x + 1, y):
                        # Check if it's the destination
                        expand_vertex_regular(x, y, x + 1, y, map, end, closed, queues[0], 0)
                        # East
                    if isValid(x, y + 1):
                        # Check if it's the destination
                        expand_vertex_regular(x, y, x, y + 1, map, end, closed, queues[0], 0)
                        # West
                    if isValid(x, y - 1):
                        # Check if it's the destination
                        expand_vertex_regular(x, y, x, y - 1, map, end, closed, queues[0], 0)
                    # South-West
                    if isValid(x + 1, y - 1):
                        expand_vertex_diagonal(x, y, x + 1, y - 1, map, end, closed, queues[0], 0)

                        # North-East
                    if isValid(x - 1, y + 1):
                        expand_vertex_diagonal(x, y, x - 1, y + 1, map, end, closed, queues[0], 0)
                        # North West
                    if isValid(x - 1, y - 1):
                        expand_vertex_diagonal(x, y, x - 1, y - 1, map, end, closed, queues[0], 0)

                    # South-East
                    if isValid(x + 1, y + 1):
                        expand_vertex_diagonal(x, y, x + 1, y + 1, map, end, closed, queues[0], 0)


def expand_vertex_regular(x, y, x_new, y_new, map, end, closed, queue, i):
    if isDestination(x_new, y_new, end):
        map[x_new][y_new].parent_x = x
        map[x_new][y_new].parent_y = y
        print("Destination Found")
        trace(map, end)
        return
    elif not closed[x_new][y_new] & map[x_new][y_new].isBlocked() is False:
        gNew = get_cost_regular(x, y, x_new, y_new, map)
        hNew = getHValue(x_new, y_new, i, end)
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            queue.put((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def get_cost_regular(x, y, x_new, y_new, map):
    if map[x][y].isHardToTraverse() is False and map[x][y].isHighway() is False:
        if map[x_new][y_new].isHardToTraverse() is False:
            cost = map[x][y].g + 1
        else:
            cost = map[x][y].g + 1.5
    elif map[x][y].code.isHardToTraverse() and map[x][y].isHighway() is False:
        if map[x_new][y_new].isHardToTraverse() is False:
            cost = map[x][y].g + 1.5
        else:
            cost = map[x][y].g + 2.0
    elif map[x][y].isHardToTraverse() is False and map[x][y].isHighway():
        if map[x_new][y_new].isHardToTraverse() is False and map[x_new][y_new].isHighway():
            cost = map[x][y].g + 0.25
        elif map[x_new][y_new].isHardToTraverse() and map[x_new][y_new].isHighway():
            cost = map[x][y].g + 0.375
        elif map[x_new][y_new].isHardToTraverse() is False:
            cost = map[x][y].g + 1
        else:
            cost = map[x][y].g + 1.5
    else:
        if map[x_new][y_new].isHardToTraverse() is False and map[x_new][y_new].isHighway():
            cost = map[x][y].g + 0.375
        elif map[x_new][y_new].isHardToTraverse() and map[x_new][y_new].isHighway():
            cost = map[x][y].g + 0.5
        elif map[x_new][y_new].isHardToTraverse() is False:
            cost = map[x][y].g + 1.5
        else:
            cost = map[x][y].g + 2.0
    return cost


def expand_vertex_diagonal(x, y, x_new, y_new, map, end, closed, queue, i):
    if isDestination(x_new, y_new, end):
        map[x_new][y_new].parent_x = x
        map[x_new][y_new].parent_y = y
        print("Destination Found")
        trace(map, end)
        return
    elif closed[x_new][y_new] is False and map[x_new][y_new].isUnblocked() is False:
        gNew = get_cost_diagonal(x, y, x_new, y_new, map)
        hNew = getHValue(x_new, y_new, i, end)
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            queue.put((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def update_vertex(x, y, x_new, y_new, map, f, g, h):
    map[x_new][y_new].f = f
    map[x_new][y_new].g = g
    map[x_new][y_new].h = h
    map[x_new][y_new].parent_x = x
    map[x_new][y_new].parent_y = y


def get_cost_diagonal(x, y, new_x, new_y, map):
    if map[x][y].isHardToTraverse is False:
        if map[new_x][new_y].isHardToTraverse() is False:
            cost = map[x][y].g + math.sqrt(2)
        else:
            cost = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
    else:
        if map[new_x][new_y].isHardToTraverse() is False:
            cost = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
        else:
            cost = map[x][y].g + math.sqrt(8)
    return cost


def expand_vertex_regular_a_star(x, y, x_new, y_new, map, end, closed, openList):
    if isDestination(x_new, y_new, end):
        map[x_new][y_new].parent_x = x
        map[x_new][y_new].parent_y = y
        print("Destination Found")
        trace(map, end)
        return
    elif not closed[x_new][y_new] & map[x_new][y_new].isBlocked() is False:
        gNew = get_cost_regular(x, y, x_new, y_new, map)
        hNew = getHValue(x_new, y_new, 0, end)
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            openList.append((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def expand_vertex_diagonal_a_star(x, y, x_new, y_new, map, end, closed, openList):
    if isDestination(x_new, y_new, end):
        map[x_new][y_new].parent_x = x
        map[x_new][y_new].parent_y = y
        print("Destination Found")
        trace(map, end)
        return
    elif closed[x_new][y_new] is False and map[x_new][y_new].isUnblocked() is False:
        gNew = get_cost_diagonal(x, y, x_new, y_new, map)
        hNew = getHValue(x_new, y_new, 0, end)
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            openList.append((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def expand_vertex_diagonal_a_star_weighted(x, y, x_new, y_new, map, end, closed, openList, w):
    if isDestination(x_new, y_new, end):
        map[x_new][y_new].parent_x = x
        map[x_new][y_new].parent_y = y
        print("Destination Found")
        trace(map, end)
        return
    elif closed[x_new][y_new] is False and map[x_new][y_new].isUnblocked() is False:
        gNew = get_cost_diagonal(x, y, x_new, y_new, map)
        hNew = getHValue(x_new, y_new, 0, end)
        hNew *= w
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            openList.append((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def expand_vertex_regular_a_star_weighted(x, y, x_new, y_new, map, end, closed, openList, w):
    if isDestination(x_new, y_new, end):
        map[x_new][y_new].parent_x = x
        map[x_new][y_new].parent_y = y
        print("Destination Found")
        trace(map, end)
        return
    elif not closed[x_new][y_new] & map[x_new][y_new].isBlocked() is False:
        gNew = get_cost_regular(x, y, x_new, y_new, map)
        hNew = getHValue(x_new, y_new, 0, end)
        hNew *= w
        fNew = gNew + hNew
        if map[x_new][y_new].f > fNew:
            openList.append((fNew, (x_new, y_new)))
            update_vertex(x, y, x_new, y_new, map, fNew, gNew, hNew)


def a_star(map, start, end):
    if isValid(start.coordinates[0], start.coordinates[1]) is False:
        print("Invalid Start")
        return
    if isValid(end.coordinates[0], end.coordinates[1]) is False:
        print("Invalid End")
        return
    if start.isBlocked() | end.isBlocked():
        print(start.isBlocked())
        print("Blocked Node Chosen")
        return

    closed = [[False for j in range(120)] for i in range(160)]
    openList = []
    openList.append((0, (start.coordinates[0], start.coordinates[1])))

    while len(openList) > 0:
        (f, (x, y)) = openList.pop()
        closed[x][y] = True
        gNew = 0
        # North
        if isValid(x - 1, y):
            # Check if it's the Goal Cell
            expand_vertex_regular_a_star(x, y, x - 1, y, map, end, closed, openList)
        # South
        if isValid(x + 1, y):
            expand_vertex_regular_a_star(x, y, x + 1, y, map, end, closed, openList)
        # East
        if isValid(x, y + 1):
            expand_vertex_regular_a_star(x, y, x, y + 1, map, end, closed, openList)
        # West
        if isValid(x, y - 1):
            expand_vertex_regular_a_star(x, y, x, y - 1, map, end, closed, openList)
        # North-East
        if isValid(x - 1, y + 1):
            expand_vertex_diagonal_a_star(x, y, x - 1, y + 1, map, end, closed, openList)
        # South-East
        if isValid(x + 1, y + 1):
            expand_vertex_diagonal(x, y, x + 1, y + 1, map, end, closed, openList)
        # South-West
        if isValid(x + 1, y - 1):
            expand_vertex_diagonal_a_star(x, y, x + 1, y - 1, map, end, closed, openList)
        if isValid(x - 1, y - 1):
            expand_vertex_regular_a_star(x, y, x - 1, y - 1, map, end, closed, openList)
    print("Failed to find a valid path")
    return


def a_star_weighted(map, start, end, w):
    if isValid(start.coordinates[0], start.coordinates[1]) is False:
        print("Invalid Start")
        return
    if isValid(end.coordinates[0], end.coordinates[1]) is False:
        print("Invalid End")
        return
    if start.isBlocked() | end.isBlocked():
        print(start.isBlocked())
        print("Blocked Node Chosen")
        return

    closed = [[False for j in range(120)] for i in range(160)]
    openList = []
    openList.append((0, (start.coordinates[0], start.coordinates[1])))

    while len(openList) > 0:
        (f, (x, y)) = openList.pop()
        closed[x][y] = True
        gNew = 0
        # North
        if isValid(x - 1, y):
            expand_vertex_regular_a_star_weighted(x, y, x - 1, y, map, end, closed, openList, w)
        # South
        if isValid(x + 1, y):
            expand_vertex_regular_a_star_weighted(x, y, x + 1, y, map, end, closed, openList, w)
        # East
        if isValid(x, y + 1):
            expand_vertex_regular_a_star_weighted(x, y, x, y + 1, map, end, closed, openList, w)
        # West
        if isValid(x, y - 1):
            expand_vertex_regular_a_star_weighted(x, y, x, y - 1, map, end, closed, openList, w)
        # North-East
        if isValid(x - 1, y + 1):
            expand_vertex_diagonal_a_star_weighted(x, y, x - 1, y + 1, map, end, closed, openList, w)
        # South-East
        if isValid(x + 1, y + 1):
            expand_vertex_diagonal_a_star_weighted(x, y, x + 1, y + 1, map, end, closed, openList, w)
        # South-West
        if isValid(x + 1, y - 1):
            expand_vertex_diagonal_a_star_weighted(x, y, x + 1, y - 1, map, end, closed, openList, w)
        if isValid(x - 1, y - 1):
            expand_vertex_regular_a_star_weighted(x, y, x - 1, y - 1, map, end, closed, openList, w)
    print("Failed to find a valid path")
    return


def uniform_search(map, start, end):
    if isValid(start.coordinates[0], start.coordinates[1]) is False:
        print("Invalid Start")
        return
    if isValid(end.coordinates[0], end.coordinates[1]) is False:
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
        if isDestination(x, y, end):
            print("Destination Found")
            trace(map, end)
            return
        if isValid(x - 1, y):
            if closed[x - 1][y] is False and map[x - 1][y].isBlocked() is False:
                cost = get_cost_regular(x, y, x -1, y, map)
                map[x - 1][y].parent_x = x
                map[x - 1][y].parent_y = y
                queue.put((cost, (x - 1, y)))
        if isValid(x + 1, y):
            if closed[x + 1][y] is False and map[x + 1][y].isBlocked() is False:
                cost = get_cost_regular(x, y, x + 1, y, map)
                map[x + 1][y].parent_x = x
                map[x + 1][y].parent_y = y
                queue.put((cost, (x + 1, y)))

        if isValid(x, y + 1):
            if closed[x][y + 1] is False and map[x][y + 1].isBlocked() is False:
                cost = get_cost_regular(x, y, x, y + 1, map)
                map[x][y + 1].parent_x = x
                map[x][y + 1].parent_y = y
                queue.put((cost, (x, y + 1)))

        if isValid(x, y - 1):
            if closed[x][y - 1] is False and map[x][y - 1].isBlocked() is False:
                cost = get_cost_regular(x, y, x, y - 1, map)
                map[x][y - 1].parent_x = x
                map[x][y - 1].parent_y = y
                queue.put((cost, (x, y - 1)))
        if isValid(x - 1, y + 1):
            if closed[x - 1][y + 1] is False and map[x - 1][y + 1].isBlocked() is False:
                cost = get_cost_diagonal(x, y, x -1, y+1, map)
                map[x - 1][y + 1].parent_x = x
                map[x - 1][y + 1].parent_y = y
                queue.put((cost, (x - 1, y + 1)))
        if isValid(x - 1, y - 1):
            if closed[x - 1][y - 1] is False and map[x - 1][y - 1].isBlocked() is False:
                cost = get_cost_diagonal(x, y, x-1, y -1, map)
                map[x - 1][y - 1].parent_x = x
                map[x - 1][y - 1].parent_y = y
                queue.put((cost, (x - 1, y - 1)))
        if isValid(x + 1, y + 1):
            if closed[x + 1][y + 1] is False and map[x + 1][y + 1].isBlocked() is False:
                cost = get_cost_diagonal(x, y, x +1, y +1, map)
                map[x + 1][y + 1].parent_x = x
                map[x + 1][y + 1].parent_y = y
                queue.put((cost, (x + 1, y + 1)))
        if isValid(x + 1, y - 1):
            if closed[x + 1][y - 1] is False and map[x + 1][y - 1].isBlocked() is False:
                cost = get_cost_diagonal(x, y, x + 1, y - 1, map)
                map[x + 1][y - 1].parent_x = x
                map[x + 1][y - 1].parent_y = y
                queue.put((cost, (x + 1, y - 1)))
    print("Failed to find the goal")
    return
