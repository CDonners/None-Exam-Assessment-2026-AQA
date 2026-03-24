from deckLogic import deckHandling
from players import player, NPC, dealer
import pygame
from pygameUtils.rand import genRandInt, genRandFloat

NPCNAMES = ["Paul","Noel","Aniyah","Dalton","Mariah","Zeke","Jolie","Kristian","Brynlee","Dilan","Charlotte","Cory","Camila","Sonny","Martha","Quincy","Elliot","Blaze","Paola","Cain","Anya","Raylan","Emily","Jax","Lucy"]
NPCPERSONALITIES = []

class setupGame():
    def __init__(self, startingBux: int, noOfNPCs):
        self.startingBux = startingBux
        # User object
        self.user = player(startingBux) # Creating the player object
        # Create NPCs
        self.NPCs = [] # Preparing to make the NPCs
        self.usedNames = []
        if noOfNPCs != 0:
            for _ in range(noOfNPCs): # Repeats for how many NPCs there are
                self.NPCs.append(self.createNPC()) # Create the NPC
        self.players = self.NPCs[:] # A list for all the players, cloning the NPCs list
        self.userPosition = (len(self.NPCs))//2 # Get the index where the user will be
        self.players.insert(self.userPosition, self.user) # Insert the User object into the middle of the list with a left bias
        self.players.append(dealer()) # Adds the dealer to the end of the player list

    def createNPC(self):
        name = self.pickName()
        prosperity = self.generateProsperity()
        confidence = self.generateConfidence()
        experience = self.generateExperience()
        return NPC(name, self.startingBux, prosperity, confidence, experience)
    
    def pickName(self):
        # Picks am unused name from the NPC Names list
        pickedName = ""
        indexCorrect = False 
        while not indexCorrect: # Looping until a correct index is generated
            generatedIndex = genRandInt(8) # Generate an integer for the index
            if generatedIndex < len(NPCNAMES): # If the index is greater or equal to length of the names list, regenerate it.
                pickedName = NPCNAMES[generatedIndex] # Get the item at the index
                if pickedName not in self.usedNames:
                    indexCorrect = True
                    self.usedNames.append(pickedName)
        return pickedName

    def generateProsperity(self):
        # Must generate a float between 0.5-1.5
        generatedProsperity = genRandFloat(0.5, 1.5)
        return generatedProsperity
    
    def generateConfidence(self):
        # Must generate a float between 0.75-1.25
        generatedConfidence = genRandFloat(0.75, 1.25)
        return generatedConfidence

    def generateExperience(self):
        # Must generate a float between 0.5-1.5
        generatedExperience = genRandFloat(0.75, 1.50)
        return generatedExperience

class handleGameUI:
    def __init__(self, screen, playerSeats):
        self.screen = screen
        self.playerSeats = playerSeats
        # Fonts
        self.mainFont = pygame.font.SysFont("", 32)
        self.betFont = pygame.font.SysFont("", 28)
        self.playerFont = pygame.font.SysFont("", 32) # Sets the font to pygame default with size 22
        self.largeFont = pygame.font.SysFont("", 48)
        # Game Over Text
        self.gameOverTextSurface = self.largeFont.render(f"GAME OVER", True, (255, 0, 0)) # Creates text surface with colour black
        self.gameOverTextRect = self.gameOverTextSurface.get_rect(center=(700,300))
        # Out of Cards Text
        self.outOfCardsSurface = self.largeFont.render(f"DECK OUT OF CARDS", True, (255, 0, 0)) # Creates text surface with colour black
        self.outOfCardsTextRect = self.gameOverTextSurface.get_rect(center=(630,250))
        # Card dimensions
        self.cardWidth = 55
        self.cardHeight = 75
        self.cardSpacing = 7
        self.handSpacing = 15
        
    def drawGameOverText(self):
        self.screen.blit(self.gameOverTextSurface, self.gameOverTextRect)
        
    def drawOutOfCardsText(self):
        self.screen.blit(self.outOfCardsSurface, self.outOfCardsTextRect)
        
    def drawPlayerTexts(self, players):
        for playerObj in players:
            # Creating the text for the player
            playerTextSurface = self.playerFont.render(f"{playerObj.name}", True, (255, 255, 255)) # Creates text surface with colour black
            playerTextRect = playerTextSurface.get_rect(center=self.playerSeats[playerObj])
            self.screen.blit(playerTextSurface, playerTextRect)

    def drawPlayerBets(self, players):
        for playerObj in players:
            if not playerObj.isDealer:
                betCentre = (self.playerSeats[playerObj][0], self.playerSeats[playerObj][1]+25)
                betTextSurface = self.betFont.render(f"Bet: {playerObj.totalBet}", True, (255, 255, 255)) # Creates text surface with colour white
                betTextRect = betTextSurface.get_rect(center=betCentre)
                self.screen.blit(betTextSurface, betTextRect)

    def drawHandStatus(self, hand, centre):
        statusTextSurface = None
        if hand.busted:
            statusTextSurface = self.mainFont.render("Busted", True, "black")
        elif hand.naturalBlackjack:
            statusTextSurface = self.mainFont.render("BLACKJACK", True, "black")
        elif hand.stood:
            statusTextSurface = self.mainFont.render("Stood", True, "black")
        elif hand.push:
            statusTextSurface = self.mainFont.render("Push", True, "black")
        if statusTextSurface:  # Only draw if something exists
            statusTextRect = statusTextSurface.get_rect(center=centre)
            self.screen.blit(statusTextSurface, statusTextRect)

    def drawHand(self, playerObj):
        hands = list(reversed(playerObj.hands))
        if not hands:
            return
        # Calculate widths for each hand and total width
        handWidths = []
        totalWidth = 0
        for hand in hands:
            numCards = len(hand.cards)
            width = numCards * self.cardWidth + max(0, (numCards - 1) * self.cardSpacing)
            handWidths.append(width)
            totalWidth += width
        # Add spacing between hands
        totalWidth += (len(hands) - 1) * self.handSpacing

        # Starting X for centered hands
        centerX = self.playerSeats[playerObj][0]
        startX = centerX - totalWidth // 2 + self.cardWidth//2 # Accounts for width of cards
        currentX = startX

        # Draw each hand
        for i, hand in enumerate(hands):
            handWidth = handWidths[i]
            handCenterX = currentX + handWidth // 2 - self.cardWidth//2 # Acounts for card width
            handCenterY = self.playerSeats[playerObj][1] # Middle of hand is over seat

            # Determine if this hand is active
            handActive = (playerObj.handIndex == len(hands)-1-i)

            # Draw cards in the hand
            for j, card in enumerate(hand.cards):
                x = currentX + j * (self.cardWidth + self.cardSpacing)
                y = self.playerSeats[playerObj][1] - 60  # Center of card over the seat
                colourIndex = len(hands) - 1 - i  # Rightmost hand black
                card.drawCard(self.screen, (x, y), colourIndex=colourIndex, active=handActive)

            # Draw hand status above cards
            if hand.cards:
                statusY = self.playerSeats[playerObj][1] - self.cardHeight - 30
                self.drawHandStatus(hand, (handCenterX, statusY))

            # Move X to next hand
            currentX += handWidth + self.handSpacing

    def drawBalance(self, players):
        targetPlayer = next(playerObj for playerObj in players if playerObj.isPlayer)
        playerBalance = targetPlayer.bustBux
        balanceTopLeft = (25,15)
        balanceTextSurface = self.mainFont.render(f"Balance:{playerBalance}", True, (0, 0, 0)) # Creates text surface with colour black
        balanceTextRect = balanceTextSurface.get_rect(topleft=balanceTopLeft)
        self.screen.blit(balanceTextSurface, balanceTextRect)   
        
    def drawWinnings(self, winnings):
        # Assume player made nothing
        textSurface = self.mainFont.render(f"Broke Even", True, (0, 0, 0)) # Creates text surface with colour black 
        if winnings > 0: # Player won BustBux
            textSurface = self.mainFont.render(f"Won: {winnings}", True, (0, 0, 0)) # Creates text surface with colour black
        elif winnings < 0: # Player lose BustBux
            textSurface = self.mainFont.render(f"Lost: {winnings*-1}", True, (0, 0, 0)) # Creates text surface with colour black
        # Create the text rect
        textRect = textSurface.get_rect(center=(700,350))
        self.screen.blit(textSurface, textRect)
        
    def updateImage(self, players):
        for player in players:
            self.drawHand(player)
        self.drawPlayerTexts(players)
        self.drawBalance(players)
        self.drawPlayerBets(players)

class gameStates: # TODO Clean and comment
    # Game States
    gamePlayRunning = True
    gameOver = False
    deckOutOfCards = False
    bettingPhase = True
    roundStarted = False
    roundOver = False
    payedOut = False
    NPCTurn = False
    dealerTurn = False
    doubleDownAvailable = False
    insuranceAvailable = False

class playerActionStates:
    # Player Actions
    hit = False
    stand = False
    split = False
    insurance = False
    betMade = False
    startNextRound = False
    potentialBet = 0
    playerWinnings = 0

class playGame():
    def __init__(self, screen, noOfDecks: int, difficulty: str, noOfNPCs:int, startingBux: int,  debugMode: bool):
        self.startingBux = startingBux
        self.noOfDecks = noOfDecks
        self.noOfNPCs = noOfNPCs
        self.difficulty = difficulty
        # Game setup variables
        self.screen = screen
        self.gameSetup = setupGame(startingBux, noOfNPCs)
        self.players = self.gameSetup.players
        self.playerSeats = self.getPlayerSeats()
        self.UI = handleGameUI(screen, self.playerSeats)
        # Handle deck
        self.deckInstance = deckHandling(noOfDecks) # Deck handling instance ready
        self.deckInstance.shuffle() # Shuffle the deck
        # Game States
        self.gameState = gameStates()
        self.playerAction = playerActionStates()
        # Gameplay Attributes
        self.currentPlayer = self.players[0]
        self.dealer = self.players[len(self.players)-1]
        self.playerIndex = 0
        self.bustPlayers = 0 # Integer to count how many players went bust
        self.minCardsPerPlayer = len(self.players) * 5 # Assume each player will require 5 cards per turn on average
        # Counting Cards
        self.runningCount = 0
        self.trueCount = 0
        self.seenCards = 0
        self.predictedNextCard = ""
        # --- DEBUGGING PRUPOSES --- #
        self.debugMode = debugMode
        self.presetCards = self.getPresetCards()
        self.roundNumber = 1
        # -------------------------- #

    # --- DEBUGGING PURPOSES --- #
    def getPresetCards(self):
        # Faces: "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" 
        return {
                "roundStagger": None,
                "dealer": [],
                "player": ["5","K", "6"]
                }
    # -------------------------- #
            
    def initialDeal(self):
        for i in range(2): # Deal 2 cards to players from left to right
            for player in self.players:
                if i == 1 and player.isDealer: # If the dealer is dealt their second card
                    player.dealCard(self, visible=False) # Deal the card face down
                else: # Deal the card to the player
                    player.dealCard(self)
        self.roundStarted = True # Start the round

    def isDoubleDownAvailable(self):
        # Makes double down available
        if self.currentPlayer.canDoubleDown() and self.currentPlayer.isPlayer:
            self.gameState.doubleDownAvailable = True
        else:
            self.gameState.doubleDownAvailable = False
            
    def isInsuranceAvailable(self):
        dealerHand = self.dealer.hands[0]
        if dealerHand.cards[0].face == "A":
            self.gameState.insuranceAvailable = True
        else:
            self.gameState.insuranceAvailable = False

    def hasActiveHands(self):
        for player in self.players: # Loop through players
            if player.isDealer:
                continue
            for hand in player.hands:
                if not hand.busted and not hand.naturalBlackjack:
                    return True
        return False
    
    def deckHasEnoughCards(self):
        # Returns true if the deck has enough cards to play
        if len(self.deckInstance.deck) > self.minCardsPerPlayer:
            return True
        else:
            return False

    def increaseCount(self, card):
        self.runningCount += card.cardWeight
        self.seenCards += 1
        decksRemaining = self.noOfDecks - round(self.seenCards // 56)
        self.trueCount = self.runningCount // decksRemaining
        # self.predictNextCard()

    def progressTurn(self):
        # If the current hand index is the last hand
        if self.currentPlayer.handIndex == len(self.currentPlayer.hands) - 1:
            # If the current index is less than the last index, increase it
            if self.playerIndex < len(self.players) - 1:
                self.playerIndex += 1
            self.currentPlayer = self.players[self.playerIndex]  # always update currentPlayer
        # Move to the next hand
        else:
            self.currentPlayer.handIndex += 1

    def endRound(self):
        # Game States
        self.gameState.bettingPhase = True
        self.gameState.roundStarted = False
        self.gameState.roundOver = False
        self.gameState.payedOut = False
        self.gameState.NPCTurn = False
        self.gameState.dealerTurn = False
        self.gameState.doubleDownAvailable = False
        # Player Actions
        self.playerAction.hit = False
        self.playerAction.stand = False
        self.playerAction.split = False
        self.playerAction.insurance = False
        self.playerAction.betMade = False
        self.playerAction.startNextRound = False
        self.playerAction.potentialBet = 0
        self.playerAction.playerWinnings = 0
        self.playerIndex = 0
        for player in self.players:
            player.newRound()
        # --- Debugging Purposes --- #
        self.roundNumber += 1
        #print(self.roundNumber)

    def getPlayerSeats(self):
        # Assigns players their seating positions
        seatingPositions = [(300, 250), (300, 550), (700, 650), (1100,550), (1100,250)] # TODO Find good seating positions, will be the position of the text of the player's name
        playerPos = 0 # Position of the player in the list
        seatingPosDict = {}
        # Get the position of the user in the players list
        for player in self.players:
            if player.isPlayer:
                playerPos = self.players.index(player)
        # Align the 2 lists so the middles match
        startingPos = 2 - playerPos # 2 is the middle of the seatingPositions list, player pos should be the middle of the players list
        for i in range(startingPos, len(self.players)-1 + startingPos):
            # self.players[i - startingPos] "i - startingPos" Is the index of the players in the player list
            # seatingPositions[i] is the aligned seating position
            seatingPosDict[self.players[i - startingPos]] = seatingPositions[i]
        seatingPosDict[self.players[len(self.players)-1]] = (700, 200) # Adds the dealer's seating position
        return seatingPosDict
    
    def predictNextCard(self):
        if self.seenCards > (56 * self.noOfDecks) * 0.5: # Half of the deck has been seen so predictions are strong
            if self.trueCount > 6:
                self.predictedNextCard = "strongHigh"
            elif self.trueCount > 4:
                self.predictedNextCard = "weakHigh"
            elif self.trueCount < -6:
                self.predictedNextCard = "strongLow"
            elif self.trueCount < -4:
                self.predictedNextCard = "weakLow"
            else:
                self.predictedNextCard = "medium"
        elif self.seenCards > (56 * self.noOfDecks) * 0.25: # Seen a quarter of the deck so predictions may be accurate
            if self.trueCount > 4:
                self.predictedNextCard = "weakHigh"
            elif self.trueCount < -4:
                self.predictedNextCard = "weakLow"
            else:
                self.predictedNextCard = "unknown"
        else: # Not seen enough the deck to accurately predict the next card
            self.predictedNextCard = "unknown"
            
    
    def handleUI(self):
        self.UI.updateImage(self.players)
    