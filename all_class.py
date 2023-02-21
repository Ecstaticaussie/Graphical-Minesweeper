import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, isMine, isFlagged, pos, size, colour):
        super().__init__()
        self.size = size
        self.isMine = isMine
        self.isFlagged = isFlagged
        self.pos = pos
        self.image = pygame.surface.Surface(size)
        self.rect = self.image.get_rect(topleft = pos)
        self.image.fill(colour)
        self.font = pygame.font.Font("/Users/Kids/Documents/Programming/python_personal/oop_mine_sweeper/assests/Pixeltype.ttf", 30)

    def show_num(self, num, screen):
        self.num_txt = self.font.render(str(num), False, "#BBBBBB")
        self.num_txt_rect = self.num_txt.get_rect(center = (self.pos[0]+int(self.size[0] / 2), self.pos[1]+int(self.size[1] / 2)))
        screen.blit(self.num_txt, self.num_txt_rect)

    def find_index(self, grid):
        for row in range(len(grid)):
            for cell in range(len(grid[0])):
                if grid[row][cell] == self: self.index = (row, cell)

    def give_adj_cells(self, grid):
        x = self.index[0]
        y = self.index[1]

        row_length = len(grid[0])
        column_length = len(grid)
        adj_cells = []

        try:
            if grid[x-1][y-1] and x >= 1 and y>= 1: adj_cells.append(grid[x-1][y-1])
        except: pass
        try:
            if grid[x][y-1] and y>= 1: adj_cells.append(grid[x][y-1])
        except: pass
        try:
            if grid[x+1][y-1] and x <= row_length-1 and y>= 1: adj_cells.append(grid[x+1][y-1])
        except: pass
        try: 
            if grid[x-1][y] and x >= 1: adj_cells.append(grid[x-1][y])
        except: pass
        try: 
            if grid[x+1][y] and x <= row_length-1: adj_cells.append(grid[x+1][y])
        except: pass
        try:
            if grid[x-1][y+1] and x >= 1 and y<= column_length-1:adj_cells.append(grid[x-1][y+1])
        except: pass
        try:
            if grid[x][y+1] and y<= column_length-1: adj_cells.append(grid[x][y+1])
        except: pass
        try:
            if grid[x+1][y+1] and x <= row_length-1 and y<= column_length-1: adj_cells.append(grid[x+1][y+1])
        except: pass

        self.adj_cells = adj_cells

    def get_adjacent_mines(self, grid):
        x = self.index[0]
        y = self.index[1]

        adjacent_mines = 0
        row_length = len(grid[0])
        column_length = len(grid)

        try:
            if grid[x-1][y-1].isMine and x >= 1 and y>= 1: adjacent_mines += 1
        except: pass
        try:
            if grid[x][y-1].isMine and y>= 1: adjacent_mines += 1
        except: pass
        try:
            if grid[x+1][y-1].isMine and x <= row_length-1 and y>= 1: adjacent_mines += 1
        except: pass
        try:
            if grid[x-1][y].isMine and x >= 1: adjacent_mines += 1
        except: pass
        try:
            if grid[x+1][y].isMine and x <= row_length-1: adjacent_mines += 1
        except: pass
        try:
            if grid[x-1][y+1].isMine and x >= 1 and y<= column_length-1: adjacent_mines += 1
        except: pass
        try:
            if grid[x][y+1].isMine and y<= column_length-1: adjacent_mines += 1
        except: pass
        try:
            if grid[x+1][y+1].isMine and x <= row_length-1 and y<= column_length-1: adjacent_mines += 1
        except: pass

        self.adj_mines_num = adjacent_mines

class myCursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((1, 1))
        self.rect = self.image.get_rect(topleft = (100, 100))
        self.image.fill("white")

    def set_pos(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]
        self.rect.y = mouse_pos[1]

    def get_pos(self): return(self.rect.x, self.rect.y)

    
