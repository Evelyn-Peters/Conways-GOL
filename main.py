

import pygame
from random import randint
pygame.font.init()


BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
screen_width = 400
screen_height = 400

mywantsize = 40

def wraparound(index, size):

    '''takes in current index and size of array and returns the new index (that is wrapped around the array)'''

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
    
    return [[((y, x), 0) for x in range(size)] for y in range(size)]

def convert_array_to_pygame(myarray):

    '''Converst an array in the format of location and status into an array of instances of Cell class'''

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

    '''converts an array of cell instances to back end tuples'''

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

    '''A class for each square/pixel/cell in the game'''

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
            self.color = BLACK
        self.color = WHITE
    def change_state(self):
        if self.state:
            self.color = WHITE
        elif self.state == False:
            self.color = BLACK
    def draw_cell(self, display):
        rect = pygame.Rect(self.top_corner_x, self.top_corner_y, self.width, self.height)
        pygame.draw.rect(display, self.color, rect)
        #pygame.draw.rect(screen, (235,245,255), rect, 1)
    def button_dimensions(self):
        return pygame.Rect(self.top_corner_x, self.top_corner_y, self.width, self.height)
import ast

gun_array = []
with open('gun.txt','r') as file:
    lines = file.readlines()
    string_list = lines[0]
    real_list = ast.literal_eval(string_list)
    gun_array = real_list

print(gun_array)

show_gun = convert_array_to_pygame(gun_array)
quasar_array = []
with open('quasar.txt','r') as file:
    lines = file.readlines()
    string_list = lines[0]
    real_list = ast.literal_eval(string_list)
    quasar_array = real_list

show_quasar = convert_array_to_pygame(quasar_array)

behind_n_array = make_beg_array(mywantsize)
showcase_normal = convert_array_to_pygame(behind_n_array)


screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont('markerfelt', 23) 
title_font = pygame.font.SysFont('markerfelt', 14)  

# Text
title_text = font.render("Maija & Evelyn's completely original game", True, BLACK) 
second_title_text = font.render("(also known as Conway's Game of Life)", True, BLACK)
subtitle_text = title_font.render("Starting Screen: Press 'B' for blank, 'G' for a gun, and 'Q' for a quasar", True, BLACK)

# Text positions
title_pos = title_text.get_rect(center=(200, 100))  # Center at x=400, y=200
s_title_pos = second_title_text.get_rect(center=(200, 130))
subtitle_pos = subtitle_text.get_rect(center=(200, 180))


running = True
gens = False
drawing = False
ORANGE = (255, 165, 0, 255)
start_screen = True

while running:

    
    for event in pygame.event.get(): # handling all keypresses

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.KEYDOWN:

            if start_screen:  # Handle keypresses only for the title screen
                if event.key == pygame.K_b:
                    showcase_array = showcase_normal
                    start_screen = False
                elif event.key == pygame.K_g:
                    showcase_array = show_gun
                    start_screen = False
                elif event.key == pygame.K_q:
                    showcase_array = show_quasar
                    start_screen = False

            else: # Handle keypresses for the main game
                if event.key == pygame.K_r:
                    start_screen = True
                    behind_n_array = make_beg_array(mywantsize)
                    showcase_normal = convert_array_to_pygame(behind_n_array)

                if event.key == pygame.K_RETURN:
                    gens = True
                    behind_array = front_to_back(showcase_array)
                elif event.key== pygame.K_SPACE:
                    gens = False

    if start_screen: # starting screen
        screen.fill(ORANGE)
        screen.blit(title_text, title_pos)
        screen.blit(second_title_text, s_title_pos)
        screen.blit(subtitle_text, subtitle_pos)

    else: # showing which starting screen you chose
        screen.fill(ORANGE) 
        for row in showcase_array:
            for cell in row:
                cell.draw_cell(screen)

    if drawing and not start_screen: # handling drawing in blank mode
        mouse_y, mouse_x = pygame.mouse.get_pos()
        col = mouse_x // (screen_width// mywantsize)
        row = mouse_y //(screen_height // mywantsize)
        if 0 <= row < mywantsize and 0 <= col < mywantsize:
            mycell= showcase_array[row][col]
            mycell.color= BLACK
            mycell.state =True

    if gens and not start_screen: # going through generations
        behind_array = nextgen(behind_array)
        pygame.time.wait(70)
        showcase_array = convert_array_to_pygame(behind_array)

    pygame.display.flip()

pygame.quit()
