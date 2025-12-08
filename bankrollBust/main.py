import pygame
from deckLogic import deckHandling
from pygameUtils.buttonUtils import button, discreteSlider, inputBox

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
newGameButton = button(screen, (700,300), "New Game")
continueButton = button(screen, (700,400), "Continue")
settingsButton = button(screen,(700,500), "Settings")
quitButton = button(screen, (700,600), "Quit")

def newGameSettings():
    # Mini Window Setup
    miniWindowImage = pygame.image.load("bankrollBust/images/MiniMenu.png")
    miniWindowRect = miniWindowImage.get_rect(center=(initX/2, initY/2))    
    # Interaction Setup
    noOfDecksSlider = discreteSlider(screen, "Number Of Decks", (miniWindowRect.centerx, miniWindowRect.centery-150), [1,2,4,6,8,10], scale=1.3)
    difficultySlider = discreteSlider(screen, "Difficulty", (miniWindowRect.centerx, miniWindowRect.centery-100), ["Full-Assist", "Semi-Assist", "There-When-Needed","No-Help"], scale=1.3)
    noOfNPCsSlider = discreteSlider(screen, "Number of NPCs", (miniWindowRect.centerx, miniWindowRect.centery-50), [0,1,2,3,4,5,6,7], scale=1.3)
    startingBuxInput = inputBox(screen, (miniWindowRect.centerx, miniWindowRect.centery+25), "Starting Bux", None, scale=0.8)
    startButton = button(screen, (miniWindowRect.centerx+135, miniWindowRect.centery+125), "Start Game", scale=0.7)
    cancelButton = button(screen, (miniWindowRect.centerx-135, miniWindowRect.centery+125), "Cancel", scale=0.7)
    # Keeping Window Open
    started = False
    while not started:
        for event in pygame.event.get(): #Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            screen.blit(miniWindowImage, miniWindowRect)
            noOfDecks = noOfDecksSlider.getValue(event)
            difficulty = difficultySlider.getValue(event)
            noOfPlayers = noOfNPCsSlider.getValue(event)
            startingBux = startingBuxInput.getInput(event)
            if startButton.updateImage(event):
                started = True
                return [noOfDecks, difficulty, noOfPlayers, startingBux]
            elif cancelButton.updateImage(event):
                return None # Gotta figure out logic
            pygame.display.flip()

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
    screen.blit(bg, (0,0)) # Set the screen as my background
    for event in pygame.event.get(): #Checking for events
        if event.type == pygame.QUIT: # If the user presses the X button, quit game
            gameRunning = False
        if newGameButton.updateImage(event):
            gameSettings = newGameSettings()
            if gameSettings is not None: # If it is none they cancelled new game
                noOfDecks = gameSettings[0]
                difficulty = gameSettings[1]
                noOfPlayers = gameSettings[2]
                startingBux = gameSettings[3]
                newGame(noOfDecks, difficulty, noOfDecks, startingBux)
        elif continueButton.updateImage(event):
            pass
        elif settingsButton.updateImage(event):
            pass
        elif quitButton.updateImage(event):
            gameRunning = False
        pygame.display.flip() # Update the screen
    
    
    
pygame.quit # Exit out of Pygame

