from deckLogic import deckHandling
from players import player, NPC, dealer
import pygame
from pygameUtils.rand import genRandInt

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
        judgement = self.generateJudgement()
        experience = self.generateExperience()
        return NPC(name, self.startingBux, "personality", prosperity, confidence, judgement, experience)
    
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

    def generateFloat(self, lowerBound: int, upperBound: int):
        integerGenerated = genRandInt(8) # Generate an integer
        while integerGenerated > upperBound or integerGenerated < lowerBound: # While it is between the bounds
            integerGenerated = genRandInt(8) # Regenerate integer
        generatedFloat = integerGenerated/100
        return generatedFloat

    def generateProsperity(self):
        # Must generate a float between 0.5-1.5
        generatedProsperity = self.generateFloat(50, 150)
        return generatedProsperity
    
    def generateConfidence(self):
        # Must generate a float between 0.75-1.25
        generatedConfidence = self.generateFloat(75, 125)
        return generatedConfidence

    def generateJudgement(self):
        # Must generate a float between 0.75-1.25
        generatedJudgement = self.generateFloat(75, 125)
        return generatedJudgement

    def generateExperience(self):
        # Must generate a float between 0.5-1.5
        generatedExperience = self.generateFloat(50, 150)
        return generatedExperience

class handleGameUI:
    def __init__(self, screen, playerSeats):
        self.screen = screen
        self.playerSeats = playerSeats
        # Fonts
        self.mainFont = pygame.font.SysFont("", 32)
        self.betFont = pygame.font.SysFont("", 28)
        self.playerFont = pygame.font.SysFont("", 32) # Sets the font to pygame default with size 22
        
    def drawPlayerTexts(self, players):
        for playerObj in players:
            # Creating the text for the player
            playerTextSurface = self.playerFont.render(f"{playerObj.name}", True, (255, 255, 255)) # Creates text surface with colour black
            playerTextRect = playerTextSurface.get_rect(center=self.playerSeats[playerObj])
            self.screen.blit(playerTextSurface, playerTextRect)

    # !Might not need anymore need to test
    # def updateBet(self, betIndex):
    #     playerObj = self.players[betIndex]
    #     betTextSurface = self.betFont.render(f"Bet: {playerObj.totalBet}", True, (255, 255, 255)) # Creates text surface with colour black
    #     self.betTexts[betIndex][0] = betTextSurface

    def drawPlayerBets(self, players):
        for playerObj in players:
            if playerObj.name != "Dealer":
                betCentre = (self.playerSeats[playerObj][0], self.playerSeats[playerObj][1]+25)
                betTextSurface = self.betFont.render(f"Bet: {playerObj.totalBet}", True, (255, 255, 255)) # Creates text surface with colour black
                betTextRect = betTextSurface.get_rect(center=betCentre)
                self.screen.blit(betTextSurface, betTextRect)
            
    def drawHand(self, playerObj):
        hands = playerObj.hands
        if len(hands) != 0:
            # Card dimensions
            cardWidth = 60
            cardHeight = 80
            spacing = 15
            handSpacing = 30  
            # Calculate total width
            totalWidth = 0
            for i, hand in enumerate(hands):
                cards = hand.cards
                if len(cards) > 0:
                    totalWidth += len(cards) * cardWidth # Combined width of cards
                    totalWidth += (len(cards) - 1) * spacing # Include spacing of cards
                # Add spacing between hands instead of the card spacing
                if i < len(hands) - 1:
                    totalWidth += handSpacing
            # Centering start X
            centerX = self.playerSeats[playerObj][0]
            startX = centerX - totalWidth // 2
            # Start drawing hands at the specified positions
            currentX = startX
            for i, hand in enumerate(reversed(hands)):
                cards = hand.cards
                for j, card in enumerate(cards):
                    x = currentX + j * (cardWidth + spacing)
                    y = self.playerSeats[playerObj][1] - spacing - cardHeight // 2
                    card.drawCard(self.screen, (x, y), handIndex=i)
                # Move forward by this hand's width
                if len(cards) > 0:
                    currentX += len(cards) * cardWidth
                    currentX += (len(cards) - 1) * spacing
                # Add gap between hands
                if i < len(hands) - 1:
                    currentX += handSpacing

    def drawBalance(self, players, userIndex):
        playerBalance = players[userIndex].bustBux
        balanceCentre = (25,25)
        balanceTextSurface = self.mainFont.render(f"Balance:{playerBalance}", True, (0, 0, 0)) # Creates text surface with colour black
        balanceTextRect = balanceTextSurface.get_rect(topleft=balanceCentre)
        self.screen.blit(balanceTextSurface, balanceTextRect)   
        
    def drawStatusText(self, winnings):
        if winnings == 0: # Player made nothing
            textSurface = self.mainFont.render(f"Bets returned", True, (0, 0, 0)) # Creates text surface with colour black
        elif winnings > 0: # Player won BustBux
            textSurface = self.mainFont.render(f"Won: {winnings}", True, (0, 0, 0)) # Creates text surface with colour black
        elif winnings < 0: # Player lose BustBux
            textSurface = self.mainFont.render(f"Lost: {winnings*-1}", True, (0, 0, 0)) # Creates text surface with colour black
        
        textRect = textSurface.get_rect(center=(700,350))
        self.screen.blit(textSurface, textRect)
        
    def updateImage(self, players, userIndex):
        for player in players:
            self.drawHand(player)
        self.drawPlayerTexts(players)
        self.drawBalance(players, userIndex)
        self.drawPlayerBets(players)

class playGame():
    def __init__(self, noOfDecks: int, difficulty: str, noOfNPCs:int, startingBux: int, screen):
        self.startingBux = startingBux
        # Game setup variables
        self.screen = screen
        self.gameSetup = setupGame(startingBux, noOfNPCs)
        self.players = self.gameSetup.players
        self.playerSeats = self.getPlayerSeats()
        self.UI = handleGameUI(screen, self.playerSeats)
        # Handle deck
        self.deckInstance = deckHandling(noOfDecks) # Deck handling instance ready
        self.deckInstance.shuffle() # Shuffle the deck
        # Gameplay Attributes
        self.playerIndex = 0
        self.roundStarted = False
        self.roundOver = False
        self.stoodHands = {} # Dictionary of stood hands as uniqueID:PlayerObject
        self.bustPlayers = 0 # Integer to count how many players went bust
        
    def initialDeal(self):
        for i in range(2): # Deal 2 cards to players from left to right
            for player in self.players:
                if i == 1 and player.name == "Dealer": # If the dealer is dealt their second card
                    player.dealCard(self.deckInstance, visible=False) # Deal the card face down
                else: # Deal the card to the player
                    player.dealCard(self.deckInstance)
        self.roundStarted = True # Start the round


    def getPlayerSeats(self):
        # Assigns players their seating positions
        seatingPositions = [(), (), (), (700, 650), (), (), ()] # TODO Find good seating positions, will be the position of the text of the player's name
        playerPos = 0 # Position of the player in the list
        seatingPosDict = {}
        # Get the position of the user in the players list
        for i in self.players:
            if i.name == "Player":
                playerPos = self.players.index(i)
        # Align the 2 lists so the middles match
        startingPos = 3 - playerPos # 3 is the middle of the seatingPositions list, player pos should be the middle of the players list
        for i in range(startingPos, len(self.players) + startingPos):
            # self.players[i - startingPos] "i - startingPos" Is the index of the players in the player list
            # seatingPositions[i] is the aligned seating position
            seatingPosDict[self.players[i - startingPos]] = seatingPositions[i]
        seatingPosDict[self.players[len(self.players)-1]] = (700, 200) # Adds the dealer's seating position
        return seatingPosDict
    
    def handleUI(self):
        self.UI.updateImage(self.players,self.playerIndex)
    