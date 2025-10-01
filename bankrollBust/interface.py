import pygame

def menu():
    pygame.init() # Initialise Pygame
    screen = pygame.display.set_mode((400,400), pygame.RESIZABLE) # Initial Size of screen, to be changed as resizable is allowed 
    running = True # Game runs on script running
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(screen.get_size())
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pygame.display.flip()


pygame.quit()