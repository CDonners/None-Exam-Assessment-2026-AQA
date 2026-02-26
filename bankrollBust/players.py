from typing import Any

class player():
    def __init__(self, bustBux: int):
        self.name = "Player"
        self.hand = []
        self.handValue = 0
        self.bustBux = bustBux
        self.isBusted = False
        self.isStood = False
        self.bet = 0
        
    def bust(self, game):
        game.bustPlayers += 1
        self.isBusted = True
    
    def stand(self, game):
        if self.name != "Dealer":
            print("Dealer not standing")
            game.stoodHands[self.handValue] = self # Adding the stood hand to the dictionary
            print(len(game.stoodHands))
        self.isStood = True

    def dealCard(self, deck: Any, visible = True):
        card = deck.getCard()
        if visible:
            card.setVisible()
        self.hand.append(card)
        
    def newRound(self):
        self.hand = []
        self.handValue = 0
        self.isBusted = False
        self.isStood = False
        self.bet = 0
    
class dealer(player):
    def __init__(self):
        super().__init__(-1)
        self.name = "Dealer"
        self.hand = []
        self.isBusted = False
        self.isStood = False

    def decideNextMove(self):
        pass # Do when I feel like it

class NPC(player):
    def __init__(self, name: str, bustBux: int, personality: str,  prosperity: float, confidence: float, judgement: float, experience: float):
        super().__init__(bustBux)
        self.name = name
        self.personality = personality
        self.prosperity = prosperity
        self.confidence= confidence
        self.judgement = judgement
        self.experience = experience 
        
    def decideNextMove(self):
        pass # Do when I feel like it

    def calculateBet(self):
        pass # min bet + (min-bet * prosperity) and current count something or other
