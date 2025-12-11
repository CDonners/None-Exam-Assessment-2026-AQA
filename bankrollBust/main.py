import pygame
from deckLogic import deckHandling
from pygameUtils.buttonUtils import button, discreteSlider, inputBox

deckInstance = deckHandling(4) # Deck handling instance ready

# Pygame Setup
pygame.init() # Initialise Pygame
INITX = 1400
INITY = 900
INITIALSIZE = (INITX, INITY) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/table.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen

# Button Setup
centreX = INITX//2 # Dynamically centering X
# Dymanically centering Y with the formula (Distance from top initially)/(Initial Y) * CurrentY this will make the buttons be in the same place no matter the screensize
newGameButton = button(screen, (centreX, 600), "New Game")
continueButton = button(screen, (centreX,400), "Continue")
settingsButton = button(screen,(centreX,500), "Settings")
quitButton = button(screen, (centreX,600), "Quit")

def newGameSettings():
    # Mini Window Setup
    miniWindowImage = pygame.image.load("bankrollBust/images/MiniMenu.png") # Loading the mini window image
    miniWindowRect = miniWindowImage.get_rect(center=(INITX/2, INITY/2)) # Dynamically centering the window
    # Interaction Setup
    currentX = miniWindowRect.centerx # Making my function calls shorter - Neater code :)
    currentY = miniWindowRect.centery
    noOfDecksSlider = discreteSlider(screen, "Number Of Decks", (currentX, currentY-150), [1,2,4,6,8,10], scale=1.3)
    difficultySlider = discreteSlider(screen, "Difficulty", (currentX, currentY-100), ["Full-Assist", "Semi-Assist", "There-When-Needed","No-Help"], scale=1.3)
    noOfNPCsSlider = discreteSlider(screen, "Number of NPCs", (currentX, currentY-50), [0,1,2,3,4,5,6,7], scale=1.3)
    startingBuxInput = inputBox(screen, (currentX, currentY+25), "Starting Bux", None, scale=0.8)
    startButton = button(screen, (currentX+135, currentY+125), "Start Game", scale=0.7)
    cancelButton = button(screen, (currentX-135, currentY+125), "Cancel", scale=0.7)
    # Keeping Window Open
    started = False
    while not started:
        for event in pygame.event.get(): #Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            screen.blit(miniWindowImage, miniWindowRect) # Draws the mini window onto the screen
            noOfDecks = noOfDecksSlider.getValue(event) # Get the value from the slider -- See buttonUtils.py
            difficulty = difficultySlider.getValue(event) # Get the value from the slider -- See buttonUtils.py
            noOfPlayers = noOfNPCsSlider.getValue(event) # Get the value from the slider -- See buttonUtils.py
            startingBux = startingBuxInput.getInput(event) # Get the value of the input box -- See buttonUtils.py
            if startButton.updateImage(event): # Checking if User has pressed the start button
                started = True # Sets started to true breaking the loop
                return [noOfDecks, difficulty, noOfPlayers, startingBux] # Returns list of all selected settings
            elif cancelButton.updateImage(event): # Checks if player pressed the cancel button
                return None # Retuns none passing over the If-Statement checking if the game is started
            pygame.display.flip() # Updates the screen with all the rects 

def newGame(noOfDecks, difficulty, startingBux, noOfNPCs):
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
        # By updating the image on an event I can limit the amount of checks my code makes, additionally I can make it so you only press one button at a time
        if newGameButton.updateImage(event):
            gameSettings = newGameSettings()
            if gameSettings is not None: # If it is none they cancelled new game
                # Settings the values of the selected settings - Neater function call
                noOfDecks = gameSettings[0]
                difficulty = gameSettings[1]
                noOfNPCs = gameSettings[2]
                startingBux = gameSettings[3]
                newGame(noOfDecks, difficulty, noOfNPCs, startingBux) # Creating the game with the selected settings
        elif continueButton.updateImage(event):
            pass
        elif settingsButton.updateImage(event):
            pass
        elif quitButton.updateImage(event):
            gameRunning = False
        pygame.display.flip() # Update the screen
    
    
    
pygame.quit # Exit out of Pygame

