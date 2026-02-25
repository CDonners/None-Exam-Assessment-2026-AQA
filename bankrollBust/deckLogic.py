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
        self.cardRect = pygame.Rect(0, 0, 80, 120)
        self.FONT_VALUE = pygame.font.SysFont("", 36)
        self.FONT_SUIT = pygame.font.SysFont("", 22)
        
    def drawCard(self, surface, centre: tuple):
        self.cardRect.center = centre
        pygame.draw.rect(surface, (255, 255, 255), self.cardRect) # Black border of card
        pygame.draw.rect(surface, (0, 0, 0), self.cardRect, 2) # White centre
        # Get the correct font colour
        if self.suit in ["♥", "♦"]:
            colour = (200, 0, 0)
        else:
            colour = (0, 0, 0)
        # Top-left text
        text = self.FONT_SUIT.render(self.suit, True, colour)
        # Center suit symbol
        center_text = self.FONT_VALUE.render(self.face, True, colour)
        text_rect = center_text.get_rect(center=self.cardRect.center)
        # Drawing texts
        surface.blit(text, (self.cardRect.x + 5, self.cardRect.y + 5))
        surface.blit(center_text, text_rect)
        
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
        suits = ["♠", "♥", "♦", "♣"]
        values = [["A", -1],["2", 1],["3", 1],["4", 2],["5", 2],["6", 2],["7", 1],["8", 0],["9", 0],["10", -2],["J", -2],["Q", -2],["K", -2]] 
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