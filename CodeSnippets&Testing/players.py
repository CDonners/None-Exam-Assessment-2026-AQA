from .deckHandlingTesting import playCards

class player(playCards):
    def __init__(self, name: str, startingBux: int):
        super().__init__(noOfDecks=4)
        # Asthetic Attributes
        self.name = name
        # Gameplay Variables
        self.hand = []
        self.bustbux = startingBux
        self.isBusted = False

class nonePlayableCharacters(player):
    def __init__(self, name: str, personality: str, prosperity: int, judgement: int, confidence: int, experience: int, startingBux: int):
        super().__init__(name, startingBux)
        # Asthetic Attributes
        self.personality = personality # Affects voice lines 
        # Gameplay Attributes
        self.prosperity = prosperity # Affects how much they bet in general (Similar to a multiplier)
        self.judgement = judgement # Affects how much they bet on a good/bad hand 
        self.confidence = confidence # Affects how likely they are to place a risky bet (Affected by the card count and their hand)
        self.experience = experience # Their card counting ability (Affects how well they can use the card count to their advantage)
        
    