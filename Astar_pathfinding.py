"""
Algorithm explained (Guide followed Tech with Tim on youtube):

Its an informative algorithm that uses heuristic func to find shortest path,
so it doesn't bruteforce to find shortest path.

=Equation

F(n) = G(n) + H(n)

H(n) *Hscore-> shows the estimation of distance between node n to end node
G(n) *Gscore-> current shortest distance to get from node n to start node
F(n) *Fscore-> nodes with lower Fscore are the ones considered, assuming its closer to the end

Consider (A ----> D)
                           Node | F | G | H | Last
A-------B----              -----------------------
 \     /    |                A  | 0 | 0 | 0 |     
  \   /     |                B  | ∞ | ∞ | ∞ |
   \ C------D                C  | ∞ | ∞ | ∞ |
                             D  | ∞ | ∞ | ∞ |
Open set = {(0,A)
-> keeps track of the node that we want to look at next, starting with the start node)
-> contains (Fscore, node)
-> start graph with infinity for all points
-> points updated according to fscore considering nodes in open set
-> when a node is checked, all neighboring nodes fscores are calculated and if these values
are less than the ones in the table then the table is updated, if not then the node is ignored
-> if the end node reaches the open set with the lowest fscore, then the algorithm is done
-> check last column in table to find the shortest path


"""


import math
from queue import PriorityQueue

import pygame

WIDTH = 800 #width of pygame window
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding Algorithm")


#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64, 224, 208)

#Node holds it position (row,column) in grid, its width, its neighbors, its color
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width #width here is used to determine number of nodes
        self.y = col * width
        self.color = WHITE #initially all nodes are white
        self.neighbors = [] #neighbor nodes
        self.width = width
        self.total_rows = total_rows

    def get_pos(self): #returns position of node
        return self.row, self.col

    def is_closed(self): #checks if this node is already considered (closed set)
        return self.color == RED
    
    def is_open(self): #checks if this node is in the open set
        return self.color == GREEN
    
    def is_barrier(self): #checks if this node is a barrier
        return self.color == BLACK

    def is_start(self): #checks if this node is the start node
        return self.color == ORANGE

    def is_end(self): #checks if this node is the end node
        return self.color == TURQUOISE
    
    def reset(self): #resets node to white color
        self.color = WHITE

    def make_closed(self): 
        self.color = RED
    
    def make_open(self): 
         self.color = GREEN

    def make_barrier(self): 
         self.color = BLACK

    def make_start(self): 
         self.color = ORANGE

    def make_end(self): 
        self.color = TURQUOISE
   
    def make_path(self):
        self.color = PURPLE

    def draw(self, win): #where to draw the node
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid): #neighbors in 4 directions
        self.neighbors = []
        #a barrier can't be a neighbor
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #down node isn't a barrier
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #up node isn't a barrier
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #right node isn't a barrier
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #left node isn't a barrier
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other): #less than method, used to compare another node object with the current one
        return False

def h(p1, p2): #calculates H(n) between two points (uses manhattan distance, uses the shortest straight lines distance)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def astar_algo(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() #data structure for open set, efficient way to get the smallest element out of it, uses heap sort algo
    open_set.put((0, count, start)) #add start node with fscore to the open set
    came_from = {} #keeps track which node does the current one comes from (LAST column in table)
    g_score = {node: float("inf") for row in grid for node in row} #initially all values are inf
    g_score[start] = 0 #for start node gscores = 0
    f_score = {node: float("inf") for row in grid for node in row} #initially all values are inf
    f_score[start] = h(start.get_pos(), end.get_pos()) #for start node fscore = heuristic calculation to end node

    open_set_hash = {start} #keeps track of items that in the Queue, as u can't check if the value is still in open set (CHECK QUEUE DS)

    while not open_set.empty(): #as long as open set isn't empty, keep algo running
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #exit loop while algo running
                pygame.quit()
        
        current = open_set.get()[2] #current node
        open_set_hash.remove(current) #remove the current node from the open set hash

        if current == end: #PATH IS FOUND !
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 #assume all edges = 1


            if temp_g_score < g_score[neighbor]: #if we find a better way to reach this neighbor, update the path
                #similar to updating g_score in table if its less than the current value
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor)) #add neighbor to open set
                    open_set_hash.add(neighbor)
                    neighbor.make_open() #set neighbor to open

        draw()

        if current != start: #if the node is considered, close it
            current.make_closed()


    return False #we didn't find a path




def make_grid(rows, width): #creates the grid to draw
    grid = []
    gap = width // rows #// integer division
    for i in range(rows):
        grid.append([])
        for j  in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(win, rows, width): #draws grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap)) #draw horizontal lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width)) #draw vertical lines

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update() #updates that on the display

def get_clicked_pos(pos, rows, width): #gets mouse position when clicked           
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def main(win, width): #main loop
    ROWS = 50 #number of rows, increase for more nodes
    grid = make_grid(ROWS, width)

    start = None
    end = None
    
    run = True
    started = False
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get(): #check all the events that happened e.x mouse clicked
            if event.type == pygame.QUIT: #if window is closed, close the program
                run = False


            if pygame.mouse.get_pressed()[0]: #left mouse button is pressed
                pos = pygame.mouse.get_pos() #gives mouse coordinates
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col] #access node object from the grid 2D list
                if not start and node != end:
                    start = node
                    start.make_start()
                
                elif not end and node != start:
                    end = node
                    end.make_end()

                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]: #right mouse button is pressed:
                pos = pygame.mouse.get_pos() #gives mouse coordinates
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col] #access node object from the grid 2D list
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN: #if key on keyboard is pressed
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    #call A* pathfinding algo
                    astar_algo(lambda: draw(win, grid, ROWS, width), grid, start, end) #pass draw function as arg
                
                if event.key == pygame.K_c: #clear the entire screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit() #close pygamme window

main(WIN, WIDTH)