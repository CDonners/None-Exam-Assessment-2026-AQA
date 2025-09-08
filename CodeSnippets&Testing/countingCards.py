class countingCards():
    def __init__(self):
        # Constants
        self.CARDGROUPS  = {"veryHigh":[["K","J","Q","10"],4], "high":[["7","8", "9"],3], "low":[["4","5","6"],2], "veryLow":[["A","2","3"],1]}
        ## Formatted as [cardGroup: [List of cards], numerical value assigned to group]
        # Variables
        self.runningCount = 0
        self.trueCount = 0
        self.nextCards = self.findnextCards()
    
    def findnextCards(self):
        nextCards = "" # Very High, High, Low, Very Low, Unknown
        if self.runningCount <= 0:
            nextCards = "low"
            if self.runningCount < -10:
                nextCards = "veryLow"
        elif self.runningCount > 0:
            nextCards = "high"
            if self.runningCount > 10:
                nextCards = "veryHigh"
        return nextCards
    
    def determineCardsNeeded(self, valuesNeeded):
        cardGroupsNeeded = [] # Can be atmost 2 values
        for category in self.CARDGROUPS:
            cardGroup = self.CARDGROUPS[category][0]
            if any(i in cardGroup for i in valuesNeeded):
                cardsInGroup = 0
                for card in valuesNeeded:
                    if card in cardGroup:
                        cardsInGroup += 1
                cardGroupsNeeded.append([category, cardsInGroup])
        return cardGroupsNeeded
    
    def handQuality(self, hand: list):
        handValue = 0
        handQual = None
        for card in hand: # Sum of card score
            handValue += card.score
        # Target is 21, 20, 19
        if handValue in [21, 20, 19]:
            return "Stand"
        # Find cards needed:
        valuesNeeded = [i-handValue for i in range(21, 18, -1)]
        # Get the base value for the hand
        if any(i >= 10 for i in valuesNeeded): # Cannot bust at all
            handQual = 1.0
        cardsNeeded = self.determineCardsNeeded(valuesNeeded)
        if len(cardsNeeded) == 2:
            pass
        else:
            cardsNeeded = cardsNeeded[0][0] # We know the 3 cards match up and there's only one category so we can ignore the rest
            if self.CARDGROUPS[cardsNeeded][0] == self.CARDGROUPS[self.nextCards][0]:
                handQual = 0.9 # Good scenario but not 100% reliable
            else:
                difference = abs(self.CARDGROUPS[self.nextCards][1] - self.CARDGROUPS[cardsNeeded][1])
                if difference == 1:
                    handQual = 0.75
                elif difference == 2:
                    handQual = 0.5
                else:
                    handQual = 0.25
        return handQual