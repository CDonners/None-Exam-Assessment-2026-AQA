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
    def __init__(self, name: str, personality: str, prosperity: float, judgement: float, confidence: float, experience: float, startingBux: int):
        super().__init__(name, startingBux)
        # Asthetic Attributes
        self.personality = personality # Affects voice lines 
        # Gameplay Attributes
        self.prosperity = prosperity # Affects how much they bet in general (Similar to a multiplier)
        self.confidence = confidence # Affects how likely they are to place a risky bet (Affected by the card count and their hand)
        self.judgement = judgement # Affects how well they determine whether a hand is good/bad 
        self.experience = experience # Their card counting ability (Affects how well they can use the card count to their advantage)
        
p = player("steve", 1000)
p.dealCard()
print(p.hand)