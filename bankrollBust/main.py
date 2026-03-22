import pygame
from pygameUtils.buttonUtils import button, discreteSlider, inputBox
from gameLogic import playGame

# ! SHORT TERM GOALS !
# TODO Handle deck running out of cards somehow - Probably regenerate deck telling the player you have
# TODO Handle player running out of bustBux - End game as player lost

# ! Bugs ! 
# TODO Player order seems to be a bit wack?

# Pygame Setup
pygame.init() # Initialise Pygame
INITX = 1400
INITY = 900
INITIALSIZE = (INITX, INITY) # Set my initial window size
screen = pygame.display.set_mode(INITIALSIZE) # Create my screen
BGIMAGE = pygame.image.load("bankrollBust/images/table.png") # Load the background image
bg = pygame.transform.scale(BGIMAGE, INITIALSIZE) # Set the size of the background image to the size of the screen
clock = pygame.time.Clock() # To limit FPS
pygame.display.set_caption("Bankroll Bust") # Set the caption of the game

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
        screen.blit(bg, (0,0)) # Set the screen as my background
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
            game.UI.drawWinnings(game.playerAction.playerWinnings)
        if game.gameState.doubleDownAvailable:
            doubleDownButton.draw()
        pygame.display.update() 
        
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
            # Betting Phase
            if game.gameState.bettingPhase:
                if game.currentPlayer.isPlayer: # Checks if current player is the human player
                    # Make the relevant interactables be interactable
                    betAmountInputBox.setMax(game.currentPlayer.bustBux)
                    game.playerAction.potentialBet = int(betAmountInputBox.getInput(event))
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
                            currentHand = game.currentPlayer.hands[0]
                            game.currentPlayer.bustBux -= currentHand.bet # Remove the additional bet from their total
                            game.currentPlayer.totalBet += currentHand.bet
                            currentHand.bet *= 2
                            # Usual card dealing process
                            game.currentPlayer.dealCard(game)
                            game.currentPlayer.stand(game)
                            endPlayerTurn()
                            game.gameState.doubleDownAvailable = False
            elif game.gameState.roundOver:
                if nextRoundButton.updateImage(event):
                    game.endRound()

    def endPlayerTurn():
        # Make all buttons uninteractable
        hitButton.makeUninteractable()
        standButton.makeUninteractable()
        splitButton.makeUninteractable()
        insuranceButton.makeUninteractable()
        confirmBetButton.makeUninteractable()
        betAmountInputBox.makeUninteractable()

    def playerTurn():
            hitButton.makeInteractable()
            standButton.makeInteractable()
            dealerHand = dealer.hands[0]
            currentHand = game.currentPlayer.hands[game.currentPlayer.handIndex]
            # Making actions available
            if game.currentPlayer.canSplit(): # If player's cards are equal
                splitButton.makeInteractable()
            if game.gameState.insuranceAvailable and game.currentPlayer.insurance == 0: # If the dealer has a visible Ace
                insuranceButton.makeInteractable()
            # Player Stands
            if game.playerAction.stand:
                game.currentPlayer.stand(game) # Make the player stand
                game.playerAction.stand = False # Reset Player Action state         
            # Player Hits                    
            if game.playerAction.hit:
                game.currentPlayer.dealCard(game) # Deal a card
                game.playerAction.hit = False # Reset Player Action state  
            # Player Splits
            if game.playerAction.split:
                game.currentPlayer.splitHand() # Split the hands
                game.playerAction.split = False # Reset Player Action state  
                splitButton.makeUninteractable() # Split button no longer available
            # Player uses insurance
            if game.playerAction.insurance:
                game.currentPlayer.insurance = currentHand.bet/2
                game.currentPlayer.totalBet += currentHand.bet/2
                game.currentPlayer.bustBux -= currentHand.bet/2
                game.playerAction.insurance = False # Reset Player Action state  
                insuranceButton.makeUninteractable()
            game.isDoubleDownAvailable()
            game.isInsuranceAvailable()
            handInactive = currentHand.stood or currentHand.busted or currentHand.naturalBlackjack # If either of these conditions are true then a hand is inactive
            if len(game.currentPlayer.hands)-1 == game.currentPlayer.handIndex and handInactive:
                # Player has no more hands to player so move to the next
                endPlayerTurn()
   
    def playerBettingTurn():
        # Make the relevant interactables be interactable
        confirmBetButton.makeInteractable()
        betAmountInputBox.makeInteractable()
        if game.playerAction.betMade: # Bet confirmed
            game.currentPlayer.makeBet(game.playerAction.potentialBet)
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
    
    def payOut():
        dealerHand = dealer.hands[0]
        for player in game.players:
            if not player.isDealer:
                bustBuxPayOut = 0
                if dealerHand.naturalBlackjack: # No one can win unless they have natural blackjack
                    if player.hands[0].naturalBlackjack: # Player can only have natural blackjack on one hand
                        bustBuxPayOut += player.hands[0].bet * 2.5
                    bustBuxPayOut += 2 * player.insurance
                else:
                    for hand in player.hands:
                        if hand.naturalBlackjack: # Hand has natural blackjack - Does not matter if dealer busted/stood always pays out
                            bustBuxPayOut += hand.bet * 2.5
                        elif dealerHand.busted: # All stood players win
                            if hand.stood:
                                bustBuxPayOut += hand.bet * 2
                        elif not hand.busted: # Compare players hand value with dealer's hand value
                            if hand.handValue > dealerHand.handValue: # Hand won
                                bustBuxPayOut += hand.bet * 2
                            elif hand.handValue == dealerHand.handValue: # Possible Push
                                multiplier = handlePush(hand.cards, dealerHand.cards)
                                bustBuxPayOut += hand.bet * multiplier
                            else: # Player Lost
                                pass # Nothing needs to be handled
                if player.isPlayer:
                    profit = bustBuxPayOut - player.totalBet  # Only the net profit
                    player.winnings += profit
                    player.bustBux += bustBuxPayOut
                    game.playerAction.playerWinnings += player.winnings
        game.gameState.payedOut = True

    # Gameplay loop
    while gamePlayRunning:
        events = pygame.event.get()
        eventHandler(events)
        game.currentPlayer = game.players[game.playerIndex]
        if game.gameState.bettingPhase: # If betting phase is active
            # Player's betting turn
            if game.currentPlayer.isPlayer:
                playerBettingTurn()
            # End of betting phase
            elif game.currentPlayer.isDealer:
                game.gameState.bettingPhase = False
                game.gameState.roundStarted = True
                game.playerIndex = 0
                game.initialDeal() # Do the initial Deal
            # NPC's betting turn
            else:
                game.playerIndex += 1
                # gameAct += 1
                # if gameAct >= gameActionDelay//2:
                #     pass
        # Round Started
        elif game.gameState.roundStarted:
            # Player's Turn
            if game.currentPlayer.isPlayer:
                playerTurn()        
            # Dealers Turn
            elif game.currentPlayer.isDealer:
                gameAct += 1  # Increment frame counter
                dealerHand = dealer.hands[0]
                # Dealer moves when delay is over
                if gameAct >= gameActionDelay:
                    # Show the dealer's down card
                    if not dealerHand.cards[1].visible:
                        dealerHand.cards[1].setVisible() 
                        game.increaseCount(dealerHand.cards[1]) # Increase the count now that we can see the card
                    # Ends Round as dealer's turn finished
                    elif dealerHand.stood or dealerHand.busted:
                        # Once dealer has stood if bets haven't been paid
                        if not game.gameState.payedOut: 
                            payOut()
                        game.gameState.roundOver = True
                        game.gameState.roundStarted = False
                    # Dealer turn to decide
                    elif game.hasActiveHands():
                        # Don't hit if there are no active hands
                        dealerAction = dealer.decideNextMove()
                        if dealerAction == "hit":
                            dealer.dealCard(game)
                        elif dealerAction == "stand":
                            dealer.stand(game)
                    else:
                        dealer.stand(game)
                    # Reset action timer
                    gameAct = 0
            # NPC's turn
            else:
                gameAct += 1
                if gameAct == gameActionDelay:
                    NPCAction = game.currentPlayer.decideNextMove(game)
                    if NPCAction == "hit":
                        game.currentPlayer.dealCard(game)
                    elif NPCAction == "stand":
                        game.currentPlayer.stand(game)
                    elif NPCAction == "split":
                        game.currentPlayer.splitHand()
                    gameAct = 0
        drawScreen()
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
    noOfNPCsSlider = discreteSlider(screen, "Number of NPCs:", (currentX, currentY-50), [0,1,2,3,4], scale=1.3)
    startingBuxInput = inputBox(screen, (currentX, currentY+25), "Starting Bux:", "num", "1000",  scale=0.8, minMax=(1000, 100000))
    startButton = button(screen, (currentX+135, currentY+125), "Start Game", scale=0.7)
    cancelButton = button(screen, (currentX-135, currentY+125), "Cancel", scale=0.7)
    debugMode = False
    # Keeping Window Open
    started = False
    while not started:
        for event in pygame.event.get(): #Checking for events
            if event.type == pygame.QUIT: # If the user presses the X button, quit game
                quit()
            elif event.type == pygame.KEYDOWN:
                # --- DEBUGGING PURPOSES --- #
                if event.key == pygame.K_F10:
                    debugMode = True if not debugMode else False # Toggle debug mode
                    if debugMode:
                        pygame.display.set_caption("Bankroll Bust -- DEBUGGING")
                    else:
                        pygame.display.set_caption("Bankroll Bust")
                # -------------------------- #
            screen.blit(miniWindowImage, miniWindowRect) # Draws the mini window onto the screen
            noOfDecks = noOfDecksSlider.getValue(event) # Get the value from the slider -- See buttonUtils.py
            difficulty = difficultySlider.getValue(event) # Get the value from the slider -- See buttonUtils.py
            noOfPlayers = noOfNPCsSlider.getValue(event) # Get the value from the slider -- See buttonUtils.py
            startingBux = startingBuxInput.getInput(event) # Get the value of the input box -- See buttonUtils.py
            if startButton.updateImage(event): # Checking if User has pressed the start button
                started = True # Sets started to true breaking the loop
                # Returns list of all selected settings
                return {"noOfDecks":noOfDecks,
                        "difficulty":difficulty,
                        "startingBux":startingBux,
                        "noOfNPCs":noOfPlayers,
                        "debugMode": debugMode} 
            elif cancelButton.updateImage(event): # Checks if player pressed the cancel button
                return None # Retuns none passing over the If-Statement checking if the game is started
            pygame.display.flip() # Updates the screen with all the rects 

def newGame(noOfDecks, difficulty, noOfNPCs, startingBux, debugMode):
    # Button setup that requires vairables: Bet Amount
    game = playGame(screen, noOfDecks, difficulty, noOfNPCs, startingBux, debugMode)
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
                newGame(**gameSettings) # Creating the game with the selected settings
        elif continueButton.updateImage(event):
            pass
        elif settingsButton.updateImage(event):
            pass
        elif quitButton.updateImage(event):
            gameRunning = False
        pygame.display.flip() # Update the screen
    clock.tick(60) # Limiting clock to 60
    
    
    
pygame.quit() # Exit out of Pygame
