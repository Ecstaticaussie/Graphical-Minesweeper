import pygame
from random import randint
from all_class import Cell, myCursor

class Game(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.grid = [[Cell(False, False, (50+y, 50+x), (35, 35), "#99b4bf") for x in range(0, 541, 37)] for y in range(0, 541, 37)]
        self.grid_background = Cell(False, False, (35, 35), (self.grid[-1][-1].pos[0]+15, self.grid[-1][-1].pos[1]+15), "#e3e7e8")
        self.non_cell_mines = []

    def setup(self):
        self.cursor = myCursor()
        self.cells = pygame.sprite.Group()
        self.cells_background = pygame.sprite.GroupSingle(self.grid_background)

        #sets up the mines
        num_of_mines = 28
        while num_of_mines != 0:
            x = randint(0, 14)
            y = randint(0, 14)
            if not self.grid[x][y].isMine:
                self.grid[x][y].isMine = True
                num_of_mines -= 1
        
        for row in self.grid:
            for cell in row:
                self.cells.add(cell)
                cell.find_index(self.grid)
                cell.give_adj_cells(self.grid)
                cell.get_adjacent_mines(self.grid)
    
    def show_all_mines(self):
        for row in self.grid:
            for cell in row:
                if cell.isMine: cell.image.fill("red")

    def spreading(self, cell):
        if not cell.adj_mines_num:
            for adj_cell in cell.adj_cells:
                print(adj_cell)

    def change_cell_state(self):
        mouse_buttons = pygame.mouse.get_pressed()
        collided_cell = pygame.sprite.spritecollide(self.cursor, self.cells, False)
        if collided_cell and (collided_cell not in self.non_cell_mines):
            collided_cell = collided_cell[0]
            if mouse_buttons[0] and not mouse_buttons[2]:
                if collided_cell.isMine:
                    self.show_all_mines()
                else:
                    self.non_cell_mines.append(collided_cell)
                    self.spreading(collided_cell)
                    self.non_cell_mines = list (set(self.non_cell_mines))


            elif not mouse_buttons[0] and mouse_buttons[2]:
                collided_cell.isFlagged = True
                collided_cell.image.fill("#99b4ff")

    def always_shows_adj_mines(self, screen):
        for cell in self.non_cell_mines:
            if not cell.isFlagged:
                cell.image.fill("white")
                if cell.adj_mines_num != 0: cell.show_num(cell.adj_mines_num, screen)
        
    def update(self, screen):
        self.cursor.set_pos()
        self.change_cell_state()
        self.always_shows_adj_mines(screen)