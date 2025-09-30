from main import deckInstance
from players import player, NPC

NPCNAMES = []
NPCPERSONALITIES = []

class playGame():
    def __init__(self, noOfNPCs: int, startingBux: int):
        self.NPCs = []
        if noOfNPCs != 0: # Create NPCs
            for _ in range(noOfNPCs):
                pass
    def createPlayerObject(self, startingBux: int, personality = None, pr = None):
        if personality is None: # Player Object is not an NPC so treat as such
            pass
        else:
            pass