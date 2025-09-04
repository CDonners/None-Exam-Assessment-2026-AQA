class countingCards():
    def __init__(self):
        self.runningCount = 0
        self.trueCount = 0
    
    def decisionMaking(self, hand: list):
        handValue = hand[0].value