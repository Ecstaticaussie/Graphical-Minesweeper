from game_class import Game
import pygame, sys

#The class instance being used and setup
the_game = Game()
the_game.setup()

# Pygame setup - initialise, set the window and create a clock for the amount of times the code is run per second(fps)
pygame.init()
screen = pygame.display.set_mode((1100, 680))
clock = pygame.time.Clock()

#The code is run here in an infinite while loop
while True:
    #All events
    for event in pygame.event.get():
        #To close the game in this bizarre way
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    #This places the screen and all the cells
    screen.fill('white')
    the_game.cells_background.draw(screen)
    the_game.cells.draw(screen)

    #Continously updates the state of the game
    the_game.update(screen)

    #This updates the window a set number of times per second - fps
    pygame.display.update()
    clock.tick(60)