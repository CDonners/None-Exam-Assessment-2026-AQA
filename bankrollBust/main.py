import pygame
from pygameUtils.buttonUtils import button, discreteSlider, inputBox
from gameLogic import playGame

# ! SHORT TERM GOALS !
# TODO Handle deck running out of cards somehow - Probably regenerate deck telling the player you have
# TODO Handle player running out of bustBux - End game as player lost
# TODO Implement Next round
# TODO Implement displaying winnings at end of round - game.UI.drawWinnings
# TODO Display hand status(Bust, stood, push) on the cards - game.UI.drawHands
### ! Hand is now a class make it so everywhere ! ###

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
centreX = INITX//2
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
confirmBetButton = button(screen, (centreX, 850), "Confirm Bet", interactable=True)
doubleDownButton = button(screen, (centreX, centreY), "Double Down")
nextRoundButton = button(screen, (centreX, centreY), "Next Round")

def playingGame(game):
    # Creating the bet amount input box
    minBet = round(game.startingBux * 0.01 / 5) * 5 # Rounds the minimum bet to the nearest 5, so the minimum bet will always be 1% of the starting bux to the nearest 5
    betAmountInputBox = inputBox(screen, (centreX, 770), "Bet Amount:", "num", f"{minBet}", interactable=False, minMax=[float(minBet), 1000*float(minBet)])
    # Game State variables
    gamePlayRunning = True
    # Game action delay (in frames at 60 FPS)
    gameActionDelay = 30  # 1 second at 60 FPS
    gameAct = 0
    # Utility
    dealer = game.players[len(game.players) -1] # Dealer is always this index
    
    def drawScreen():
        game.handleUI()
        hitButton.draw()
        standButton.draw()
        splitButton.draw()
        insuranceButton.draw()
        confirmBetButton.draw()
        betAmountInputBox.draw()
        # Keep conditional buttons on screen when applicable
        if game.gameState.roundOver:
            nextRoundButton.draw()
        if game.gameState.doubleDownAvailable:
            doubleDownButton.draw()
        
    def eventHandler(events):
        for event in events: # Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            # Update buttons
            hitButton.updateImage(event)
            standButton.updateImage(event)
            splitButton.updateImage(event)
            insuranceButton.updateImage(event)
            confirmBetButton.updateImage(event)
            # State Machine for gameplay
            if game.gameState.bettingPhase: # If betting phase is active
                if game.currentPlayer.isPlayer: # Checks if current player is the human player
                    # Make the relevant interactables be interactable
                    betAmountInputBox.setMax(game.currentPlayer.bustBux)
                    game.currentPlayer.totalBet = int(betAmountInputBox.getInput(event))
                    game.playerAction.betMade = confirmBetButton.updateImage(event)
            # Starting action phase
            elif game.gameState.roundStarted:
                if game.currentPlayer.isPlayer:
                    playerTurn()
                    game.playerAction.hit = hitButton.updateImage(event)
                    game.playerAction.stand = standButton.updateImage(event)
                    game.playerAction.split = splitButton.updateImage(event)
                    game.playerAction.insurance = insuranceButton.updateImage(event)
                    if game.gameState.doubleDownAvailable:
                        if doubleDownButton.updateImage(event): # If the player hasn't acted they can double down
                            game.currentPlayer.bustBux -= game.currentPlayer.totalBet # Remove the additional bet from their total
                            game.currentPlayer.totalBet *= 2 # Double the bet
                            # Usual card dealing process
                            game.currentPlayer.dealCard(game)
                            game.currentPlayer.stand(game)
                            endPlayerTurn()

                        
                elif game.currentPlayer.isDealer:
                    if dealerHand.stood or dealerHand.busted:
                        nextRound = nextRoundButton.updateImage(event)

    def startNewRound():
        # Resets game state variables
        gameAct = 0
        game.playerIndex = 0
        game.bustPlayers = 0
        game.gameState.roundStarted = False
        game.gameState.roundOver = False
        game.gameState.bettingPhase = True
        game.gameState.payedOut = False
        # Resetting players
        game.playerAction.betMade = False
        for player in game.players:
            player.newRound()

    def endPlayerTurn():
        game.currentPlayer.winnings -= game.currentPlayer.totalBet
        # Make all buttons uninteractable
        hitButton.makeUninteractable()
        standButton.makeUninteractable()
        splitButton.makeUninteractable()
        insuranceButton.makeUninteractable()
        confirmBetButton.makeUninteractable()
        betAmountInputBox.makeUninteractable()

    def playerTurn():
        game.isDoubleDownAvailable()
        hitButton.makeInteractable()
        standButton.makeInteractable()
        dealerHand = dealer.hands[0]
        # Making actions available
        if game.currentPlayer.checkBlackjack(game):
            game.currentPlayer.bustBux += 2.5*game.currentPlayer.totalBet
            endPlayerTurn()
        else: 
            # Check's if split is available
            if game.currentPlayer.canSplit(): # If player's cards are equal
                splitButton.makeInteractable()
            if dealerHand.cards[0].face == "A": # If the dealer has a visible Ace
                insuranceButton.makeInteractable()

    def playerBettingTurn():
        # Make the relevant interactables be interactable
        confirmBetButton.makeInteractable()
        betAmountInputBox.makeInteractable()
        if game.playerAction.betMade: # Bet confirmed
            game.currentPlayer.makeBet(game.currentPlayer.totalBet)
            # Make buttons uninteractable
            confirmBetButton.makeUninteractable()
            betAmountInputBox.makeUninteractable()
            game.playerAction.betMade = False
            game.playerIndex += 1

    def handlePush(hand, dealerHand):
        # Returns the players earnings multiplier
        dealerHandValues = [card.value for card in dealerHand]
        handValues = [card.value for card in hand]
        if 11 in dealerHandValues and 11 in handValues: # Both have soft hand
            return 1 # Push
        elif 11 in dealerHandValues and 11 not in handValues: # Player has superior hand
            return 2 # Player Win
        elif 11 not in dealerHandValues and 11 in handValues: # Dealer has superior hand
            return 0
        else: # No one has 11
            return 1 # Push
    
    def payOut(): # TODO completely rehaul into payOut
        dealerHand = dealer.hands[0]
        for player in game.players:
            bustBuxPayOut = 0
            if dealerHand.naturalBlackjack: # No one can win unless they have natural blackjack
                if player.hands[0].naturalBlackjack: # Player can only have natural blackjack on one hand
                    bustBuxPayOut += player.hands[0].bet * 2.5
            else:
                for hand in player.hands:
                    if hand.naturalBlackjack: # Hand has natural blackjack - Does not matter if dealer busted/stood always pays out
                        bustBuxPayOut += hand.bet * 2.5
                    elif dealerHand.busted: # All stood players win
                        if hand.stood:
                            bustBuxPayOut += hand.bet * 2
                    else: # Compare players hand value with dealer's hand value
                        if hand.handValue > dealerHand.handValue: # Hand won
                            bustBuxPayOut += hand.bet * 2
                        elif hand.handValue == dealerHand.handValue: # Possible Push
                            multiplier = handlePush(hand.cards, dealerHand.cards)
                            bustBuxPayOut += hand.bet * multiplier
                        else: # Player Lost
                            pass # Nothing needs to be handled
            player.bustBux += bustBuxPayOut
            player.winnings += bustBuxPayOut
        game.gameState.payedOut = True

    # Gameplay loop
    while gamePlayRunning:
        game.currentPlayer = game.players[game.playerIndex]
        events = pygame.event.get()
        eventHandler(events)    
        if game.gameState.bettingPhase: # If betting phase is active
            if game.currentPlayer.isPlayer: # Checks if current player is the human player
                playerBettingTurn()
            elif game.currentPlayer.isDealer: # Checks if the current player is the dealer - Signals end of betting phase
                game.gameState.bettingPhase = False
                game.gameState.roundStarted = True
                game.initialDeal() # Do the initial Deal
                game.playerIndex = 0
            else: # Current player is an NPC
                gameAct += 1
                if gameAct >= gameActionDelay:
                    pass
        # Round Started
        elif game.gameState.roundStarted:
            # Player's Turn
            if game.currentPlayer.isPlayer:
                playerTurn()        
                # Player Stands
                if game.playerAction.stand:
                    game.currentPlayer.stand(game) # Make the player stand
                    if len(game.currentPlayer.hands) <= game.currentPlayer.handIndex:
                        # Player has no more hands to player so move to the next
                        endPlayerTurn()
                    game.playerAction.stand = False # Reset Player Action state         
                # Player Hits                    
                if game.playerAction.hit:
                    game.currentPlayer.dealCard(game) # Deal a card
                    if len(game.currentPlayer.hands) <= game.currentPlayer.handIndex:
                        # Player has no more hands to player so move to the next
                        endPlayerTurn()
                    game.playerAction.hit = False # Reset Player Action state  
                # Player Splits
                if game.playerAction.split:
                    game.currentPlayer.splitHand() # Split the hands
                    game.playerAction.split = False # Reset Player Action state  
                    splitButton.makeUninteractable() # Split button no longer available
                # Player uses insurance
                if game.playerAction.insurance:
                    game.currentPlayer.insurance = game.currentPlayer.totalBet/2
                    game.currentPlayer.bustBux -= game.currentPlayer.insurance
                    game.playerAction.insurance = False # Reset Player Action state  
                    insuranceButton.makeUninteractable()
            # Dealers Turn
            elif game.currentPlayer.isDealer:
                gameAct += 1  # Increment frame counter
                dealerHand = dealer.hands[0] # Keeping cleaner code
                dealerHand.cards[1].setVisible() # Show the dealer's down card
                dealer.checkBlackjack(game) # Check if dealer has blackjack
                if dealerHand.stood or dealerHand.busted: # Dealer has either stood or busted so round will end
                    # Once dealer has stood if bets haven't been paid
                    if not game.gameState.payedOut: 
                        payOut()
                    game.gameState.roundOver = True
                    # Waiting for player to be ready for the next round
                    if game.playerAction.nextRound:
                        pass

                elif len(game.players)-1 != game.bustPlayers and len(game.stoodHands) != 0:
                    # Don't hit if everyone is bust or has natural blackjack
                    if gameAct >= gameActionDelay:
                        dealerAction = dealer.decideNextMove()
                        if dealerAction == "hit":
                            dealer.dealCard(game)
                        elif dealerAction == "stand":
                            dealer.stand(game)
                        gameAct = 0
                else:
                    dealer.stand(game)
            # NPC's turn
            else:
                if game.currentPlayer.isStood or game.currentPlayer.isBusted:
                    pass
        screen.blit(bg, (0,0)) # Set the screen as my background
        drawScreen()
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
    
    
    
pygame.quit() # Exit out of Pygame
