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


def getHValue(x, y, goal):
    end_x, end_y = goal.coordinates
    h = math.sqrt(((end_x - x) * (end_x - x)) + ((end_y - y) * (end_y - y)))
    return h

def getHValDiagonalDistance (x, y, goal):
    end_x, end_y = goal.coordinates
    h = max(abs(x - end_x), abs(y - end_y))
    return h

def getHValEuclideanDistance (x, y, goal):
    end_x, end_y = goal.coordinates
    h = sqrt(pow((x - end_x), 2) + pow((y - end_y), 2))
    return h  
    
def getHValCustom (x, y, goal, start):
    end_x, end_y = goal.coordinates
    begin_x, begin_y = start.coordinates
    stDistance = sqrt(pow(end_x - begin_x, 2) + pow(end_y - begin_y, 2))
    h = abs(stDistance - (sqrt(pow(x - start_x, 2) + pow(y - start_y, 2))))
    return h

def getHValManhattanDistance (x, y, goal):
    end_x, end_y = goal.coordinates
    h = abs(x - end_x) + abs(y - end_y)
    return h
# A* Search
# Start is a pair of coordinates for the start and end is a pair of coordinates for the end
def a_star(map, start, end):
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

    closed = [[False for j in range(120)] for i in range(160)]
    openList = []
    openList.append((0, (start.coordinates[0], start.coordinates[1])))

    while len(openList) > 0:
        (f, (x,y)) = openList.pop()
        closed[x][y] = True
        print(x, y)
        gNew = 0
        # North
        if isValid(x - 1, y):
            # Check if it's the Goal Cell
            if isDestination(x - 1, y, end):
                map[x - 1][y].parent_x = x
                map[x - 1][y].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            # If the vertex is blocked or already closed then ignore it
            elif not closed[x - 1][y] & map[x - 1][y].isBlocked() is False:
                # G value will differ depending on if the cell is hard to traverse or not
                # On a highway
                if map[x][y].code == '1':
                    if map[x - 1][y].code == '1' or map[x-1][y].code == 'a':
                        gNew = map[x][y].g + 1
                    if map[x - 1][y].code == '2' or map[x - 1][y].code == 'b':
                        gNew = map[x - 1][y].g + 1.5
                elif map[x][y].code == '2':
                    if map[x - 1][y].code == '1' or map[x-1][y].code == 'a':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                elif map[x][y].code == 'a':
                    if map[x - 1][y].code == 'a':
                        gNew = map[x][y].g + 0.25
                    elif map[x - 1][y].code == 'b':
                        gNew = map[x][y].g + 0.375
                    elif map[x - 1][y].code == '1':
                        gNew = map[x][y].g + 1
                    else:
                        gNew = map[x][y].g + 1.5
                else:
                    if map[x - 1][y].code == 'a':
                        gNew = map[x][y].g + 0.375
                    elif map[x-1][y].code == 'b':
                        gNew = map[x][y].g + 0.5
                    elif map[x-1][y].code == '1':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0


                hNew = getHValue(x - 1, y, end)
                fNew = gNew + hNew
                if map[x - 1][y].f > fNew:
                    openList.append((fNew, (x - 1, y)))
                    map[x - 1][y].f = fNew
                    map[x - 1][y].g = gNew
                    map[x - 1][y].h = hNew
                    map[x - 1][y].parent_x = x
                    map[x - 1][y].parent_y = y
        # South
        if isValid(x + 1, y):
            # Check if it's the destination
            if isDestination(x + 1, y, end):
                map[x + 1][y].parent_x = x
                map[x + 1][y].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif not closed[x + 1][y] & map[x + 1][y].isBlocked() is False:
                if map[x][y].code == '1':
                    if map[x + 1][y].code == '1' or map[x + 1][y].code == 'a':
                        gNew = map[x][y].g + 1
                    if map[x + 1][y].code == '2' or map[x + 1][y].code == 'b':
                        gNew = map[x + 1][y].g + 1.5
                elif map[x][y].code == '2':
                    if map[x + 1][y].code == '1' or map[x + 1][y].code == 'a':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                elif map[x][y].code == 'a':
                    if map[x + 1][y].code == 'a':
                        gNew = map[x][y].g + 0.25
                    elif map[x + 1][y].code == 'b':
                        gNew = map[x][y].g + 0.375
                    elif map[x + 1][y].code == '1':
                        gNew = map[x][y].g + 1
                    else:
                        gNew = map[x][y].g + 1.5
                else:
                    if map[x + 1][y].code == 'a':
                        gNew = map[x][y].g + 0.375
                    elif map[x + 1][y].code == 'b':
                        gNew = map[x][y].g + 0.5
                    elif map[x + 1][y].code == '1':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                hNew = getHValue(x + 1, y, end)
                fNew = gNew + hNew
                if map[x + 1][y].f > fNew:
                    openList.append((fNew, (x + 1, y)))
                    map[x + 1][y].f = fNew
                    map[x + 1][y].g = gNew
                    map[x + 1][y].h = hNew
                    map[x + 1][y].parent_x = x
                    map[x + 1][y].parent_y = y
        # East
        if isValid(x, y + 1):
            # Check if it's the destination
            if isDestination(x, y + 1, end):
                map[x][y + 1].parent_x = x
                map[x][y + 1].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif not closed[x][y + 1] & map[x][y + 1].isBlocked() is False:
                if map[x][y].code == '1':
                    if map[x][y + 1].code == '1' or map[x][y + 1].code == 'a':
                        gNew = map[x][y].g + 1
                    if map[x][y + 1].code == '2' or map[x][y + 1].code == 'b':
                        gNew = map[x][y].g + 1.5
                elif map[x][y].code == '2':
                    if map[x][y + 1].code == '1' or map[x][y + 1].code == 'a':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                elif map[x][y].code == 'a':
                    if map[x][y + 1].code == 'a':
                        gNew = map[x][y].g + 0.25
                    elif map[x][y + 1].code == 'b':
                        gNew = map[x][y].g + 0.375
                    elif map[x][y + 1].code == '1':
                        gNew = map[x][y].g + 1
                    else:
                        gNew = map[x][y].g + 1.5
                else:
                    if map[x][y + 1].code == 'a':
                        gNew = map[x][y].g + 0.375
                    elif map[x][y + 1].code == 'b':
                        gNew = map[x][y].g + 0.5
                    elif map[x][y + 1].code == '1':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                hNew = getHValue(x, y + 1, end)
                fNew = gNew + hNew
                if map[x][y + 1].f > fNew:
                    openList.append((fNew, (x, y + 1)))
                    map[x][y + 1].f = fNew
                    map[x][y + 1].g = gNew
                    map[x][y + 1].h = hNew
                    map[x][y + 1].parent_x = x
                    map[x][y + 1].parent_y = y
        # West
        if isValid(x, y - 1):
            # Check if it's the destination
            if isDestination(x, y - 1, end):
                map[x][y + 1].parent_x = x
                map[x][y + 1].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif not closed[x][y - 1] & map[x][y - 1].isBlocked() is False:
                if map[x][y].code == '1':
                    if map[x][y - 1].code == '1' or map[x][y - 1].code == 'a':
                        gNew = map[x][y].g + 1
                    if map[x][y - 1].code == '2' or map[x][y - 1].code == 'b':
                        gNew = map[x][y].g + 1.5
                elif map[x][y].code == '2':
                    if map[x][y - 1].code == '1' or map[x][y - 1].code == 'a':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                elif map[x][y].code == 'a':
                    if map[x][y - 1].code == 'a':
                        gNew = map[x][y].g + 0.25
                    elif map[x][y - 1].code == 'b':
                        gNew = map[x][y].g + 0.375
                    elif map[x][y - 1].code == '1':
                        gNew = map[x][y].g + 1
                    else:
                        gNew = map[x][y].g + 1.5
                else:
                    if map[x][y - 1].code == 'a':
                        gNew = map[x][y].g + 0.375
                    elif map[x][y - 1].code == 'b':
                        gNew = map[x][y].g + 0.5
                    elif map[x][y - 1].code == '1':
                        gNew = map[x][y].g + 1.5
                    else:
                        gNew = map[x][y].g + 2.0
                hNew = getHValue(x, y - 1, end)
                fNew = gNew + hNew
                if map[x][y - 1].f > fNew:
                    openList.append((fNew, (x, y - 1)))
                    map[x][y - 1].f = fNew
                    map[x][y - 1].g = gNew
                    map[x][y - 1].h = hNew
                    map[x][y - 1].parent_x = x
                    map[x][y - 1].parent_y = y

        # North-East
        if isValid(x - 1, y + 1):
            # Check if it's the destination
            if isDestination(x - 1, y + 1, end):
                map[x - 1][y + 1].parent_x = x
                map[x - 1][y + 1].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif closed[x - 1][y + 1] is False and map[x - 1][y + 1].code != '0':
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x - 1][y + 1].code == 'a' or map[x - 1][y + 1] == '1':
                        gNew = map[x][y].g + math.sqrt(2)
                    else:
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x - 1][y + 1].code == 'a' or map[x - 1][y + 1] == '1':
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        gNew = map[x][y].g + math.sqrt(8)

                hNew = getHValue(x - 1, y + 1, end)
                fNew = gNew + hNew
                if map[x - 1][y + 1].f > fNew:
                    openList.append((fNew, (x - 1, y + 1)))
                    map[x - 1][y + 1].f = fNew
                    map[x - 1][y + 1].g = gNew
                    map[x - 1][y + 1].h = hNew
                    map[x - 1][y + 1].parent_x = x
                    map[x - 1][y + 1].parent_y = y
        # North West
        if isValid(x - 1, y - 1):
            # Check if it's the destination
            if isDestination(x - 1, y - 1, end):
                map[x - 1][y - 1].parent_x = x
                map[x - 1][y - 1].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif closed[x - 1][y - 1] is False and map[x - 1][y - 1].code != '0':
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x - 1][y - 1].code == 'a' or map[x - 1][y - 1] == '1':
                        gNew = map[x][y].g + math.sqrt(2)
                    else:
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x - 1][y - 1].code == 'a' or map[x - 1][y - 1] == '1':
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        gNew = map[x][y].g + math.sqrt(8)
                hNew = getHValue(x - 1, y - 1, end)
                fNew = gNew + hNew
                if map[x - 1][y - 1].f > fNew:
                    openList.append((fNew, (x - 1, y - 1)))
                    map[x - 1][y - 1].f = fNew
                    map[x - 1][y - 1].g = gNew
                    map[x - 1][y - 1].h = hNew
                    map[x - 1][y - 1].parent_x = x
                    map[x - 1][y - 1].parent_y = y

        # South-East
        if isValid(x + 1, y + 1):
            # Check if it's the destination
            if isDestination(x + 1, y + 1, end):
                map[x + 1][y + 1].parent_x = x
                map[x + 1][y + 1].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif closed[x + 1][y + 1] is False and map[x + 1][y + 1].code != '0':
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x + 1][y + 1].code == 'a' or map[x + 1][y + 1] == '1':
                        gNew = map[x][y].g + math.sqrt(2)
                    else:
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x + 1][y + 1].code == 'a' or map[x + 1][y + 1] == '1':
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        gNew = map[x][y].g + math.sqrt(8)
                hNew = getHValue(x + 1, y + 1, end)
                fNew = gNew + hNew
                if map[x + 1][y + 1].f > fNew:
                    openList.append((fNew, (x + 1, y + 1)))
                    map[x + 1][y + 1].f = fNew
                    map[x + 1][y + 1].g = gNew
                    map[x + 1][y + 1].h = hNew
                    map[x + 1][y + 1].parent_x = x
                    map[x + 1][y + 1].parent_y = y
        # South-West
        if isValid(x + 1, y - 1):
            # Check if it's the destination
            if isDestination(x + 1, y - 1, end):
                map[x + 1][y - 1].parent_x = x
                map[x + 1][y - 1].parent_y = y
                print("Destination Found")
                trace(map, end)
                return
            elif closed[x + 1][y - 1] is False and map[x + 1][y - 1].code != '0':
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x + 1][y - 1].code == 'a' or map[x + 1][y - 1] == '1':
                        gNew = map[x][y].g + math.sqrt(2)
                    else:
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x + 1][y - 1].code == 'a' or map[x + 1][y - 1] == '1':
                        gNew = map[x][y].g + (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        gNew = map[x][y].g + math.sqrt(8)
                hNew = getHValue(x + 1, y - 1, end)
                fNew = gNew + hNew
                if map[x + 1][y - 1].f > fNew:
                    openList.append((fNew, (x + 1, y - 1)))
                    map[x + 1][y - 1].f = fNew
                    map[x + 1][y - 1].g = gNew
                    map[x + 1][y - 1].h = hNew
                    map[x + 1][y - 1].parent_x = x
                    map[x + 1][y - 1].parent_y = y
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
        print("Loop")
        (f, (x, y)) = queue.get()
        closed[x][y] = True
        if isDestination(x, y, end):
            print("Destination Found")
            trace(map, end)
            return
        if isValid(x - 1, y):
            if closed[x - 1][y] is False and map[x - 1][y].isBlocked() is False:
                if map[x][y].code == '1':
                    if map[x - 1][y] == '1' or map[x-1][y] == 'a':
                        cost = 1
                    else:
                        cost = 1.5
                elif map[x][y].code == 'a':
                    if map[x - 1][y] == '1':
                        cost = 1
                    elif map[x - 1][y] == 'a':
                        cost = 0.25
                    elif map[x - 1][y] == '2':
                        cost = 1.5
                    else:
                        cost = 0.375
                elif map[x][y].code == '2':
                    if map[x-1][y] == '1' or map[x-1][y] == 'a':
                        cost = 1.5
                    else:
                        cost = 2
                else:
                    if map[x - 1][y] == '1':
                        cost = 1.5
                    elif map[x - 1][y] == 'a':
                        cost = 0.375
                    elif map[x - 1][y] == '2':
                        cost = 2
                    else:
                        cost = 0.5
                map[x - 1][y].parent_x = x
                map[x - 1][y].parent_y = y
                queue.put((cost, (x - 1, y)))
        if isValid(x + 1, y):
            if closed[x + 1][y] is False and map[x + 1][y].isBlocked() is False:
                cost = 0
                if map[x][y].code == '1':
                    if map[x + 1][y] == '1' or map[x + 1][y] == 'a':
                        cost = 1
                    else:
                        cost = 1.5
                elif map[x][y].code == 'a':
                    if map[x + 1][y] == '1':
                        cost = 1
                    elif map[x + 1][y] == 'a':
                        cost = 0.25
                    elif map[x + 1][y] == '2':
                        cost = 1.5
                    else:
                        cost = 0.375
                elif map[x][y].code == '2':
                    if map[x + 1][y] == '1' or map[x + 1][y] == 'a':
                        cost = 1.5
                    else:
                        cost = 2
                else:
                    if map[x + 1][y] == '1':
                        cost = 1.5
                    elif map[x + 1][y] == 'a':
                        cost = 0.375
                    elif map[x + 1][y] == '2':
                        cost = 2
                    else:
                        cost = 0.5
                map[x + 1][y].parent_x = x
                map[x + 1][y].parent_y = y
                queue.put((cost, (x + 1, y)))

        if isValid(x, y + 1):
            if closed[x][y + 1] is False and map[x][y + 1].isBlocked() is False:
                if map[x][y].code == '1':
                    if map[x][y + 1] == '1' or map[x][y + 1] == 'a':
                        cost = 1
                    else:
                        cost = 1.5
                elif map[x][y].code == 'a':
                    if map[x][y + 1] == '1':
                        cost = 1
                    elif map[x][y + 1] == 'a':
                        cost = 0.25
                    elif map[x][y + 1] == '2':
                        cost = 1.5
                    else:
                        cost = 0.375
                elif map[x][y].code == '2':
                    if map[x][y + 1] == '1' or map[x][y + 1] == 'a':
                        cost = 1.5
                    else:
                        cost = 2
                else:
                    if map[x][y + 1] == '1':
                        cost = 1.5
                    elif map[x][y + 1] == 'a':
                        cost = 0.375
                    elif map[x][y + 1] == '2':
                        cost = 2
                    else:
                        cost = 0.5
                map[x][y + 1].parent_x = x
                map[x][y + 1].parent_y = y
                queue.put((cost, (x, y + 1)))

        if isValid(x, y - 1):
            if closed[x][y - 1] is False and map[x][y - 1].isBlocked() is False:
                cost = 0
                if map[x][y].code == '1':
                    if map[x][y - 1] == '1' or map[x][y - 1] == 'a':
                        cost = 1
                    else:
                        cost = 1.5
                elif map[x][y].code == 'a':
                    if map[x][y - 1] == '1':
                        cost = 1
                    elif map[x][y - 1] == 'a':
                        cost = 0.25
                    elif map[x][y - 1] == '2':
                        cost = 1.5
                    else:
                        cost = 0.375
                elif map[x][y].code == '2':
                    if map[x][y - 1] == '1' or map[x][y - 1] == 'a':
                        cost = 1.5
                    else:
                        cost = 2
                else:
                    if map[x][y - 1] == '1':
                        cost = 1.5
                    elif map[x][y - 1] == 'a':
                        cost = 0.375
                    elif map[x][y - 1] == '2':
                        cost = 2
                    else:
                        cost = 0.5
                map[x][y - 1].parent_x = x
                map[x][y - 1].parent_y = y
                queue.put((cost, (x, y - 1)))
        if isValid(x - 1, y + 1):
            if closed[x - 1][y + 1] is False and map[x - 1][y + 1].isBlocked() is False:
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x - 1][y + 1].code == 'a' or map[x - 1][y + 1]:
                        cost = math.sqrt(2)
                    else:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x - 1][y + 1].code == 'a' or map[x - 1][y + 1]:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        cost = math.sqrt(8)
                map[x - 1][y + 1].parent_x = x
                map[x - 1][y + 1].parent_y = y
                queue.put((cost, (x - 1, y + 1)))
        if isValid(x - 1, y - 1):
            if closed[x - 1][y - 1] is False and map[x - 1][y - 1].isBlocked() is False:
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x - 1][y - 1].code == 'a' or map[x - 1][y - 1]:
                        cost = math.sqrt(2)
                    else:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x - 1][y - 1].code == 'a' or map[x - 1][y - 1]:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        cost = math.sqrt(8)
                map[x - 1][y - 1].parent_x = x
                map[x - 1][y - 1].parent_y = y
                queue.put((cost, (x - 1, y - 1)))
        if isValid(x + 1, y + 1):
            if closed[x + 1][y + 1] is False and map[x + 1][y + 1].isBlocked() is False:
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x + 1][y + 1].code == 'a' or map[x + 1][y + 1]:
                        cost = math.sqrt(2)
                    else:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x + 1][y + 1].code == 'a' or map[x + 1][y + 1]:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        cost = math.sqrt(8)
                map[x + 1][y + 1].parent_x = x
                map[x + 1][y + 1].parent_y = y
                queue.put((cost, (x + 1, y + 1)))
        if isValid(x + 1, y - 1):
            if closed[x + 1][y - 1] is False and map[x + 1][y - 1].isBlocked() is False:
                if map[x][y].code == 'a' or map[x][y].code == '1':
                    if map[x + 1][y - 1].code == 'a' or map[x + 1][y - 1]:
                        cost = math.sqrt(2)
                    else:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                else:
                    if map[x + 1][y - 1].code == 'a' or map[x + 1][y - 1]:
                        cost = (math.sqrt(2) + math.sqrt(8)) / 2
                    else:
                        cost = math.sqrt(8)
                map[x + 1][y - 1].parent_x = x
                map[x + 1][y - 1].parent_y = y
                queue.put((cost, (x + 1, y - 1)))
    print("Failed to find the goal")
    return