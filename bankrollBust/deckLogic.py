from pygameUtils.rand import shuffleList
import pygame

class cards():
    def __init__(self, face: str, suit: str, cardWeight: int):
        self.faceConversion = {"A":11, "K":10, "Q":10, "J":10}
        # Card 
        self.face = face
        self.value = int(face) if face.isnumeric() else self.faceConversion[face]
        self.suit = suit
        self.cardWeight = cardWeight
        # Card Gameplay Attributes
        self.visible = False
        # Card Rects
        self.cardRect = pygame.Rect(0, 0, 55, 75)
        # Text Variables
        self.FONT_VALUE = pygame.font.SysFont("", 36)
        self.FONT_SUIT = pygame.font.SysFont("segoeuiemoji", 18)
        
    def drawCard(self, screen, centre: tuple, colourIndex = 0, active=True):
        handColours = {0:"black", 1: (255, 87, 51), 2: (51, 255, 87), 
                       3: (51, 87, 255), 4: (255, 51, 168), 5: (51, 255, 243), 
                       6: (243, 255, 51), 7: (168, 51, 255), 8: (255, 140, 51), 
                       9: (51, 255, 140)} # Colours for hands to distinguish them
        self.cardRect.center = centre
        # Get the correct font colour
        if self.suit in ["♥️", "♦️"]:
            colour = (200, 0, 0)
        else:
            colour = (0, 0, 0)
        # Top-left text
        text = self.FONT_SUIT.render(self.suit, True, colour)
        # Center suit symbol
        center_text = self.FONT_VALUE.render(self.face, True, colour)
        text_rect = center_text.get_rect(center=self.cardRect.center)
        # Colour of the card centre
        if active:
            centreColour = "white"
        else:
            centreColour = (180, 180, 180)
        # Drawing texts if card is visible
        if self.visible:
            pygame.draw.rect(screen, centreColour, self.cardRect) # White card Centre
            screen.blit(text, (self.cardRect.x + 5, self.cardRect.y + 5))
            screen.blit(center_text, text_rect)
        else:
            pygame.draw.rect(screen, (255,69,67), self.cardRect) # Red card Centre
        pygame.draw.rect(screen, handColours[colourIndex], self.cardRect, 4) # Border
        
    def setVisible(self):
        self.visible = True

class deckHandling():
    def __init__(self, noOfDecks: int):
        self.noOfDecks = noOfDecks
        self.deck = self.generateDeck()

    def generateDeck(self):
        # Card Values and Suits
        suits = ["♠️", "♥️", "♦️", "♣️"]
        values = [["A", -1],["2", 1],["3", 1],["4", 2],["5", 2],
                  ["6", 2],["7", 1],["8", 0],["9", 0],["10", -2],
                  ["J", -2],["Q", -2],["K", -2]] 
        deck = [] # Empty list to append generated cards to
        # Create every card in the standard 52 playing card deck
        for _ in range(self.noOfDecks):
            for suit in suits:
                for value in values:
                    deck.append(cards(value[0], suit, value[1])) # Create object for the individual card
        return deck # Returns finalised deck
    
    def shuffle(self):
        self.deck = shuffleList(self.deck)
    
    def getCard(self):
        return self.deck.pop(0) # Returns top card