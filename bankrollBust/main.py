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
confirmBetButton = button(screen, (centreX, 850), "Confirm Bet", interactable=False)

def playingGame(game):
    # Creating the bet amount input box
    minBet = round((int(game.startingBux)/100)/5)*5 # Rounds the minimum bet to the nearest 5, so the minimum bet will always be 1% of the starting bux to the nearest 5
    betAmountInputBox = inputBox(screen, (centreX, 770), "Bet Amount", "num", f"{minBet}", interactable=False, minMax=[float(minBet), 1000*float(minBet)])
    betAmount = None
    # Game Status variables
    gamePlayRunning = True
    bettingPhase = True
    currentPlayerIndex = 0
    dealer = game.players[len(game.players) -1] # Dealer is always this index
    # Gameplay loop
    while gamePlayRunning:
        screen.blit(bg, (0,0)) # Set the screen as my background
        for event in pygame.event.get(): # Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            # Draw buttons
            hitButton.updateImage(event)
            standButton.updateImage(event)
            splitButton.updateImage(event)
            insuranceButton.updateImage(event)
            confirmBetButton.draw()
            betAmountInputBox.draw()
            # State Machine for gameplay
            currentPlayer = game.players[currentPlayerIndex]
            if bettingPhase: # If betting phase is active
                if currentPlayer.name == "Player": # Checks if current player is the human player
                    # Make the relevant interactables be interactable
                    confirmBetButton.makeInteractable()
                    betAmountInputBox.makeInteractable()
                    playerBet = int(betAmountInputBox.getInput(event))
                    if confirmBetButton.updateImage(event): # Bet confirmed
                        currentPlayer.bet = playerBet
                        currentPlayer.bustBux -= playerBet
                        currentPlayerIndex += 1 # Increment player index
                        # Make buttons uninteractable
                        confirmBetButton.makeUninteractable()
                        betAmountInputBox.makeUninteractable()
                        confirmBetButton.updateImage(event) # Updating the image of the button properly
                elif currentPlayer.name == "Dealer": # Checks if the current player is the dealer - Signals end of betting phase
                    currentPlayerIndex = 0
                    bettingPhase = False
                else: # Current player is an NPC
                    playerBet = game.players[currentPlayerIndex].calculateBet()
                    currentPlayer.bet = playerBet
                    currentPlayerIndex += 1
            # Starting action phase
            if game.roundStarted:
                if currentPlayer.name == "Player": # Is the Player's turn
                    # Making actions available
                    if len(currentPlayer.hand) > 2: # Special cases not available
                        splitButton.makeUninteractable()
                        insuranceButton.makeUninteractable()
                    else: # Need to check if special cases are available
                        if currentPlayer.hand[0].face == currentPlayer.hand[1].face: # If player's cards are equal
                            splitButton.makeInteractable()
                        if dealer.hand[0].face == "A": # If the dealer has a visible Ace
                            insuranceButton.makeInteractable()
                    hitButton.makeInteractable()
                    standButton.makeInteractable()
                    # Checks if player's round is over 
                    if currentPlayer.isStood or currentPlayer.isBusted:
                        currentPlayerIndex += 1 # Moves to next player
                        # Make all buttons uninteractable
                        hitButton.makeUninteractable()
                        standButton.makeUninteractable()
                        splitButton.makeUninteractable()
                        insuranceButton.makeUninteractable()
                    # Waiting for interactions
                    if standButton.updateImage(event):
                        currentPlayer.stand()
                        game.stoodHands[currentPlayer.handValue] = currentPlayer # Adding the stood hand to the dictionary
                    if hitButton.updateImage(event):
                        currentPlayer.dealCard(game.deckInstance)
                        game.getHandValue(currentPlayer)

                elif currentPlayer.name == "Dealer": # Is the dealer's turn
                    # Handling the end of the game
                    if currentPlayer.isStood or currentPlayer.isBusted: # Dealer has either stood or busted
                        if currentPlayer.isStood: # Once dealer has stood
                            for hand in list(game.stoodHands.keys()):
                                stoodPlayer = game.stoodHands[hand]
                                if currentPlayer.handValue == hand:
                                    stoodPlayer.bustBux += stoodPlayer.bet
                                    # TODO handle end of round
                                elif currentPlayer.handValue < hand:
                                    stoodPlayer.bustBux += 2*stoodPlayer.bet
                                    # TODO handle end of round
                                # If player doesn't enter either of these, player has lost
                        # Dealer has bust so every stood player wins
                        elif currentPlayer.isBusted:
                            for hand in list(game.stoodHands.keys()):
                                stoodPlayer = game.stoodHands[hand]
                                stoodPlayer.bustBux += 2*stoodPlayer.bet
                                # TODO handle end of round
                        # Reset game
                        currentPlayerIndex = 0
                        game.roundStarted = False
                        bettingPhase = False
                        for player in game.players:
                            player.newRound()
                    if currentPlayer.handValue < 17:
                        currentPlayer.dealCard()
                        game.getHandValue(currentPlayer)
                    else:
                        currentPlayer.stand()

                else: # Is NPC's turn
                    if currentPlayer.isStood or currentPlayer.isBusted:
                        currentPlayerIndex += 1
            game.updateImage()
            pygame.display.flip()
    
        # Initial deal happens once, after betting
        if bettingPhase == False and game.roundStarted == False:
            game.initialDeal()
            game.stoodHands = {} # Reset stood hand
        

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

