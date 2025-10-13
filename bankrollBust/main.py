import pygame
from deckLogic import deckHandling
import interface
from pygameUtils.buttonUtils import button

deckInstance = deckHandling(4) # Deck handling instance ready

# Pygame Setup
pygame.init() # Initialise Pygame
INITIALSIZE = (1400, 800) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/menu.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen

# Button Setup
buttons = [button(screen, (700,420), "button"), button(screen,(700,520), "button"), button(screen, (700,620), "button")]
button1 = buttons[0]
button2 = buttons[1]
button3 = buttons[2]

# Main Game Loop
gameRunning = True
while gameRunning:
    for event in pygame.event.get(): #Checking for events
        if event.type == pygame.QUIT: # If the user presses the X button, quit game
            gameRunning = False
    screen.blit(bg, (0,0)) # Set the screen as my background
    button1.draw()
    mousePos = pygame.mouse.get_pos()
    if button1.checkHover(mousePos):
        pygame.display.set_caption("YUHHH")
    else:
        pygame.display.set_caption("NAHHHH")
    pygame.display.flip() # Update the screen
    
pygame.quit # Exit out of Pygame