import pygame
from deckLogic import deckHandling
from pygameUtils.buttonUtils import button, discreteSlider

deckInstance = deckHandling(4) # Deck handling instance ready

# Pygame Setup
pygame.init() # Initialise Pygame
initX = 1400
initY = 900
INITIALSIZE = (initX, initY) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/table.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen

# Button Setup
newGameButton = button(screen, (700,300), "button")
continueButton = button(screen, (700,400), "button")
settingsButton = button(screen,(700,500), "button")
quitButton = button(screen, (700,600), "button")

def newGameSettings():
    # Mini Window Setup
    miniWindowImage = pygame.image.load("bankrollBust/images/MiniMenu.png")
    miniWindowRect = miniWindowImage.get_rect(center=(initX/2, initY/2))
    
    # Interaction Setup
    noOfDecksSlider = discreteSlider(screen, (miniWindowRect.centerx, miniWindowRect.centery), [1,2,3,4,5])
    difficultySlider = None
    noOfPlayersSliders = None
    startingBuxInput = None
    #startButton = button(screen, (miniWindowRect.centerx, miniWindowRect.centery), "button")
    #cancelButton = button(screen, (), "button")
    # Keeping Window Open
    started = False
    while not started:
        for event in pygame.event.get(): #Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
        pygame.display.flip()
        screen.blit(miniWindowImage, miniWindowRect)
        if noOfDecksSlider.moveThumb():
            pass
            #return [1,2,3,4]
        #if quitButton.updateImage():
            #return None

def newGame(noOfDecks, difficulty, startingBux, noOfPlayers):
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
    if newGameButton.updateImage():
        gameSettings = newGameSettings()
        if newGameSettings is not None: # If it is none they cancelled new game
            noOfDecks = gameSettings[0]
            difficulty = gameSettings[1]
            startingBux = gameSettings[2]
            noOfPlayers = gameSettings[3]
    continueButton.updateImage()
    settingsButton.updateImage()
    if quitButton.updateImage():
        gameRunning = False
    
    pygame.display.flip() # Update the screen
    
pygame.quit # Exit out of Pygame
