import pygame
from random import randint
from all_class import Cell, myCursor

#The main class which has all the code executing here
class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #This is the program's representation of the game
        self.grid = [[Cell(False, False, (50+y, 50+x), (35, 35), "#99b4bf") for x in range(0, 541, 37)] for y in range(0, 541, 37)]
        #background for the cell
        self.grid_background = Cell(False, False, (35, 35), (self.grid[-1][-1].pos[0]+15, self.grid[-1][-1].pos[1]+15), "#e3e7e8")
        #This is for updating all the cells the user have to be not mines
        self.non_cell_mines = []

    #This is run at the beginning of main.py to set up and randomise the mines
    def setup(self):
        #places the cursor and all the cells into 2 seperate groups - this is how pygame deals with collisions
        self.cursor = myCursor()
        self.cells = pygame.sprite.Group()

        #sets up the mines - randomly picks an elemen from self.grid
        num_of_mines = 28
        while num_of_mines != 0:
            x = randint(0, 14)
            y = randint(0, 14)
            if not self.grid[x][y].isMine:
                self.grid[x][y].isMine = True
                num_of_mines -= 1
        
        #this sets up all the information about each cell a the start of the program
        for row in self.grid:
            for cell in row:
                self.cells.add(cell)
                cell.find_index(self.grid)
                cell.give_adj_cells(self.grid)
                cell.get_adjacent_mines(self.grid)
    
    #if a mine is clicked by the user, this method shows all of the mines
    def show_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.isMine: cell.image.fill("red")

    #This is meant to be a recursive subroutine to spread out the cells clicked by the user - WHERE THE ISSUE OF THE PROGRAM IS
    #I have tried implementing variuos recursive ways of applying a method to every element in a list, but it causes a RecursionError - too many subroutines in the call stack
    def spreading(self, cell):
        if not cell.adj_mines_num:
            for adj_cell in cell.adj_cells:
                if not adj_cell.isMine: self.non_cell_mines.append(adj_cell)
                self.spreading(adj_cell)

    #This is what happens when a user clicks on a cell
    def change_cell_state(self):
        #gets the specified mouse buttons being clicked
        mouse_buttons = pygame.mouse.get_pressed()
        #Gets the cell that the user has clicked on
        collided_cell = pygame.sprite.spritecollide(self.cursor, self.cells, False)
        if collided_cell: #Checks if the collided_cell list is not empty -> collisions are outputted via lists
            collided_cell = collided_cell[0]
            #this is for checking what buttons have been clicked - this is for left mouse button
            if mouse_buttons[0] and not mouse_buttons[2]:
                #shows all the mines if a mine has been clicked
                if collided_cell.isMine:
                    self.show_all_mines()
                else:
                    #this spreads out the empty cells based on where the user has clicked
                    self.non_cell_mines.append(collided_cell)
                    self.spreading(collided_cell)
                    #makes sure that there are no repeated cells being updated
                    self.non_cell_mines = list(set(self.non_cell_mines))

            #this is for right mouse button - flags a cell and prevents from being accidentlly clicked
            elif not mouse_buttons[0] and mouse_buttons[2]:
                collided_cell.isFlagged = True
                collided_cell.image.fill("#99b4ff")

    #this shows all the non-mine cells that have been clicked by the user
    def always_shows_clicked_cells(self, screen):
        for cell in self.non_cell_mines:
            if not cell.isFlagged:
                cell.image.fill("white")
                #shows the number of adjacent cells
                if cell.adj_mines_num != 0: cell.show_num(cell.adj_mines_num, screen)
        
    #here, the cursor and cells are updated each time they are called
    def update(self, screen):
        self.cursor.set_pos()
        self.change_cell_state()
        self.always_shows_clicked_cells(screen)