from typing import Any

class hand:
    def __init__(self):
        self.hand = []
        self.handValue = 0
        self.stood = False
        self.busted = False
        self.blackjack = False
        self.push = False
        self.bet = 0

class player():
    def __init__(self, bustBux: int):
        self.name = "Player"
        self.hands = [{"hand": [], "handValue": 0, "stood": False, "busted": False, "blackjack": False, "bet": 0}] 
        self.handIndex = 0
        self.totalBet = 0
        self.bustBux = bustBux
        self.insurance = 0
        
    def bust(self, game):
        currentHand = self.hands[self.handIndex]
        game.bustPlayers += 1
        currentHand["busted"] = True
        self.handIndex += 1
    
    def stand(self, game):
        currentHand = self.hands[self.handIndex]
        if self.name != "Dealer":
            uniqueHandID = f"{currentHand["handValue"]},{self.name},{self.handIndex}"
            game.stoodHands[uniqueHandID] = self # Adding the stood hand to the dictionary
        self.hands[self.handIndex]["stood"] = True
        self.handIndex += 1

    def dealCard(self, deck: Any, visible = True):
        currentHand = self.hands[self.handIndex] 
        card = deck.getCard()
        if visible:
            card.setVisible()
        currentHand["hand"].append(card) # TODO Make compatible with new hand system
        
    def newRound(self):
        self.hands = [hand()]
        self.handIndex = 0
        self.totalBet = 0
        self.insurance = 0
    
class dealer(player):
    def __init__(self):
        super().__init__(-1)
        self.name = "Dealer"

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
