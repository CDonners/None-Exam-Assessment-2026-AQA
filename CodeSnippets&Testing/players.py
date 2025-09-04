class nonePlayableCharacters():
    def __init__(self, name: str, personality: str, prosperity: int, judgement: int, confidence: int, experience: int):
        # Asthetic Attributes
        self.name = name
        self.personality = personality # Affects voice lines 
        # Gameplay Attributes
        self.prosperity = prosperity # Affects how much they bet in general (Similar to a multiplier)
        self.judgement = judgement # Affects how much they bet on a good/bad hand 
        self.confidence = confidence # Affects how likely they are to place a risky bet (Affected by the card count and their hand)
        self.experience = experience # Their card counting ability (Affects how well they can use the card count to their advantage)
        # Gameplay Variables
        self.hand = []