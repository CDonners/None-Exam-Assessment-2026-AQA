import pygame
from deckLogic import deckHandling
from pygameUtils.buttonUtils import button

deckInstance = deckHandling(4) # Deck handling instance ready

# Pygame Setup
pygame.init() # Initialise Pygame
INITIALSIZE = (1400, 900) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/table.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen

# Button Setup
playButton = button(screen, (700,400), "button")
settingsButton = button(screen,(700,500), "button")
quitButton = button(screen, (700,600), "button")

def play():
    global gameRunning
    while gameRunning:
        for event in pygame.event.get(): #Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
        screen.blit(bg, (0,0)) # Set the screen as my background
        pygame.display.flip()

# Main Game Loop
gameRunning = True
while gameRunning: # Main Menu Loop
    for event in pygame.event.get(): #Checking for events
        if event.type == pygame.QUIT: # If the user presses the X button, quit game
            gameRunning = False
    screen.blit(bg, (0,0)) # Set the screen as my background
    # Draw the buttons, also detects whether pressed or 
    if playButton.updateImage():
        play()
    settingsButton.updateImage()
    if quitButton.updateImage():
        gameRunning = False
    
    pygame.display.flip() # Update the screen
    
pygame.quit # Exit out of Pygame