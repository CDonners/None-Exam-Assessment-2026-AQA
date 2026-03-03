import pygame
from pygameUtils.buttonUtils import button, discreteSlider, inputBox
from gameLogic import playGame

# ! SHORT TERM GOALS !
# TODO Handle deck running out of cards somehow
# TODO Handle player running out of bustBux
# TODO Show a text saying player Won/Lost/Pushq
# TODO Add insurance - Will just be an if statement and a variable
# TODO Add split - Will use 2D list, need to add checks for integration
# TODO Detect natural blackjack not working
# TODO Need to add that soft numbers are worse than none-soft numbers

# Pygame Setup
pygame.init() # Initialise Pygame
INITX = 1400
INITY = 900
INITIALSIZE = (INITX, INITY) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/table.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen
clock = pygame.time.Clock() # To limit FPS

# Menu Button Setup
centreX = INITX//2 # X is always centre no matter the initial size
centreY = INITY//2
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
doubleDownButton = button(screen, (centreX, centreY), "Double Down")
nextRoundButton = button(screen, (centreX, centreY), "Next Round")

def playingGame(game):
    global currentPlayerIndex
    global showDBButton
    # Creating the bet amount input box
    minBet = round((int(game.startingBux)/100)/5)*5 # Rounds the minimum bet to the nearest 5, so the minimum bet will always be 1% of the starting bux to the nearest 5
    betAmountInputBox = inputBox(screen, (centreX, 770), "Bet Amount:", "num", f"{minBet}", interactable=False, minMax=[float(minBet), 1000*float(minBet)])
    # Game State variables
    gamePlayRunning = True
    bettingPhase = True
    nextRound = False
    showDBButton = False
    currentPlayerIndex = 0
    betsGiven = False
    # Player state variables
    betMade = False
    playerBet = 0
    hit = False
    stood = False
    # Game action delay (in frames at 60 FPS)
    gameActionDelay = 30  # 1 second at 60 FPS
    gameAct = 0
    # Utility
    dealer = game.players[len(game.players) -1] # Dealer is always this index
    
    def endPlayerTurn():
        global currentPlayerIndex
        currentPlayerIndex += 1 # Moves to next player
        # Make all buttons uninteractable
        hitButton.makeUninteractable()
        standButton.makeUninteractable()
        splitButton.makeUninteractable()
        insuranceButton.makeUninteractable()
        confirmBetButton.makeUninteractable()
        betAmountInputBox.makeUninteractable()
        
    def startPlayerTurn(currentPlayer, event):
        global showDBButton
        # Check if player has natural blackjack
        hitButton.makeInteractable()
        standButton.makeInteractable()
        # Making actions available
        if len(currentPlayer.hand) > 2: # Special cases not available
            splitButton.makeUninteractable()
            insuranceButton.makeUninteractable()
            if game.checkBlackjack(currentPlayer):
                currentPlayer.stand(game)
                endPlayerTurn()
        # Checks if player has natural blackjack as they have 2 cards
        elif game.checkBlackjack(currentPlayer):
            currentPlayer.bustBux += 2.5*currentPlayer.bet
            endPlayerTurn()
        else: # Need to check if special cases are available
            # Check's if split is available
            if currentPlayer.hand[0].face == currentPlayer.hand[1].face: # If player's cards are equal
                splitButton.makeInteractable()
            # Checks if insurance is available
            if dealer.hand[0].face == "A": # If the dealer has a visible Ace
                insuranceButton.makeInteractable()
            # Makes double down available
            showDBButton = True
            if doubleDownButton.updateImage(event): # If the player hasn't acted they can double down
                showDBButton = False
                currentPlayer.bustBux -= currentPlayer.bet # Remove the additional bet from their total
                currentPlayer.bet *= 2 # Double the bet
                # Usual card dealing process
                currentPlayer.dealCard(game.deckInstance)
                game.updateBet(currentPlayerIndex)
                if game.checkBusted(currentPlayer):
                    currentPlayer.bust(game)
                endPlayerTurn()
    
    # Gameplay loop
    while gamePlayRunning:
        screen.blit(bg, (0,0)) # Set the screen as my background
        currentPlayer = game.players[currentPlayerIndex]
        for event in pygame.event.get(): # Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            # # Draw buttons
            hitButton.updateImage(event)
            standButton.updateImage(event)
            splitButton.updateImage(event)
            insuranceButton.updateImage(event)
            confirmBetButton.updateImage(event)
            # State Machine for gameplay
            if bettingPhase: # If betting phase is active
                if currentPlayer.name == "Player": # Checks if current player is the human player
                    # Make the relevant interactables be interactable
                    betAmountInputBox.setMax(currentPlayer.bustBux)
                    playerBet = int(betAmountInputBox.getInput(event))
                    betMade = confirmBetButton.updateImage(event)
                    
            # Starting action phase
            elif game.roundStarted:
                if currentPlayer.name == "Player":
                    startPlayerTurn(currentPlayer, event)
                    hit = hitButton.updateImage(event)
                    stood = standButton.updateImage(event)
                elif currentPlayer.name == "Dealer":
                    if currentPlayer.isStood or game.checkBusted(currentPlayer):
                        nextRound = nextRoundButton.updateImage(event)
                        
        if bettingPhase: # If betting phase is active
            if currentPlayer.name == "Player": # Checks if current player is the human player
                # Make the relevant interactables be interactable
                confirmBetButton.makeInteractable()
                betAmountInputBox.makeInteractable()
                if betMade: # Bet confirmed
                    currentPlayer.bet = playerBet
                    currentPlayer.bustBux -= playerBet
                    currentPlayerIndex += 1 # Increment player index
                    # Make buttons uninteractable
                    confirmBetButton.makeUninteractable()
                    betAmountInputBox.makeUninteractable()
                    betMade = False
            elif currentPlayer.name == "Dealer": # Checks if the current player is the dealer - Signals end of betting phase
                currentPlayerIndex = 0
                bettingPhase = False
                game.createPlayerBetTexts()
                game.initialDeal()
                game.stoodHands = {} # Reset stood hand
                game.drawPlayerTexts()  # Draw player names
                game.drawPlayerBets() # Draw player bets
            else: # Current player is an NPC
                gameAct += 1
                if gameAct == gameActionDelay:
                    playerBet = game.players[currentPlayerIndex].calculateBet()
                    currentPlayer.bet = playerBet
                    currentPlayerIndex += 1
                    gameAct = 0
        
        elif game.roundStarted:
            if currentPlayer.name == "Player": # Is the Player's turn               
                # Wait for interactions
                if stood:
                    showDBButton = False
                    currentPlayer.stand(game)
                    endPlayerTurn()
                    stood = False                                               
                if hit:
                    showDBButton = False
                    currentPlayer.dealCard(game.deckInstance)
                    if game.checkBusted(currentPlayer):
                        endPlayerTurn()
                        currentPlayer.bust(game)
                    elif game.checkBlackjack(currentPlayer):
                        currentPlayer.stand(game)
                        endPlayerTurn()
                    hit = False

            elif currentPlayer.name == "Dealer": # Is the dealer's turn
                gameAct += 1  # Increment frame counter
                dealer = currentPlayer # Making it more clear that we are talking about dealer
                dealer.hand[1].setVisible() # Show the dealer's down card
                # Checking the players have won and paying them
                if dealer.isStood or game.checkBusted(dealer): # Dealer has either stood or busted
                    if dealer.isStood and not betsGiven: # Once dealer has stood if bets haven't been paid
                        for hand in list(game.stoodHands.keys()): # Loop through the list of stoof hands
                            stoodPlayer = game.stoodHands[hand]
                            if dealer.handValue == hand:
                                stoodPlayer.bustBux += stoodPlayer.bet
                                # TODO handle end of round
                            elif dealer.handValue < hand:
                                stoodPlayer.bustBux += 2*stoodPlayer.bet
                                # TODO handle end of round
                            # If player doesn't enter either of these, player has lost
                        betsGiven = True
                    # Dealer has bust so every stood player wins
                    elif dealer.isBusted and not betsGiven:
                        for hand in list(game.stoodHands.keys()):
                            stoodPlayer = game.stoodHands[hand]
                            stoodPlayer.bustBux += 2*stoodPlayer.bet
                        betsGiven = True
                            # TODO handle end of round
                    # Waiting for player to be ready for the next round
                    if nextRound:
                        # Reset game
                        gameAct = 0
                        currentPlayerIndex = 0
                        game.bustPlayers = 0
                        game.stoodHands = {}
                        game.betTexts = []
                        game.roundStarted = False
                        bettingPhase = True
                        betsGiven = False
                        for player in game.players:
                            player.newRound()
                elif dealer.handValue < 17 and len(game.players)-1 != game.bustPlayers and len(game.stoodHands) != 0: # If dealer's hand is below 17 must hit
                    # Don't hit if everyone is bust or has natural blackjack
                    if gameAct == gameActionDelay:
                        gameAct = 0
                        dealer.dealCard(game.deckInstance)
                        if game.checkBusted(currentPlayer):
                            currentPlayer.bust(game)
                else:
                    dealer.stand(game)
            # NPC's turn
            else:
                if currentPlayer.isStood or currentPlayer.isBusted:
                    currentPlayerIndex += 1
        # Keeping all buttons on screen
        if currentPlayer.name == "Dealer":
            if currentPlayer.isStood or game.checkBusted(currentPlayer):
                nextRound = nextRoundButton.draw()
        if showDBButton:
            doubleDownButton.draw()
        hitButton.draw()
        standButton.draw()
        splitButton.draw()
        insuranceButton.draw()
        confirmBetButton.draw()
        betAmountInputBox.draw()
        game.updateImage()
        pygame.display.update() 
        clock.tick(60) # Limiting clock to 60        

def newGameSettings():
    # Mini Window Setup
    miniWindowImage = pygame.image.load("bankrollBust/images/MiniMenu.png") # Loading the mini window image
    miniWindowRect = miniWindowImage.get_rect(center=(INITX/2, INITY/2)) # Dynamically centering the window
    # Interaction Setup
    currentX = miniWindowRect.centerx # Making my function calls shorter - Neater code :)
    currentY = miniWindowRect.centery
    noOfDecksSlider = discreteSlider(screen, "Number Of Decks:", (currentX, currentY-150), [4,6,8,10,12,16], scale=1.3)
    difficultySlider = discreteSlider(screen, "Difficulty:", (currentX, currentY-100), ["Full-Assist", "Semi-Assist", "There-When-Needed","No-Help"], scale=1.3)
    noOfNPCsSlider = discreteSlider(screen, "Number of NPCs:", (currentX, currentY-50), [0,1,2,3,4,5,6], scale=1.3)
    startingBuxInput = inputBox(screen, (currentX, currentY+25), "Starting Bux:", "num", "1000",  scale=0.8, minMax=(1000, 100000))
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
    game = playGame(noOfDecks, difficulty, noOfNPCs, startingBux, screen)
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
    clock.tick(60) # Limiting clock to 60
    
    
    
pygame.quit # Exit out of Pygame
