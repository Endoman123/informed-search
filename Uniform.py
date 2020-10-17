from queue import PriorityQueue

import ai


def uniform_search(map, start, end):
    if ai.isValid(start[1], start[0]) is False:
        print("Invalid Start")
        return
    if ai.isValid(end[1], end[0]) is False:
        print("Invalid End")
        return
    
    if (map[start[1]][start[0]].isBlocked() | map[end[1]][end[0]].isBlocked()):
        print(map[start[1]][start[0]].isBlocked())
        print("Blocked Node Chosen")
        return
    queue = PriorityQueue()
    queue.put((0, start))
    #parent = {i: {j: None for j in range(len(map[0]))} for i in range(len(map))}
    closed = [[False for j in range(120)] for i in range(160)]
    while not queue.empty():
        (f, (y, x)) = queue.get()
        closed[x][y] = True
        if ai.isDestination(x, y, end):
            #ai.trace(map, end)
            print("Path found")
            return
        for i in range(max(0, x - 1), min(len(map), x + 2)):
            print("first for")
            for j in range(max(0, y - 1), min(len(map[0]), y + 2)):
                if ai.isValid(x + i, y + j) and closed[x + i][y + j] is False and map[x + i][
                    y + j].isBlocked() is False:
                    print("first if")
                    if x == j | y == i:
                        cost = ai.get_cost_diagonal(x, y, x + i, y + j, map)
                        map[x + i][y + j].parent_x = x
                        map[x + i][y + j].parent_y = y
                        queue.put((cost, (x + i, y + j)))
    
    print("Failed to find the goal")
    return

#just me tryinng to do my own version, don't worry about this
def uniform_cost_search(map, start, goal):
    if ai.isValid(start[1], start[0]) is False:
        print("Invalid Start")
        return
    if ai.isValid(end[1], end[0]) is False:
        print("Invalid End")
        return
    
    if (map[start[1]][start[0]].isBlocked() | map[end[1]][end[0]].isBlocked()):
        print(map[start[1]][start[0]].isBlocked())
        print("Blocked Node Chosen")
        return
    
    path = PriorityQueue()
    closed = []
    path.put(0, start)
    
    while not path.empty():
        cost, (y, x) = path.get()
        current = (x, y)
        closed.append(current)
        
        if (ai.isDestination(x, y, goal)):
            print("Found goal")
            return
        
        
        
        
