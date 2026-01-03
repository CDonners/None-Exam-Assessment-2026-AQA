from deckLogic import deckHandling
from players import player, NPC

deckInstance = None

NPCNAMES = []
NPCPERSONALITIES = []

class playGame():
    def __init__(self, noOfDecks: int, difficulty: str, noOfNPCs:int, startingBux: int):
        global deckInstance
        self.user = None
        self.NPCs = []
        deckInstance = deckHandling(noOfDecks) # Deck handling instance ready
        if noOfNPCs != 0: # Create NPCs
            for _ in range(noOfNPCs):
                pass