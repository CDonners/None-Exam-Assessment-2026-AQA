from gameLogic import deckInstance

class player():
    def __init__(self, bustBux: int):
        self.name = "Player"
        self.hand = []
        self.bustBux = bustBux
        self.isBusted = False
        
    def bust(self):
        self.isBusted = True

    def dealCard(self):
        card = deckInstance.getCard()
        self.hand.append(card)
        
    def newRound(self):
        self.isBusted = False
        self.hand = []

class NPC(player):
    def __init__(self, name: str, 
                 bustBux: int,
                 personality: str, 
                 prosperity: float,
                 confidence: float, 
                 judgement: float,
                 experience: float):
        super().__init__(bustBux)
        self.name = name
        self.personality = personality
        self.prosperity = prosperity
        self.confidence= confidence
        self.judgement = judgement
        self.experience = experience 
        
    def decideNextMove(self):
        pass # Do when I feel like it
