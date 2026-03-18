from typing import Any

class hand:
    def __init__(self, card = None):
        self.cards = []
        self.handValue = 0
        self.stood = False
        self.busted = False
        self.blackjack = False
        self.push = False
        self.bet = 0

    def addCard(self, card):
        self.cards.append(card)

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
        cardToSplit = currentHand.cards.pop(1)
        newHand = hand()
        newHand.addCard(cardToSplit)
        self.hands.insert(self.handIndex+1, newHand)

    def checkBusted(self):
        cardValues = self.getHandValue() # Get list of the card values
        # Check if the player has busted
        currentHand = self.hands[self.handIndex]
        if currentHand.handValue > 21: # Player might be bust
            if 11 in cardValues: # See if the player has the ace
                aceIndex = cardValues.index(11) # Get the location of the first ace
                currentHand.cards[aceIndex].value = 1 # Set the ace's value to 1
                currentHand.handValue -= 10 # Correct the player's hand value
                return False # Player hasn't bust
            else: # Player has no ace and has bust
                return True 
        else:
            return False # Player hasn't bust
        
    def checkBlackjack(self):
        self.getHandValue() # Ensure hand value up to date
        currentHand = self.hands[self.handIndex]
        if currentHand.handValue == 21:
            return True
        else:
            return False

    def canSplit(self):
        currentHand = self.hands[self.handIndex].cards
        if len(currentHand) == 2:
             if currentHand[0].face == currentHand[1].face:
                 return True
        return False
    
    def getHandValue(self):
        # Get the value of the player's hand
        currentHand = self.hands[self.handIndex]
        totalSum = 0 # Creating variable for value
        cardValues = [card.value for card in currentHand.cards] # List of all values in the player's hand
        for value in cardValues: # Loop through the card values
            totalSum += value # Add them all together
        currentHand.handValue = totalSum # Making the handValue of the player object be the gathered value
        return cardValues # Useful for finding certain cards
        
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
