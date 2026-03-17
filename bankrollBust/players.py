from typing import Any

class hand:
    def __init__(self, card = None):
        self.hand = []
        self.handValue = 0
        self.stood = False
        self.busted = False
        self.blackjack = False
        self.push = False
        self.bet = 0

    def addCard(self, card):
        self.hand.append(card)

class player():
    def __init__(self, bustBux: int):
        self.name = "Player"
        self.hands = [hand()] 
        self.handIndex = 0
        self.totalBet = 0
        self.bustBux = bustBux
        self.insurance = 0
        
    def bust(self, game):
        if len(self.hands) > self.handIndex:
            currentHand = self.hands[self.handIndex]
            game.bustPlayers += 1
            currentHand.busted = True
            self.handIndex += 1
    
    def stand(self, game):
        if len(self.hands) > self.handIndex:
            currentHand = self.hands[self.handIndex]
            if self.name != "Dealer":
                uniqueHandID = f"{currentHand.handValue},{self.name},{self.handIndex}"
                game.stoodHands[uniqueHandID] = self # Adding the stood hand to the dictionary
            currentHand.stood = True
            self.handIndex += 1

    def dealCard(self, deck: Any, visible = True):
        if len(self.hands) > self.handIndex:
            currentHand = self.hands[self.handIndex] 
            card = deck.getCard()
            if visible:
                card.setVisible()
            currentHand.addCard(card)

    def splitHand(self):
        currentHand = self.hands[self.handIndex]
        cardToSplit = currentHand.hand.pop(1)
        newHand = hand()
        newHand.addCard(cardToSplit)
        self.hands.insert(self.handIndex+1, newHand)
        
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
