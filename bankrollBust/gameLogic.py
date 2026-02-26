from deckLogic import deckHandling
from players import player, NPC, dealer
import pygame
from pygameUtils.rand import genRandInt

NPCNAMES = ["Paul","Noel","Aniyah","Dalton","Mariah","Zeke","Jolie","Kristian","Brynlee","Dilan","Charlotte","Cory","Camila","Sonny","Martha","Quincy","Elliot","Blaze","Paola","Cain","Anya","Raylan","Emily","Jax","Lucy"]
NPCPERSONALITIES = []

class setupGame():
    def __init__(self, startingBux: int):
        self.startingBux = startingBux

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
        generatedConfidence = self.generateFloat(75, 125)
        return generatedConfidence

    def generateExperience(self):
        # Must generate a float between 0.5-1.5
        generatedConfidence = self.generateFloat(50, 150)
        return generatedConfidence

class playGame():
    def __init__(self, noOfDecks: int, difficulty: str, noOfNPCs:int, startingBux: int, screen):
        self.startingBux = startingBux
        self.screen = screen
        self.user = player(startingBux) # Creating the player object
        self.NPCs = [] # Preparing to make the NPCs
        self.roundStarted = False
        self.playerSeats = {}
        self.gameSetup = setupGame(startingBux)
        self.deckInstance = deckHandling(noOfDecks) # Deck handling instance ready
        self.deckInstance.shuffle()
        if noOfNPCs != 0: # Create NPCs
            for _ in range(noOfNPCs):
                self.NPCs.append(self.gameSetup.createNPC())
        self.players = self.NPCs[:] # A list for all the players, cloning the NPCs list
        self.userIndex = (len(self.NPCs))//2
        self.players.insert(self.userIndex, self.user) # Insert the User object into the middle of the list with a left bias
        self.getPlayerSeats()
        self.players.append(dealer())
        self.playerSeats[self.players[len(self.players)-1]] = (700, 200)
        self.stoodHands = {}
        self.bustPlayers = 0
        self.playerTexts = []
        self.betTexts = []
        self.createPlayerTexts()
        
    def initialDeal(self):
        for i in range(2): # Deal 2 cards to players from left to right
            for player in self.players:
                if i == 1 and player.name == "Dealer":
                    player.dealCard(self.deckInstance, visible=False)
                else:
                    player.dealCard(self.deckInstance)
        self.roundStarted = True        

    def getPlayerSeats(self):
        # Assigns players their seating positions
        seatingPositions = [(), (), (), (700, 650), (), (), ()] # TODO Find good seating positions, will be the position of the text of the player's name
        playerPos = 0 # Position of the player in the list
        # Get the position of the user in the players list
        for i in self.players:
            if i.name == "Player":
                playerPos = self.players.index(i)
        # Align the 2 lists so the middles match
        startingPos = 3 - playerPos # 3 is the middle of the seatingPositions list, player pos should be the middle of the players list
        for i in range(startingPos, len(self.players) + startingPos):
            # self.players[i - startingPos] "i - startingPos" Is the index of the players in the player list
            # seatingPositions[i] is the aligned seating position
            self.playerSeats[self.players[i - startingPos]] = seatingPositions[i]

    def createPlayerTexts(self):
        playerFont = pygame.font.SysFont("", 32) # Sets the font to pygame default with size 22
        for playerObj in self.players:
            # Creating the text for the player
            playerTextSurface = playerFont.render(f"{playerObj.name}", True, (255, 255, 255)) # Creates text surface with colour black
            playerTextRect = playerTextSurface.get_rect(center=self.playerSeats[playerObj])
            self.playerTexts.append([playerTextSurface, playerTextRect])
        
    def drawPlayerTexts(self):
        for text in self.playerTexts:
            playerSurface, playerRect = text[0], text[1]
            self.screen.blit(playerSurface, playerRect)

    def createPlayerBetTexts(self):
        betFont = pygame.font.SysFont("", 28) # Sets the font to pygame default with size 22
        for playerObj in self.players:
            if playerObj.name != "Dealer":
                betCentre = (self.playerSeats[playerObj][0], self.playerSeats[playerObj][1]+25)
                betTextSurface = betFont.render(f"Bet: {playerObj.bet}", True, (255, 255, 255)) # Creates text surface with colour black
                betTextRect = betTextSurface.get_rect(center=betCentre)
                self.betTexts.append([betTextSurface, betTextRect])

    def updateBet(self, betIndex):
        betFont = pygame.font.SysFont("", 28) # Sets the font to pygame default with size 22
        playerObj = self.players[betIndex]
        betTextSurface = betFont.render(f"Bet: {playerObj.bet}", True, (255, 255, 255)) # Creates text surface with colour black
        self.betTexts[betIndex][0] = betTextSurface

    def drawPlayerBets(self):
        for text in self.betTexts:
            betSurface, betRect = text[0], text[1]
            self.screen.blit(betSurface, betRect)
            
    def drawHands(self, playerObj):
        hand = playerObj.hand
        cardWidth = 80
        cardHeight = 120
        spacing = 30
        totalWidth = len(hand)*80 + (len(hand)-1) * 30
        startX = self.playerSeats[playerObj][0] - totalWidth // 2
        # The right card is self.playerSeats[player][0] + totalWidth // 2
        # Cards inbetween is last card position plus 30
        for i, card in enumerate(hand):
            x = startX + i * (cardWidth + spacing)  # no overlap
            y = self.playerSeats[playerObj][1] - 30 - cardHeight//2
            card.drawCard(self.screen, (x, y))

    def drawBalance(self):
        balanceFont = pygame.font.SysFont("", 32) # Sets the font to pygame default with size 22
        playerBalance = self.players[self.userIndex].bustBux
        balanceCentre = (25,25)
        balanceTextSurface = balanceFont.render(f"Balance:{playerBalance}", True, (0, 0, 0)) # Creates text surface with colour black
        balanceTextRect = balanceTextSurface.get_rect(topleft=balanceCentre)
        self.screen.blit(balanceTextSurface, balanceTextRect)
        
    def getHandValue(self, playerObj):
        # Get the value of the player's hand
        totalSum = 0 # Creating variable for value
        cardValues = [card.value for card in playerObj.hand] # List of all values in the player's hand
        for value in cardValues: # Loop through the card values
            totalSum += value # Add them all together
        playerObj.handValue = totalSum # Making the handValue of the player object be the gathered value    
        
    def checkBusted(self, playerToCheck):
        self.getHandValue(playerToCheck)
        cardValues = [card.value for card in playerToCheck.hand] # List of all values in the player's hand
        # Check if the player has busted
        if playerToCheck.handValue > 21: # Player might be bust
            if 11 in cardValues: # See if the player has the ace
                aceIndex = cardValues.index(11) # Get the location of the ace
                playerToCheck.hand[aceIndex].value = 1 # Set the ace's value to 1
                playerToCheck.handValue -= 10 # Correct the player's hand value
                return False # Player hasn't bust
            else: # Player has no ace and has bust
                return True 
        else:
            return False # Player hasn't bust
        
    def checkBlackjack(self, playerObj):
        self.getHandValue(playerObj)
        if playerObj.handValue == 21:
            return True
        
    def updateImage(self):
        for player in self.players:
            self.drawHands(player)
        self.drawPlayerTexts()
        self.drawBalance()
        self.drawPlayerBets()
        
