from os import urandom

class cards():
    def __init__(self, value: str, suit: str, cardWeight: int):
        self.value = value
        self.suit = suit
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
        values = [["A", -1],["2", 1],["3", 1],["4", 2],["5", 2],["6", 2],["7", 1],["8", 0],["9", 0],["10", -2],["J", -2],["Q", -3],["K", -2]] 
        deck = [] # Empty list to append generated cards to
        # Create every card in the standard 52 playing card deck
        for suit in suits:
            for value in values:
                deck.append(cards(value[0], suit, value[1])) # Create object for the individual card
        deck = deck*noOfDecks # Combines multiple decks together
        return deck # Returns finalised deck
    
class playCards(deckHandling):
    def __init__(self, noOfDecks):
        super().__init__(noOfDecks)
        self.noOfPlayers = 7 # Temporary Variable for demostration purposes
        
    def initialDeal(self):
        # noOfPlayers+1 to account for dealer, x2 as 2 cards per person, +1 as for loops aren't inclusive
        cardsToDeal = (self.noOfPlayers + 1) * 2 + 1
        for i in range(cardsToDeal): # Deal normal visible cards
            if i != cardsToDeal -1:
                self.dealCard
            else: # Dealer's last card will be the last card dealt and is not visible
                card = self.deck.pop(0)
                self.cardsInPlay.insert(0, card)
                
    def dealCard(self):
        card = self.deck.pop(0)
        card.setVisible()
        self.cardsInPlay.insert(0, card)
    
    def burnCard(self):
        card = self.deck.pop(0) # Remove card from deck
        self.discardPile.insert(0, card) # Add to the discard pile
        
    def clearTable(self):
        for card in self.cardsInPlay:
            self.discardPile.insert(0, card)
        self.cardsInPlay = []
    
class cardCountingAlgorithm():
    pass
    
p = playCards(4)
p.shuffle()



    # def generateDeck(self, noOfDecks: int):
    #     suits = ["h","d","c","s"] 
    #     values = ["1","2","3","4","5","6","7","8","9","10","11","12","13"] # Numerical representation of card values
    #     deck = []
    #     # Create every card in the standard 52 playing card deck
    #     for suit in suits:
    #         for value in values:
    #             deck.append([value, suit])
    #     deck = deck*noOfDecks # Combines multiple decks together
    #     return deck # Returns finalised deck