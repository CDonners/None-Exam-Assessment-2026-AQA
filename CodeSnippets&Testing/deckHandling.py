from os import urandom
    
class deckHandling():
    def __init__(self, noOfDecks: int):
        self.deck = self.generateDeck(noOfDecks) 
    
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
        suits = ["h","d","c","s"] 
        values = ["1","2","3","4","5","6","7","8","9","10","11","12","13"] # Numerical representation of card values
        deck = []
        # Create every card in the standard 52 playing card deck
        for suit in suits:
            for value in values:
                deck.append([value, suit])
        deck = deck*noOfDecks # Combines multiple decks together
        return deck # Returns finalised deck
