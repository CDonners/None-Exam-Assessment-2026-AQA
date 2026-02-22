from deckLogic import deckHandling
from players import player, NPC
from pygameUtils.rand import genRandInt

deckInstance = None

NPCNAMES = ["Paul","Noel","Aniyah","Dalton","Mariah","Zeke","Jolie","Kristian","Brynlee","Dilan","Charlotte","Cory","Camila","Sonny","Martha","Quincy","Elliot","Blaze","Paola","Cain","Anya","Raylan","Emily","Jax","Lucy"]
NPCPERSONALITIES = []

class setupGame():
    def __init__(self, startingBux: int):
        self.startingBux = startingBux
        self.pickedNames = []


    def createNPC(self):
        name = self.pickName()
        prosperity = self.generateProsperity()
        confidence = self.generateConfidence()
        judgement = self.generateJudgement()
        experience = self.generateExperience()
        return NPC(name, self.startingBux, "personality", prosperity, confidence, judgement, experience)
    
    def pickName(self):
        # Picks am unused name from the NPC Names list
        indexCorrect = False 
        while not indexCorrect: # Looping until a correct index is generated
            generatedIndex = genRandInt(8) # Generate an integer for the index
            if generatedIndex < len(NPCNAMES): # If the index is greater or equal to length of the names list, regenerate it.
                pickedName = NPCNAMES[generatedIndex] # Get the item at the index
                if pickedName not in self.pickedNames: # Check if the item has already been used
                    indexCorrect = True # Breaking the loop

        self.pickedNames.append(pickedName) # Add the 
        return pickedName

    def generateFloat(self, lowerBound: int, upperBound: int):
        integerGenerated = genRandInt(8) # Generate an integer
        while integerGenerated > 150 or integerGenerated < 50: # While it is between the bounds
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
    def __init__(self, noOfDecks: int, difficulty: str, noOfNPCs:int, startingBux: int):
        global deckInstance
        self.user = player(startingBux) # Creating the player object
        self.NPCs = [] # Preparing to make the NPCs
        self.roundStarted = False
        self.playerSeats = {}
        self.gameSetup = setupGame(startingBux)
        deckInstance = deckHandling(noOfDecks) # Deck handling instance ready
        if noOfNPCs != 0: # Create NPCs
            for _ in range(noOfNPCs):
                self.NPCs.append(self.gameSetup.createNPC())
        self.players = self.NPCs[:] # A list for all the players, cloning the NPCs list
        self.players.insert((len(self.NPCs))//2, self.user) # Insert the User object into the middle of the list with a left bias
        self.getPlayerSeats()
        
    def initialDeal(self):
        for _ in range(2): # Deal 2 cards to players from left to right
            for player in self.players:
                player.dealCard(deckInstance)
        self.roundStarted = True

    def getPlayerSeats(self):
        # Assigns players their seating positions
        seatingPositions = [(), (), (), (), (), (), ()]
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
        
        
    def updateImage(self):
        for i in self.players:
            pass

