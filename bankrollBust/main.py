import pygame
from pygameUtils.buttonUtils import button, discreteSlider, inputBox
from gameLogic import playGame

# Pygame Setup
pygame.init() # Initialise Pygame
INITX = 1400
INITY = 900
INITIALSIZE = (INITX, INITY) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/table.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen

# Menu Button Setup
centreX = INITX//2 # X is always centre no matter the initial size
newGameButton = button(screen, (centreX, 300), "New Game")
continueButton = button(screen, (centreX,400), "Continue")
settingsButton = button(screen,(centreX,500), "Settings")
quitButton = button(screen, (centreX,600), "Quit")
# Game Button Setup
hitButton = button(screen, (centreX+375, 770), "Hit", interactable=False)
standButton = button(screen, (centreX-375, 770), "Stand", interactable=False)
splitButton = button(screen, (centreX-375, 850), "Split", interactable=False)
insuranceButton = button(screen, (centreX+375, 850), "Insurance", interactable=False)
ConfirmBetButton = button(screen, (centreX, 850), "Confirm Bet", interactable=False)

def playingGame(game):
    # Creating the bet amount input box
    minBet = round((int(game.startingBux)/100)/5)*5 # Rounds the minimum bet to the nearest 5, so the minimum bet will always be 1% of the starting bux to the nearest 5
    betAmountInputBox = inputBox(screen, (centreX, 770), "Bet Amount", "num", f"{minBet}", interactable=False, minMax=[float(minBet), 1000*float(minBet)])
    betAmount = None
    # Game Status variables
    gamePlayRunning = True
    bettingPhase = True
    # Gameplay loop
    while gamePlayRunning:
        screen.blit(bg, (0,0)) # Set the screen as my background
        for event in pygame.event.get(): # Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            if bettingPhase:
                print("Betting Phase")
                hitButton.makeUninteractable()
                standButton.makeUninteractable()
                splitButton.makeUninteractable()
                insuranceButton.makeUninteractable()
                for player in game.players:
                    print("Going through players for bet")
                    if player.name == "Player":
                        print("Player Found")
                        # Betting Phase - Collect bet from player
                        # Make betting buttons interactable
                        print("Making buttons interactable")
                        ConfirmBetButton.makeInteractable()
                        betAmountInputBox.makeInteractable()
                        # Draw the image for the rest of the buttons
                        print("Drawing buttons")
                        hitButton.updateImage(event)
                        standButton.updateImage(event)
                        splitButton.updateImage(event)
                        insuranceButton.updateImage(event)
                        # Have input box waiting for input
                        print("Bet amount waiting for input")
                        betAmount = betAmountInputBox.getInput(event)
                        # Set max bet
                        print("Setting max bet")
                        betAmountInputBox.setMax(int(player.bustBux))
                        # Detect if bet is confirmed
                        print("Waiting for bet confirmation")
                        if ConfirmBetButton.updateImage(event): 
                            print("Bet confirmed")
                            bettingPhase = False  # Move to playing phase
                    else:
                        pass # NPC Decide bet
            else:
                # Playing Phase - Game is active
                ConfirmBetButton.makeUninteractable()
                betAmountInputBox.makeUninteractable()  
                ConfirmBetButton.updateImage(event)  
                print("Game round starting")
                game.roundStarted = True
                
            if game.roundStarted == True:
                print("123 Game round started")
                for player in game.players:
                    print("Looping through player for action")
                    if not player.isStood and not player.isBusted:
                        print("Player not stood")
                        if player.name == "Player": # Players turn
                            print("Found player turn")
                            # These will always be available for the player
                            hitButton.makeInteractable()
                            standButton.makeInteractable()
                            # Checking if the condition for the special cases are met
                            if len(player.hand) == 2:
                                if player.hand[0].face == player.hand[1].face:
                                    splitButton.makeInteractable()
                                # Got to figure out how to handle dealer to check condition for insurance 
                            else:
                                splitButton.makeUninteractable
                                insuranceButton.makeUninteractable
                            if hitButton.updateImage(event):
                                print("Hit that thang")
                                player.dealCard()
                            if standButton.updateImage(event):
                                player.stand()
                            splitButton.updateImage(event)
                            insuranceButton.updateImage(event)
                    else:
                        pass # NPC's turn
        # Drawing all the buttons    
        hitButton.draw()
        standButton.draw()
        splitButton.draw()
        insuranceButton.draw()
        ConfirmBetButton.draw()
        betAmountInputBox.draw()
        
        # Initial deal happens once, after betting
        if bettingPhase == False and game.roundStarted == False:
            print("Dealing")
            game.initialDeal()
        game.updateImage()
        pygame.display.flip()

def newGameSettings():
    
    # Mini Window Setup
    miniWindowImage = pygame.image.load("bankrollBust/images/MiniMenu.png") # Loading the mini window image
    miniWindowRect = miniWindowImage.get_rect(center=(INITX/2, INITY/2)) # Dynamically centering the window
    # Interaction Setup
    currentX = miniWindowRect.centerx # Making my function calls shorter - Neater code :)
    currentY = miniWindowRect.centery
    noOfDecksSlider = discreteSlider(screen, "Number Of Decks", (currentX, currentY-150), [1,2,4,6,8,10], scale=1.3)
    difficultySlider = discreteSlider(screen, "Difficulty", (currentX, currentY-100), ["Full-Assist", "Semi-Assist", "There-When-Needed","No-Help"], scale=1.3)
    noOfNPCsSlider = discreteSlider(screen, "Number of NPCs", (currentX, currentY-50), [0,1,2,3,4,5,6], scale=1.3)
    startingBuxInput = inputBox(screen, (currentX, currentY+25), "Starting Bux", "num", "1000",  scale=0.8, minMax=(1000, 100000))
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
                return [noOfDecks, difficulty, startingBux, noOfPlayers] # Returns list of all selected settings
            elif cancelButton.updateImage(event): # Checks if player pressed the cancel button
                return None # Retuns none passing over the If-Statement checking if the game is started
            pygame.display.flip() # Updates the screen with all the rects 

def newGame(noOfDecks, difficulty, noOfNPCs, startingBux):
    # Button setup that requires vairables: Bet Amount
    game = playGame(noOfDecks, difficulty, noOfNPCs, startingBux)
    playingGame(game)
    

# Main Game Loop
gameRunning = True
while gameRunning: # Main Menu Loop
    screen.blit(bg, (0,0)) # Set the screen as my background
    for event in pygame.event.get(): #Checking for events
        if event.type == pygame.QUIT: # If the user presses the X button, quit game
            gameRunning = False
        # By updating the image on an event I can limit the amount of checks my code makes, additionally I can make it so you only press one button at a time
        if newGameButton.updateImage(event):
            gameSettings = newGameSettings() # Opens teh new game mini window
            if gameSettings is not None: # If it is none they cancelled new game
                # Settings the values of the selected settings - Neater function call
                noOfDecks = gameSettings[0]
                difficulty = gameSettings[1]
                startingBux = gameSettings[2]
                noOfNPCs = gameSettings[3]
                newGame(noOfDecks, difficulty, noOfNPCs, startingBux) # Creating the game with the selected settings
        elif continueButton.updateImage(event):
            pass
        elif settingsButton.updateImage(event):
            pass
        elif quitButton.updateImage(event):
            gameRunning = False
        pygame.display.flip() # Update the screen
    
    
    
pygame.quit # Exit out of Pygame

