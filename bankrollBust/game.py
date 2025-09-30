from main import deckInstance
from players import player, NPC

NPCNAMES = []
NPCPERSONALITIES = []

class playGame():
    def __init__(self, noOfNPCs: int, startingBux: int):
        self.user = None
        self.NPCs = []
        if noOfNPCs != 0: # Create NPCs
            for _ in range(noOfNPCs):
                pass
            
    def createPlayerObject(self, name: str, 
                 bustBux: int, 
                 personality: str, 
                 prosperity: float,
                 confidence: float, 
                 judgement: float,
                 experience: float):
        if personality is None: # Player Object is not an NPC so treat as such
            self.user = player(name, bustBux)
        else: # Create an NPC
            playerObject = NPC(name, bustBux, personality, prosperity, confidence, judgement, experience)
            return playerObject