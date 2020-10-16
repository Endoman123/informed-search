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


def getHValManhattanDistanceHex (x, y, goal):
    end_x, end_y = goal.coordinates
    dx = end_x - x
    dy = end_y - y
    h = abs(dx + dy) / 2
    return h  



def getHValCustom(x, y, goal, start):
    end_x, end_y = goal.coordinates
    begin_x, begin_y = start.coordinates
    stDistance = sqrt(pow(end_x - begin_x, 2) + pow(end_y - begin_y, 2))
    h = abs(stDistance - (sqrt(pow(x - begin_x, 2) + pow(y - begin_y, 2))))
    return h


def getHValManhattanDistance(x, y, goal):
    end_x, end_y = goal.coordinates
    h = abs(x - end_x) + abs(y - end_y)
    return h

def isAdmissible (hCur, hParent, cost):
    return hParent <= cost + hCur


def mark_destination(x, y, x_new, y_new, map):
    map[x_new][y_new].parent_x = x
    map[x_new][y_new].parent_y = y
    trace(map, map[x_new][y_new])
    return

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
