from os import urandom

class cards():
    def __init__(self, value: str, suit: str, cardWeight: int, score: int):
        self.value = value
        self.suit = suit
        self.cardScore = score
        self.cardWeight = cardWeight
        self.visible = False
        self.discarded = False

    def setVisible(self):
        self.visible = True
        
    def setDiscarded(self):
        self.discarded = True

class deckHandling():
    def __init__(self, noOfDecks: int):
        self.deck = self.generateDeck(noOfDecks)
        self.cardsInPlay = []
        self.discardPile = []
    
    def genRandInt(self, numberOfBits: int):
        # Ensure numberOfBits is greater than 0
        if numberOfBits < 0:
            raise ValueError("Error: Cannot have less than 0 bits")
        byteStringLen = (numberOfBits+8)//8 # Converts n into bytes rounding up
        byteString = urandom(byteStringLen) # Generates a random string of bytes from within the machine with specified length
        byteStringValue = int.from_bytes(byteString) # Converts byte string back to an integer
        return byteStringValue
    
    def shuffle(self):
        for pos in range(len(self.deck)-1,-1,-1):
            # Get the new position
            bitLength = pos.bit_length() # Gets how many bits is in the index
            newPos = self.genRandInt(bitLength) # Create Position
            while newPos >= len(self.deck)-1: # If the position is out of range gen again
                newPos = self.genRandInt(bitLength) # Creates a new position
            self.deck[pos], self.deck[newPos] = self.deck[newPos], self.deck[pos] # Flips position values

    def generateDeck(self, noOfDecks: int):
        # Card Values and Suits
        suits = ["h","d","s","c"]
        values = [["A", -1, 11],["2", 1, 2],["3", 1, 3],["4", 2, 4],["5", 2, 5],["6", 2, 6],["7", 1, 7],["8", 0, 8],["9", 0, 9],["10", -2, 10],["J", -2, 10],["Q", -3, 10],["K", -2, 10]] 
        deck = [] # Empty list to append generated cards to
        # Create every card in the standard 52 playing card deck
        for suit in suits:
            for value in values:
                # No magic numbers
                cardValue = value[0]
                cardScore = value[1]
                cardWeight = value[2]
                deck.append(cards(cardValue, suit, cardScore, cardWeight)) # Create object for the individual card
        deck = deck*noOfDecks # Combines multiple decks together
        return deck # Returns finalised deck
    
class playCards(deckHandling):
    def __init__(self, noOfDecks):
        super().__init__(noOfDecks)
        self.noOfPlayers = 5 # Temporary Variable for demostration purposes
            
    def dealCard(self):
        card = self.deck.pop(0)
        card.setVisible()
        self.cardsInPlay.insert(0, card)

class countingCards():
    def __init__(self):
        self.runningCount = 0
        self.trueCount = 0
    
    def handQuality(self, hand: list):
        handValue = 0
        for card in hand:
            handValue += card.score
        # Target is 21, 20, 19
        if handValue in [21, 20, 19]:
            return "Stand"
        # Find cards needed:
        valuesNeeded = [i-handValue for i in range(21, 18, -1)]
        # Higher the count, the more high cards there are, JQK are high, 789 are mid, 456 are lowish, 23 are low A, is low and high

p = playCards(4)
p.shuffle()
for i in range(int(input("How many rounds to simulate: "))):
    for i in range(18):
        p.dealCard()
score = 0
for i in p.cardsInPlay:
    score += i.cardWeight
playedCards1 = [i.value for i in p.cardsInPlay]
playedCards = {i:playedCards1.count(i) for i in list(set(playedCards1))}
print(score,"\n",playedCards)
p.dealCard()
input()
print(p.cardsInPlay[0].value)
