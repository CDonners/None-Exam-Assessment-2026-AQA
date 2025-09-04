class countingCards():
    def __init__(self):
        self.runningCount = 0
        self.trueCount = 0
    
    def handQuality(self, hand: list):
        handValue = 0
        for card in hand:
            handValue += card.score
        # Target is 21, 20, 19
        if handValue in [21, 20, 19]:
            return "Stand"
        # Find cards needed:
        valuesNeeded = [i-handValue for i in range(21, 18, -1)]
        # Higher the count, the more high cards there are, JQK are high, 789 are mid, 456 are lowish, 23 are low A, is low and high
        