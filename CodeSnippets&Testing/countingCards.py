class countingCards():
    def __init__(self):
        # Constants
        self.CARDDEFS  = {"veryHigh":["K","J","Q","10"], "high":["7","8", "9"], "low":["4","5","6"], "veryLow":["A","2","3"]}
        # Variables
        self.runningCount = 0
        self.trueCount = 0
        self.nextCard = self.findNextCard()
    
    def findNextCard(self):
        nextCard = "" # Very High, High, Low, Very Low, Unknown
        if self.runningCount < 0:
            nextCard = "low"
            if self.runningCount < -10:
                nextCard = "veryLow"
        elif self.runningCount > 0:
            nextCard = "high"
            if self.runningCount > 10:
                nextCard = "veryHigh"
        else:
            nextCard = "Unknown"
        return nextCard
    
    def determineCardsNeeded(self, valuesNeeded):
        cardDefsNeeded = [] # Can be atmost 2 values
        for category in self.CARDDEFS:
            cardDef = self.CARDDEFS[category]
            if any(i in cardDef for i in valuesNeeded):
                cardDefsNeeded.append(cardDef)
    
    def handQuality(self, hand: list):
        handValue = 0
        for card in hand:
            handValue += card.score
        # Target is 21, 20, 19
        if handValue in [21, 20, 19]:
            return "Stand"
        # Find cards needed:
        valuesNeeded = [i-handValue for i in range(21, 18, -1)]
        # Get the base value for the hand
        if any(i > 10 for i in valuesNeeded): # Cannot bust at all
            handQual = 1
        