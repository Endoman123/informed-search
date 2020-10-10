import random

random.seed()

# Vertex represents one cell in the terrain
# As per the spec in the assignment, terrain is marked with a character 
# - 0: blocked
# - 1: unblockd
# - 2: hard to traverse
# - a: unblocked highway
# - b: hard to traverse highway
# Helper methods are provided to make getting info easier, as well as highway marking
class Vertex:
    code = '1'
    f = -1
    g = -1
    h = -1
    parent = None

    def __init__(self, c):
        self.code = c

    def isHighway(self):
        return self.code == 'a' or self.code == 'b'
    
    def isBlocked(self):
        return self.code == '0'

    def isUnblocked(self):
        return self.code == '1' or self.code == 'a'

    def isHardToTraverse(self):
        return self.code == '2' or self.code == 'b'

    def markHighway(self):
        if self.code == '0':
            raise Exception("Blocked, cannot set to highway")
        elif self.code == '1':
            self.code = 'a'
        elif self.code == '2':
            self.code = 'b'
    
    def unmarkHighway(self):
        if self.code == 'a':
            self.code = '1'
        elif self.code == 'b':
            self.code = '2' 

    def __repr__(self): 
        return f"{self.code}"

# Init terrain as follows:
# - Define a grid map 1 cell bigger with all blocked cells
# - Create a slice within the map that represents the inner area; modify this slice only
# - Select 8 random regions to be partially blocked
# - Create 4 highways
# - Select 20% of the total number of cells to be blocked cells
# For more information, see section 2 of assignment.pdf
def init_terrain(rows = 160, cols = 120):
    # Save total number of cells for later use
    size = rows * cols
    
    # Initialize cells to be blocked 
    ret = [[Vertex('0') for _ in range(cols + 2)] for _ in range(rows + 2)] 
 
    # Select the internal section to be unblocked.
    # We will modify this map.
    t = [[ret[i][j] for j in range(1, cols + 1)] for i in range(1, rows + 1)]
    for row in t:
        for v in row:
            v.code = '1'    
 
    # Select random partially blocked cells 
    for _ in range(8):
        x = random.randint(0, cols - 1)    
        y = random.randint(0, rows - 1)
    
        t_slice = t[y - 15:y + 15][x - 15:x + 15]  
        
        for row in t_slice:
            for v in row:
                v.code = random.choice(['1', '2'])
    
    # Create "highways"
    # NOTE: Assume after 10 tries that highways cannot be generated given the current config
    # 
    # 1 - Pick someplace on the edge
    # 2 - Pick a random direction
    # 3 - Push tile to list
    # 4 - Move in direction
    # 5 - Check if tile is a valid tile, if not break
    # 6 - Loop back to #3 19 more times
    # 7 - If 20 tiles have just been pushed to list, 60% chance of choosing a new direction, 20% of each perpendicular direction
    # 8 - Check number of tiles and stopping point. If both are valid, mark
    #     as a success, commit all as highway, and move on to the next one 
    n_highways = 0 
    while n_highways < 4:
        x = -1
        y = -1
        success = False 
        list_v = []        
        n_tries = 10
        
        while not success:
            # Choose side pair 
            if bool(random.getrandbits(1)): 
                x = random.randint(0, cols - 1)
                y = random.choice([0, rows - 1])
            else: 
                x = random.choice([0, cols - 1]) 
                y = random.randint(0, rows - 1)

            end = False 
            c_dir = random.randint(0, 3)
            
            while not end: 
                for _ in range(20):
                    list_v.append(t[y][x])
                    
                    if c_dir == 0:
                        y -= 1
                    elif c_dir == 1:
                        x -= 1
                    elif c_dir == 2:
                        y += 1
                    else:
                        c_dir = 3
                        x += 1

                    if x < 0 or x >= cols or y < 0 or y >= rows or t[y][x].isHighway():
                        end = True 
                        break

                if not end:
                    c_dir = (c_dir + random.choice([0, 0, 0, 1, 3])) % 4

            if len(list_v) >= 100 and not list_v[len(list_v) - 1].isHighway(): 
                for v in list_v:
                    v.markHighway() 
                success = True
                n_highways += 1
            else:
                n_tries -= 1
                
                if n_tries == 0:
                    n_highways = 0

                    for row in t:
                        for v in row:
                            v.unmarkHighway()         

    # Generate "walls"       
    for _ in range(size):
        v = None 
        while True:
            v = t[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            if not v.isHighway():
                break

        v.code = '0' 
 
    return ret 

terrain = init_terrain()
