import math
import random
import sys
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

import pygame
from pygame.constants import K_SPACE, K_f, K_r

import Alphabet

w = 500 # window width
r = 25 # number of rows
c = 25 # number of columns
cell_width =  w//c # width of each cell = window width // number of

grid = []
queue = []
closedset = []
path = []

window = pygame.display.set_mode((w, w))
pygame.display.set_caption("Pathfinder.")
logo = pygame.image.load('Assets\search.png')
pygame.display.set_icon(logo)

class SecondaryWindow(Tk):

    blank = False
    mine_field = False
    maze = False

    Dijkstra = False
    Astar = False

    def __init__(self):
        super().__init__()

        self.title('Generation: Settings')
        self.geometry('325x164+375+258')
        icon = PhotoImage(file = 'Assets\setting.png')
        self.iconphoto(False, icon)
        self.t = StringVar()
        self.a = StringVar()

        tabControl = Notebook(self)
        tab1 = Frame(tabControl)
        tab2 = Frame(tabControl)
        tabControl.add(tab1, text='Start')
        tabControl.add(tab2, text='Settings')
        tabControl.pack(expand=1, fill="both")

        #            tab 1: info/help
        f=Frame(tab1) # creates a frame to contain widgets
        # heading label
        Label(f, text='Help: Information', font=(None,'10', 'bold')).grid(row=0, column=0, columnspan=2, pady=10) 
        # label corresponding to tutorial
        Label(f, text='Set-up:').grid(row=2, column=0, sticky=W, pady=5)
        # button to show tutorial window
        Button(f, text='-open-', width=15, command=self.show_tutorial).grid(row=2, column=1, sticky=E) 
        # label corresponding to controls
        Label(f, text='Controls:').grid(row=3, column=0, sticky=W) 
        # button that shows controls
        Button(f, text='-open-', width=15, command=self.show_controls).grid(row=3, column=1, sticky=E) 
        # shows info on  pathfinding
        Button(f, text='Pathfinding', width=30, command=self.show_info).grid(row=4, column=0, columnspan=2, pady=10) 
        f.pack()  # places frame on the screen   

        #           tab 2: settings
        f2=Frame(tab2)
        # heading label
        Label(f2, text='Configure Settings', font=(None,'10', 'bold')).grid(row=0, column=0, columnspan=2, pady=10) 
        Label(f2, text='Terrain:').grid(row=2, column=0, sticky=W, pady=5) # terrain label 
        terrains = [             # list of generation algorithms
            "Terrains..",
            "Blank",
            "Mine Field",
            "Pre-Made Maze"
        ]
        OptionMenu(f2, self.t, *terrains).grid(row=2, column=1, sticky=E) # terrain dropdown
        Label(f2, text='Finding:').grid(row=3, column=0, sticky=W)
        Button(f2, text='Open Grid', width=30, command=self.open_grid).grid(row=4, column=0, columnspan=2, pady=10)
        search_algos = [             # list of generation algorithms
            "Algorithms..",
            "A*",
            "Dijkstra"
        ]
        OptionMenu(f2, self.a, *search_algos).grid(row=3, column=1, sticky=E) # pathfinding algorithm dropdown
        f2.pack()

    def open_grid(self): # initialises pygame window with configurations defined in tkinter window 
        terrain = self.t.get()
        algo = self.a.get()
        if terrain == 'Terrains..' or algo == 'Algorithms..':
            messagebox.showwarning('Terrain or Algorithm not selected.','You need to select a Terrain and an Algorithm before continuing.')
        else:
            if terrain == 'Blank':
                SecondaryWindow.blank = True
            if terrain == 'Mine Field':
                SecondaryWindow.mine_field = True   # random generation has been picked
            if terrain == 'Pre-Made Maze':
                SecondaryWindow.maze = True
            
            if algo == 'A*':
                SecondaryWindow.Astar = True
            if algo == 'Dijkstra':
                SecondaryWindow.Dijkstra = True
            PrimaryWindow()

    def show_controls(self):
        messagebox.showinfo("Controls:",
        "    SPACE: generate your selected terrain\n            F: begin the search\n            R: clean the grid\n Left Click: place target\nRight Click: place blockade")

    def show_tutorial(self):
        messagebox.showinfo("Tutorial:",
        "Select a terrain and algorithm from the drop down within the settings tab. These will correspond to the map generated and what path finding algorithm will be used.\n\nOnce selected, click 'open grid' to generate the map.\nPress 'SPACE' to begin, Left Click to place a target, Right Click to block cells, and 'F' to begin the solution.\n\nView the settings tab to begin.")

    def show_info(self):
        infowin = Toplevel() # creates another window - different from Tk() 
        # Tk() window cannot call itself within its own class
        infowin.geometry('325x300+375+455') # dimension and placement
        icon = PhotoImage(file = 'Assets\info.png') # get image
        infowin.iconphoto(False, icon) # adds window icon
        infowin.title('Algorithms: Info') # title of window
        Label(infowin, text='T')

        f=Frame(infowin) # creates a frame to contain widgets
        # heading label
        Label(f, text='Terrain Generation', font=(None,'10', 'bold')).grid(row=0, column=0, columnspan=2, pady=10) 
        Label(f, text='Mine Field:').grid(row=2, column=0, sticky=W, pady=1)
        Button(f, text='-open-', width=15, command=self.explain_mine_field).grid(row=2, column=1, sticky=E) 
        Label(f, text='Maze:').grid(row=3, column=0, sticky=W) 
        Button(f, text='-open-', width=15, command=self.explain_maze).grid(row=3, column=1, sticky=E) 
        f.pack()  # places frame on the screen 

        f2=Frame(infowin) # creates a frame to contain widgets
        # heading label
        Label(f2, text='Pathfinding', font=(None,'10', 'bold')).grid(row=0, column=0, columnspan=2, pady=10) 
        Label(f2, text='Dijkstra:').grid(row=2, column=0, sticky=W, pady=5)
        Button(f2, text='-open-', width=15, command=self.explain_dijkstra).grid(row=2, column=1, sticky=E) 
        Label(f2, text='A*:').grid(row=3, column=0, sticky=W) 
        Button(f2, text='-open-', width=15, command=self.explain_astar).grid(row=3, column=1, sticky=E) 
        f2.pack()  # places frame on the screen 
    
    def explain_mine_field(self):
        messagebox.showinfo("Mine Field:",
        "mine field info")
    def explain_maze(self):
        messagebox.showinfo("Maze:",
        "maze info")

    def explain_dijkstra(self):
        messagebox.showinfo("Dijkstra's Algorithm:",
        "dijkstra's info")
    def explain_astar(self):
        messagebox.showinfo("A* Algorithm:",
        "a* info")

class Cell:

    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.f, self.g, self.h = 0, 0, 0
        self.start = False
        self.blocked = False
        self.end =  False
        self.queued = False
        self.visited = False
        self.neighbours = [] # neighbours of the cell (for search algorithm)
        self.prior = None # prior is the cell that caused this cell to be set as a neighbour
    
    def draw(self, win, colour, shape=1):
        if shape == 1:
            pygame.draw.rect(
                win, colour,(
                    self.x * cell_width, self.y * cell_width, cell_width - 1, cell_width - 1))
        else:
            pygame.draw.circle(
                win, colour, (
                    self.x * cell_width + cell_width // 2, self.y * cell_width + cell_width // 2), cell_width // 3)

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(grid[self.x - 1][self.y]) # adds horizontal neighbouring cells to an array
        if self.x < c - 1:
            self.neighbours.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(grid[self.x][self.y - 1]) # adds horizontal neighbouring cells to an array
        if self.y < r - 1:
            self.neighbours.append(grid[self.x][self.y + 1])

class PrimaryWindow:

    def __init__(self):
        global start_cell

        for i in range(c): # creates grid
            arr = []
            for j in range(r):
                arr.append(Cell(i, j))
            grid.append(arr) # filled grid with instances of Cell

        for i in range(c):
            for j in range(r):
                grid[i][j].set_neighbours() # iterates through grid ans finds/sets neighbours for each cell
        start_cell = grid[1][1]
        start_cell.start = True
        start_cell.visited = True
        queue.append(start_cell) 
    
        Alphabet.draw_P(grid,3,3)
        Alphabet.draw_R(grid,7,3)
        Alphabet.draw_E(grid,11,3)
        Alphabet.draw_S(grid,15,3)
        Alphabet.draw_S(grid,19,3) 

        Alphabet.draw_S(grid,3,9)
        Alphabet.draw_P(grid,7,9)
        Alphabet.draw_A(grid,11,9)
        Alphabet.draw_C(grid,15,9)
        Alphabet.draw_E(grid,19,9)
        main()

    def get_clicked_position(pos, rows, width):
        gap = width // rows
        y,x = pos
        row = y // gap
        col = x // gap
        return row, col
    
    def clean(): # cleans the grid
        for row in grid: 
            for cell in row:
                cell.blocked = False # aso used for generating 'Blank' terrain

    def place_mines():
        PrimaryWindow.clean()
        for row in grid:
            for cell in row:
                if random.randint(0, 100) < 20:
                    if cell.start == False and cell.end == False:
                        cell.blocked = True
    def draw_maze():
        PrimaryWindow.clean()
        maze = [
            '1111111111111111111111111',
            '1000010000000100001100011', 
            '1111000110110101100001011',
            '1000010010010000101111011',
            '1010111011110110101000001',
            '1000000000000100101010101',
            '1011111010111111011000101',
            '1000001010000001010011101',
            '1111011011110111010110001',
            '1000001010000000010100111',
            '1110100010111110110101101',
            '1000101010100000000101001',
            '1010101010101111111100011',
            '1010101000101010000001011',
            '1010101010100010110111011',
            '1010101000101010100001011',
            '1010101010101010111111011',
            '1001101010101000100001011',
            '1111001010101010111111011',
            '1000011010101110100000001',
            '1111111110101000101111101',
            '1000000000101011100000001',
            '1011101111101010001011101',
            '1010000000001010111000001',
            '1111111111111111111111111'
        ]       
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                c = maze[x][y]
                if c == '1':
                    grid[x][y].blocked = True
                if c == '0':
                    pass        
    def reset():
        for row in grid:
            for cell in row:
                cell.blocked = False
                cell.queued = False
                cell.visited = False
                cell.path = False
                cell.blocked = False
                cell.end = False


def heuristics(a, b):
    return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)

def main():

    end_selected = False
    end_cell = None
    searching = True
    clicked = 0 
    terrain_generated = False
    run_astar = False
    run_dijkstra = False
    flag = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif pygame.mouse.get_pressed()[0] == True and terrain_generated:
                pos = pygame.mouse.get_pos()
                i, j = PrimaryWindow.get_clicked_position(pos, r, w)
                grid[i][j].blocked = True
            elif pygame.mouse.get_pressed()[2] and terrain_generated: # set target/end position
                pos = pygame.mouse.get_pos()
                i, j = PrimaryWindow.get_clicked_position(pos, r, w)
                if not end_selected:
                    end_cell = grid[i][j]
                    end_cell.blocked = False # allows user to select blocked cells as an end cell. otherwise, the algorithm will ignore the end cell as blocked = True
                    end_cell.end = True
                    end_selected = True
                else:
                    cell = grid[i][j]
                    cell.blocked = False

            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE: # starts algorithm
                    terrain_generated = True
                    clicked += 1
                    if clicked == 1:
                        if SecondaryWindow.blank == True:
                            PrimaryWindow.clean()
                        if SecondaryWindow.mine_field == True:
                            PrimaryWindow.place_mines()
                        if SecondaryWindow.maze == True:
                            PrimaryWindow.draw_maze()
                if event.key == K_r:
                    path.clear()
                    queue.clear()
                    closedset.clear()
                    queue.append(start_cell)
                    PrimaryWindow.reset()
                    main()
                if event.key == K_f and end_selected:
                    if SecondaryWindow.Astar == True:
                        run_astar = True
                    if SecondaryWindow.Dijkstra == True:
                        run_dijkstra = True
        if run_dijkstra:
            if len(queue) > 0 and searching: # len(queue) = 1 [start_cell appended earlier]
                current_cell = queue.pop(0) # start_cell = current_cell
                current_cell.visited = True # start_cell set to visited
                if current_cell == end_cell: 
                    searching = False # search is over, target cell found.
                    while current_cell.prior != start_cell: 
                        path.append(current_cell.prior)
                        current_cell = current_cell.prior   # draws path back to start_cell 
                else:
                    for neighbour in current_cell.neighbours:   # searching algorithm
                        if not neighbour.queued and not neighbour.blocked:
                            neighbour.queued = True
                            neighbour.prior = current_cell
                            queue.append(neighbour)
            else:
                if searching: # if still searching even though the search algorithm is done,
                    Tk().wm_withdraw()
                    messagebox.showerror("No Solution", "There Is No Solution!")
                    searching = False # stop searching.
        if run_astar:
            if len(queue) > 0 and searching:
                winner = 0 
                for i in range(len(queue)):
                    if queue[i].f < queue[winner].f:
                        winner = i
                current_cell = queue[winner]
                if current_cell == end_cell:
                    while current_cell.prior:
                        path.append(current_cell.prior)
                        current_cell = current_cell.prior
                    if not flag:
                        flag = True
                    elif searching:
                        continue
                if flag == False:
                    queue.remove(current_cell)
                    closedset.append(current_cell)
                    for neighbour in current_cell.neighbours:
                        if neighbour in closedset or neighbour.blocked:
                            continue
                        tempG = current_cell.g + 1
                        newpath = False
                        if neighbour in queue:
                            if tempG < neighbour.g:
                                neighbour.g = tempG
                                newpath = True
                        else:
                            neighbour.g = tempG
                            newpath = True
                            neighbour.queued = True
                            queue.append(neighbour)
                        if newpath:
                            neighbour.h = heuristics(neighbour, end_cell)
                            neighbour.f = neighbour.g + neighbour.h
                            neighbour.prior = current_cell
            else:
                if searching: # if still searching even though the search algorithm is done,
                    Tk().wm_withdraw()
                    messagebox.showerror("No Solution", "There Is No Solution!")
                    searching = False # stop searching.
        window.fill((0,0,0)) # grey lines between each cell
        # change colours of cells
        for i in range(c):
            for j in range(r):
                cell = grid[i][j]
                cell.draw(window, (190,190,190))

                if cell.queued:
                    cell.draw(window, (255, 200, 0))
                    cell.draw(window, (255, 175, 0), 0)
                if cell in closedset or cell.visited:
                    cell.draw(window, (255,255,255))
                if cell in path:
                    cell.draw(window, (0,200,0))

                if cell.start:
                    cell.draw(window, (0,200,0))
                if cell.blocked:
                    cell.draw(window, (0,0,0))
                if cell.end:
                    cell.draw(window, (200,0,0))
        
        pygame.display.flip()

if __name__ == '__main__':

    settings = SecondaryWindow()
    settings.resizable(False, False)
    settings.mainloop()
    