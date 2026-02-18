from pygameUtils.rand import shuffleList
import pygame

class cards():
    def __init__(self, face: str, suit: str, cardWeight: int):
        self.faceConversion = {"A":11, "K":10, "Q":10, "J":10}
        self.face = face
        self.value = int(face) if face.isnumeric() else self.faceConversion[face]
        self.suit = suit
        self.cardWeight = cardWeight
        self.visible = False
        self.discarded = False

    def setVisible(self):
        self.visible = True
        
    def discard(self):
        self.discarded = True
        
    def createCardImage(self):
        pass

class deckHandling():
    def __init__(self, noOfDecks: int):
        self.deck = self.generateDeck(noOfDecks)
        self.cardsInPlay = []
        self.discardPile = []

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
    
    def shuffle(self):
        self.deck = shuffleList(self.deck)
    
    def getCard(self):
        return self.deck.pop(0) # Returns top card