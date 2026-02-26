import pygame
from pygameUtils.buttonUtils import button, discreteSlider, inputBox
from gameLogic import playGame

## SHORT TERM GOALS
# TODO Handle if player ges 21 or if player gets blackjack - Semi Done
# TODO Handle deck running out of cards somehow
# TODO Handle player running out of bustBux
# TODO Fix infinite money glitch - use a set of owed players each element [playerObj, "Won"/"Draw"]
# TODO See if I can make it so the screen can update the cards n such without needing an event??? Probs alot of rewriting

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
    # Creating the bet amount input box
    global currentPlayerIndex
    minBet = round((int(game.startingBux)/100)/5)*5 # Rounds the minimum bet to the nearest 5, so the minimum bet will always be 1% of the starting bux to the nearest 5
    betAmountInputBox = inputBox(screen, (centreX, 770), "Bet Amount:", "num", f"{minBet}", interactable=False, minMax=[float(minBet), 1000*float(minBet)])
    # Game Status variables
    gamePlayRunning = True
    bettingPhase = True
    currentPlayerIndex = 0
    dealer = game.players[len(game.players) -1] # Dealer is always this index
    
    def endPlayerTurn():
        global currentPlayerIndex
        currentPlayerIndex += 1 # Moves to next player
        # Make all buttons uninteractable
        hitButton.makeUninteractable()
        standButton.makeUninteractable()
        splitButton.makeUninteractable()
        insuranceButton.makeUninteractable()
        
    def startPlayerTurn(currentPlayer, event):
        # Check if player has natural blackjack
        hitButton.makeInteractable()
        standButton.makeInteractable()
        # Making actions available
        if len(currentPlayer.hand) > 2: # Special cases not available
            splitButton.makeUninteractable()
            insuranceButton.makeUninteractable()
        # Checks if player has natural blackjack
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
            if doubleDownButton.updateImage(event): # If the player hasn't acted they can double down
                currentPlayer.bustBux -= currentPlayer.bet # Remove the additional bet from their total
                currentPlayer.bet *= 2 # Double the bet
                # Usual card dealing process
                currentPlayer.dealCard(game.deckInstance)
                game.updateBet(currentPlayerIndex)
                print(currentPlayer.bet)
                if game.checkBusted(currentPlayer):
                    endPlayerTurn()
                    currentPlayer.bust(game)
    
    # Gameplay loop
    while gamePlayRunning:
        for event in pygame.event.get(): # Checking for events
            screen.blit(bg, (0,0)) # Set the screen as my background
            game.updateImage()
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
                    game.createPlayerBetTexts()
                else: # Current player is an NPC
                    playerBet = game.players[currentPlayerIndex].calculateBet()
                    currentPlayer.bet = playerBet
                    currentPlayerIndex += 1
            # Starting action phase
            if game.roundStarted:
                if currentPlayer.name == "Player": # Is the Player's turn
                    startPlayerTurn(currentPlayer, event)                
                    # Waiting for interactions
                    if standButton.updateImage(event):
                        currentPlayer.stand(game)
                        endPlayerTurn()
                    if hitButton.updateImage(event):
                        currentPlayer.dealCard(game.deckInstance)
                        if game.checkBusted(currentPlayer):
                            endPlayerTurn()
                            currentPlayer.bust(game)
                        elif game.checkBlackjack(currentPlayer):
                            currentPlayer.stand(game)

                elif currentPlayer.name == "Dealer": # Is the dealer's turn
                    # Handling the end of the game
                    currentPlayer.hand[1].setVisible()
                    if currentPlayer.isStood or game.checkBusted(currentPlayer): # Dealer has either stood or busted
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
                                else:
                                    pass
                        # Dealer has bust so every stood player wins
                        elif currentPlayer.isBusted:
                            for hand in list(game.stoodHands.keys()):
                                stoodPlayer = game.stoodHands[hand]
                                stoodPlayer.bustBux += 2*stoodPlayer.bet
                                # TODO handle end of round
                        # Waiting for player to be ready for the next round
                        if nextRoundButton.updateImage(event):
                            # Reset game
                            currentPlayerIndex = 0
                            game.bustPlayers = 0
                            game.stoodHands = {}
                            game.betTexts = []
                            game.roundStarted = False
                            bettingPhase = True
                            for player in game.players:
                                player.newRound()
                    elif currentPlayer.handValue < 17 and len(game.players)-1 != game.bustPlayers and len(game.stoodHands) != 0: # If dealer's hand is below 17 must hit, do not hit if all players are bust or all players have blackjack
                        currentPlayer.dealCard(game.deckInstance)
                    else:
                        currentPlayer.stand(game)
                # NPC's turn
                else:
                    if currentPlayer.isStood or currentPlayer.isBusted:
                        currentPlayerIndex += 1
        # Initial deal happens once, after betting
        if bettingPhase == False:
            if game.roundStarted == False:
                game.initialDeal()
                game.stoodHands = {} # Reset stood hand
                game.drawPlayerTexts()  # Draw player names
                game.drawPlayerBets() # Draw player bets
        
        pygame.display.update() 
        clock.tick(60) # Limiting clock to 60        
