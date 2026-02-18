from deckLogic import deckHandling
from players import player, NPC

deckInstance = None

NPCNAMES = []
NPCPERSONALITIES = []

class setupGame():
    def __init__(self, startingBux: int):
        self.startingBux = startingBux

    def createNPC(self):
        return NPC("steve", self.startingBux, 1.0, 1.0, 1.0, 1.0, 1.0)
    
    def generateprosperity(self):
        pass
    def generateConfidence(self):
        pass
    def generateJudgement(self):
        pass
    def generateExperience(self):
        pass

class playGame():
    def __init__(self, noOfDecks: int, difficulty: str, noOfNPCs:int, startingBux: int):
        global deckInstance
        self.user = player(startingBux) # Creating the player object
        self.NPCs = [] # Preparing to make the NPCs
        self.roundStarted = False
        deckInstance = deckHandling(noOfDecks) # Deck handling instance ready
        if noOfNPCs != 0: # Create NPCs
            for _ in range(noOfNPCs):
                self.NPCs.append(setupGame(startingBux).createNPC())
        self.players = self.NPCs[:] # A list for all the players, cloning the NPCs list
        self.players.insert((len(self.NPCs))//2, self.user) # Insert the User object into the middle of the list with a left bias
        
    def initialDeal(self):
        for _ in range(2): # Deal 2 cards to players from left to right
            for player in self.players:
                player.dealCard(deckInstance)
        self.roundStarted = True
        
    def updateImage(self):
        for i in self.players:
            pass