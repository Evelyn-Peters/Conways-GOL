

import pygame
from random import randint
pygame.font.init()
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
screen_width = 400
screen_height = 400

def wraparound(index, size):
    
    if index < 0:
        return size - 1
    elif index >= size:
        return 0
    return index

def generate_random_array(size):
    
    '''generates random square array from the input size'''
    
    return [[((x, y), randint(0, 1)) for x in range(size)] for y in range(size)]

def make_beg_array(size):
    '''generates blank array for starting'''
    
    return [[((x, y), 0) for x in range(size)] for y in range(size)]

def convert_array_to_pygame(myarray):
    square_width = screen_width // mywantsize
    square_height = screen_height // mywantsize
    newarray = []
    for row in myarray:
        newrow = []
        for pixel in row:
            loctuple = pixel[0]
            state = pixel[1]
            if state == 0:
                newrow.append(Cell(WHITE,False,loctuple[0]*square_width,loctuple[1]*square_height,square_width,square_height))
            elif state == 1:
                newrow.append(Cell(BLACK,True,loctuple[0]*square_width,loctuple[1]*square_height,square_width,square_height))
        newarray.append(newrow)
    return newarray

def front_to_back(front_array):
    new_array = []
    for row in front_array:
        new_row = []
        for cell in row:
            new = cell.to_behind()
            new_row.append(new)
        new_array.append(new_row)
    return new_array

def nextgen(currgen): 
    
    '''go through every cell index, make new list generation with 0 or 1 repping true or false for change_status'''
    
    newgen = []
    
    for row in range(len(currgen)):

        new_row = []
        
        for pixel in range(len(currgen)):
            
            cell = currgen[row][pixel]
            cells_around = cellsurrounding(currgen, cell)
            newstate = change_status(cell, cells_around)
            new_row.append(((row, pixel), newstate))
            
        newgen.append(new_row)
    
    return newgen

def cellsurrounding(initialpattern, individualcell):
    
    
    '''returns list of lists of cells surorunding the input cell. each list inside the list reperesents the individual layers of the array '''
    
    #this is a list of each cell's status of life/death surrounding the self cell. It starts on the top left and continues clockwise
    
    size = len(initialpattern)
    y, x = individualcell[0]
    
    neighbors = []
    
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            
            if dx == 0 and dy == 0:
                continue
                
            indx, indy = wraparound(x + dx, size), wraparound(y + dy, size)
            neighbors.append(initialpattern[indy][indx][1])
            
    return neighbors

def change_status(currentcell, surroundingcells):
    
    '''
    Rules of the Game of Life
    A live cell dies if it has fewer than two live neighbors.
    A live cell with two or three live neighbors lives on to the next generation.
    A live cell with more than three live neighbors dies.
    A dead cell will be brought back to live if it has exactly three live neighbors.'''

    
    '''returns whether the inside cell should be live or dead using conways game of life'''
    
    #returns True if inside cell is live, false if dead
            
    alive = currentcell[1]
    numoflive = sum(surroundingcells)
    
    if alive == 1:
        
        if numoflive < 2 or numoflive > 3:
            return 0
        elif 2 <= numoflive <= 3:
            return 1
    
    elif alive == 0:
        if numoflive == 3:
            return 1
        
    return 0

class Cell:

    def __init__(self, color, state, top_corner_x, top_corner_y, width, height):
        self.state = state
        self.color = color
        self.top_corner_x = int(top_corner_x)
        self.top_corner_y = int(top_corner_y)
        self.width = int(width)
        self.height = int(height)
    def __str__(self):
        return f"state:{self.state}, color: {self.color}, location {self.top_corner_x,self.top_corner_y}"

    def to_behind(self):
        if self.state:
            return ((int(self.top_corner_x/self.width),int(self.top_corner_y/self.height)),1)
        return ((int(self.top_corner_x/self.width),int(self.top_corner_y/self.height)),0)
    def state_to_color(self):
        if self.state:
            self.color == BLACK
        self.color == WHITE
    def change_state(self):
        if self.state:
            self.color == WHITE
        elif self.state == False:
            self.color == BLACK
    def draw_cell(self, display):
        rect = pygame.Rect(self.top_corner_x, self.top_corner_y, self.width, self.height)
        pygame.draw.rect(display, self.color, rect)
        pygame.draw.rect(screen, (235,245,255), rect, 1)
    def button_dimensions(self):
        return pygame.Rect(self.top_corner_x, self.top_corner_y, self.width, self.height)

mywantsize = 25

behind_array = make_beg_array(mywantsize)
showcase_array = convert_array_to_pygame(behind_array)

screen = pygame.display.set_mode((screen_width, screen_height))

running = True
gens = False

while running:

    for row in showcase_array:
        for cell in row:
            cell.draw_cell(screen)
            #pygame.draw.rect(screen, BLACK, , 1)
            

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Handle closing the window, happens when hitting x button by pygame default
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # Handle mouse clicks
            for row in showcase_array:
                for cell in row:
                    button = cell.button_dimensions()
                    if button.collidepoint(event.pos):
                        if cell.color == WHITE:
                            cell.color = BLACK
                            cell.state = True
                        elif cell.color == BLACK:
                            cell.color = WHITE
                            cell.state = False
            
                    
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # Start going through gens
                
                gens = True

                behind_array = front_to_back(showcase_array)


            elif event.key == pygame.K_SPACE: 
                gens = False
                for row in showcase_array:
                    for cell in row:
                        cell.draw_cell(screen)
                # set behind array to new one with inputted cells

    if gens:


        

        behind_array = nextgen(behind_array)


        pygame.time.wait(200)
        showcase_array = convert_array_to_pygame(behind_array)




pygame.quit()
