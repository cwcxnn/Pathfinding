def draw_S(grid, x, y):
    for i in range(0, 3):
        grid[x+i][y].blocked = True
        grid[x+i][y+2].blocked = True
        grid[x+i][y+4].blocked = True
    for i in range(0, 3):
        grid[x][y+i].blocked = True
        grid[x+2][y+2+i].blocked = True  

def draw_P(grid, x, y):
    for i in range(0, 3): # draws the top 'box' of the P
        grid[x+i][y].blocked = True
        grid[x+i][y+2].blocked = True
        grid[x+2][y+i].blocked = True
    for i in range(0, 5): # draws the back/stem of the P
        grid[x][y+i].blocked = True

def draw_A(grid, x, y):
    for i in range(0, 3): # draws top and middle horizontal lines to draw A
        grid[x+i][y].blocked = True
        grid[x+i][y+2].blocked = True
    for i in range(0, 5): # draws the two verticle lines of the A
        grid[x][y+i].blocked = True 
        grid[x+2][y+i].blocked = True

def draw_C(grid, x, y):
    for i in range(0, 3):
        grid[x+i][y].blocked = True
        grid[x+i][y+4].blocked = True
    for i in range(0, 5):
        grid[x][y+i].blocked = True

def draw_E(grid, x, y):
    for i in range(0, 3):
        grid[x+i][y].blocked = True
        grid[x+i][y+2].blocked = True
        grid[x+i][y+4].blocked = True
    for i in range(0, 5):
        grid[x][y+i].blocked = True   

def draw_R(grid, x, y):
    for i in range(0, 3):
        grid[x+i][y].blocked = True
    for i in range(0, 5):
        grid[x][y+i].blocked = True
    grid[x+2][y+1].blocked = True
    grid[x+1][y+2].blocked = True
    grid[x+2][y+3].blocked = True
    grid[x+2][y+4].blocked = True


