import random

random.seed()

# Vertex represents one cell in the terrain
# Difficulty ranges from 0 to 2, 0 representing unblocked, 2 representing fully blocked
# Direction represents the acceleration direction (if applicable);
# this ranges from 0 to 4, 0 being undefined, and 1-4 being NWSE, respectively.
class Vertex:
    difficulty = 0
    direction = 0
    f = -1
    g = -1
    h = -1
    parent = None

    def __repr__(obj):
        return f"({obj.difficulty}, {obj.direction})"

# Init terrain as follows:
# - Define a grid map with all unblocked cells
# - Select 8 random regions to be partially blocked
# - Create 4 highways
# - Select 20% of the total number of cells to be blocked cells
# For more information, see section 2 of assignment.pdf
def init_terrain(rows = 160, cols = 120):
    # Save total number of cells for later use
    size = rows * cols

    # Initialize cells to be unblocked 
    t = [[Vertex() for _ in range(cols)] for _ in range(rows)] 
   
    # Select random partially blocked cells 
    for _ in range(8):
        x = random.randint(0, cols - 1)    
        y = random.randint(0, rows - 1)
    
        t_slice = t[y - 15:y + 15][x - 15:x + 15]  

        for row in t_slice:
            for v in row:
                v.difficulty = random.randint(0, 1)
       
    # Create "highways"
    for _ in range(4):
        x = -1
        y = -1
        success = False 
        list_v = []        

        while not success:
            # Choose side pair 
            if bool(random.getrandbits(1)): 
                x = random.randint(0, cols - 1)
                y = random.choice([0, rows - 1])
            else: 
                x = random.choice([0, cols - 1]) 
                y = random.randint(0, rows - 1)

            state = 0
            n_v = 0 
            
            # Highway state machine
            while 
                c_dir = random.randint(1, 4)
                
                t[x][y].direction = c_dir

                list_v.append(t[x][y])
                n_v++ 

                if n_v < 20
                    if c_dir == 1:
                        y--
                    elif c_dir == 2:
                        x--
                    elif c_dir == 3:
                        y++
                    else:
                        c_dir = 4
                        x++             
       
    # Generate "walls"       
    for _ in range(size):
        v = None 
        while True:
            v = t[random.randint(0, rows - 1)][random.randint(0, cols - 1)]
            if v.direction == 0:
                break

        v.difficulty = 2 
 
    return t 

terrain = init_terrain()
print(terrain)
