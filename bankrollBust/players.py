from pygameUtils.rand import genRandFloat

class hand:
    def __init__(self, cards = None, bet = 0):
        self.cards = cards if cards else [] # If the cards aren't specified make an empty list
        self.bet = bet
        self.handValue = 0
        self.stood = False
        self.busted = False
        self.naturalBlackjack = False
        self.push = False

    def addCard(self, card):
        self.cards.append(card)

class player():
    def __init__(self, bustBux: int):
        self.name = "Player"
        self.bustBux = bustBux
        self.isPlayer = True
        self.isDealer = False
        # Variables that reset every round
        self.hands = [hand()]
        self.handIndex = 0
        self.totalBet = 0
        self.insurance = 0
        self.winnings = 0
        # Card Counting
        self.nextCardNeeded = None
        
    def bust(self, game):
        currentHand = self.hands[self.handIndex]
        game.bustPlayers += 1
        currentHand.busted = True
    
    def stand(self, game):
        if len(self.hands) > self.handIndex:
            currentHand = self.hands[self.handIndex]
            currentHand.stood = True
            if not self.isDealer: # Don't need to progress turn if they are the dealer
                game.progressTurn()

    def dealCard(self, game, visible = True):
        deck = game.deckInstance
        if len(self.hands) > self.handIndex:
            currentHand = self.hands[self.handIndex]
            if not game.debugMode:
                card = deck.getCard()
            # --- DEBUGGING PURPOSES --- #
            else:
                card = self.dealPresetCard(deck, game)
            # -------------------------- #
            # Set the card to visible if it should be
            if visible:
                card.setVisible()
                game.increaseCount(card) # As we can see the card, affect the count
            currentHand.addCard(card)
            self.checkBusted(game)
            self.checkBlackjack(game)

    # --- DEBUGGING PURPOSES --- #
    # Deal card method for debugging - Dealing preset cards
    def dealPresetCard(self, deck, game):
        # Get the key of preset cards
        key = None
        if self.isDealer:
            key = "dealer"
        elif self.isPlayer:
            key = "player"
        else:
            key = game.players.index(self)
        # Get the face of the card to be dealt
        if key in game.presetCards and game.presetCards[key]:
            face = game.presetCards[key].pop(0)
            # Find the first instance of the preset card in the deck
            for i, c in enumerate(deck.deck):
                if c.face == face:
                    card = deck.deck.pop(i)
                    break
            # Incase card isn't in deck
            else:
                card = deck.getCard()  
        # Incase key doesn't exist or list is empty
        else: 
            card = deck.getCard()
        return card
    # -------------------------- #

    def splitHand(self):
        currentHand = self.hands[self.handIndex] # Hand that is being split
        cardToSplit = currentHand.cards.pop(1) # Card that is getting seperated
        betOnNewHand = currentHand.bet # The current bet on the hand
        self.bustBux -= betOnNewHand # Adjusting player's balance
        self.totalBet += betOnNewHand # Adjusting player's total bet
        newHand = hand(cards=[cardToSplit], bet=betOnNewHand) # Creating the new hand object
        self.hands.insert(self.handIndex+1, newHand) # Adding the new hand next to the current one

    def makeBet(self, bet):
        self.hands[self.handIndex].bet = bet
        self.totalBet += bet
        self.bustBux -= bet

    def checkBusted(self, game):
        cardValues = self.getHandValue() # Get list of the card values
        # Check if the player has busted
        currentHand = self.hands[self.handIndex]
        if currentHand.handValue > 21: # Player might be bust
            if 11 in cardValues: # See if the player has the ace
                aceIndex = cardValues.index(11) # Get the location of the first ace
                currentHand.cards[aceIndex].value = 1 # Set the ace's value to 1
                currentHand.handValue -= 10 # Correct the player's hand value
            else: # Player has no ace and has bust
                self.bust(game)
                if not self.isDealer:
                    game.progressTurn()
        
    def checkBlackjack(self, game):
        self.getHandValue() # Ensure hand value up to date
        currentHand = self.hands[self.handIndex]
        if currentHand.handValue == 21: # Player has blackjack
            if len(self.hands) == 1 and len(currentHand.cards) == 2: # Player has natural blackjack
                currentHand.naturalBlackjack = True
            self.stand(game)

    def canSplit(self):
        currentHand = self.hands[self.handIndex].cards
        if len(currentHand) == 2:
             if currentHand[0].face == currentHand[1].face:
                 return True
        return False
    
    def canDoubleDown(self):
        if len(self.hands) == 1 and len(self.hands[0].cards) == 2 and not self.hands[0].stood: # Player hasn't acted meaning they can double down
            return True
        else:
            return False

    def getHandValue(self):
        # Get the value of the player's hand
        currentHand = self.hands[self.handIndex]
        totalSum = 0 # Creating variable for value
        cardValues = [card.value for card in currentHand.cards] # List of all values in the player's hand
        for value in cardValues: # Loop through the card values
            totalSum += value # Add them all together
        currentHand.handValue = totalSum # Making the handValue of the player object be the gathered value
        return cardValues # Useful for finding certain cards
    
    def getNextCardNeeded(self):
        currentHand = self.hands[self.handIndex]
        # ["A", -1],["2", 1],["3", 1],["4", 2],["5", 2],["6", 2],["7", 1],["8", 0],["9", 0],["10", -2],["J", -2],["Q", -2],["K", -2]
        # High cards have value of -2, low cards have value of 1 or -1, medium cards have value of 2, low-High has value of 0
        # It will always hit when >10 is needed so you can ignore -2 values
        # It will always stand with hand value of 17+ so ignore the cards less than 4
        # Types of card needed is High Medium Low
        neededCard = None
        valueNeeded = 21 - currentHand.handValue
        if 5 <= valueNeeded <= 6:
            neededCard = "medium"
        elif 7 <= valueNeeded <= 8:
            neededCard = "high"
        else:
            neededCard = "low"
        self.nextCardNeeded = neededCard

    def newRound(self):
        self.hands = [hand()]
        self.handIndex = 0
        self.totalBet = 0
        self.insurance = 0
        self.winnings = 0
    
class dealer(player):
    def __init__(self):
        super().__init__(-1)
        self.name = "Dealer"
        self.ACTIONS = ["hit", "stand"]
        self.isPlayer = False
        self.isDealer = True

    def decideNextMove(self):
        dealerHand = self.hands[0]
        dealerValues = [card.value for card in dealerHand.cards]
        action = None
        if dealerHand.handValue < 17:
            action = self.ACTIONS[0]
        elif 11 in dealerValues and dealerHand.handValue == 17:
            # Dealer must hit on soft 17
            action = self.ACTIONS[0]
        else:
            action = self.ACTIONS[1]
        return action

class NPC(player):
    def __init__(self, name: str, bustBux: int, personality: str,  prosperity: float, confidence: float, judgement: float, experience: float):
        super().__init__(bustBux)
        self.name = name
        self.personality = personality
        self.prosperity = prosperity
        self.confidence= confidence
        self.judgement = judgement
        self.experience = experience
        self.isPlayer = False
        self.ACTIONS = ["hit", "stand", "split", "insurance"]
        
    def decideNextMove(self, game):
        """
        Judgement - Affects how well the NPC perceives the quality of their hand
        Good hand vs Bad hand - We can define a good hand as having a high chance of getting close to 21 when we consider the card count
        A good hand will give a higher chance of hitting while a bad hand will lower the chance of hitting
        Players would know to stand on 17-20, to always hit on soft 17, players will always hit with a card score of less than 12
        """
        # Defining useful variables
        currentHand = self.hands[self.handIndex]
        trueCount = game.trueCount
        action = ""
        # Decision making
        decidedToSplit = False
        if self.canSplit():
            decidedToSplit = self.decideToSplit()
            
        if decidedToSplit:
            action = self.ACTIONS[2]
        elif self.decideToHit(game, currentHand):
            print("Hitting")
            action = self.ACTIONS[0]
        else: # Placeholder to have game move
            action = self.ACTIONS[1]
        return action
    
    def calculateBet(self):
        pass # min bet + (min-bet * prosperity) and current count something or other

    def getHandQuality(self, game, hand):
        # Get default hand value
        value = hand.handValue
        game.predictNextCard()
        self.getNextCardNeeded()
        if value <= 11:
            quality = 1.0
        elif value == 12:
            quality = 0.8
        elif value == 13:
            quality = 0.7
        elif value == 14:
            quality = 0.6
        elif value == 15:
            quality = 0.5
        elif value == 16:
            quality = 0.4
        elif value == 17:
            quality = 0.2
        else:
            quality = 0.0  # 18+ too risky to hit
        # Have the card needed affect the quality of the hand
        # If a higher card is needed hitting is riskier, if a low card is needed risk is lesser
        if self.nextCardNeeded == "low":
            quality += 0.1 
        elif self.nextCardNeeded == "high":
            quality -= 0.1  
        # Have the predicted card affect the 
        if game.predictedNextCard in ["strongLow", "weakLow"]:
            quality += 0.1  # next card likely low → safer to hit
        elif game.predictedNextCard in ["strongHigh", "weakHigh"]:
            quality -= 0.1  # next card likely high → riskier
        elif game.predictedNextCard == "medium":
            quality -= 0.05  # moderate risk
        # Keep quality between 1 and 0
        quality = round(max(0, min(1, quality)), 4)
        return quality

    def decideToHit(self, game, currentHand):
        quality = self.getHandQuality(game, currentHand) # Quality of hand
        # Lower requirement when quality is high
        minToHit = round(0.7 - (quality * 0.5), 4)
        # Higher floor when quality is high
        floatGeneratorFloor = 0.1 + (quality * 0.7)
        lowerBound = max(0.05, min(1.0, floatGeneratorFloor * self.experience)) # Adjust the floor to be affected by experience and keep it from being stuck at 0
        # Generate the chance of hitting
        generatedChance = genRandFloat(lowerBound, 1.0)
        print(quality, minToHit, generatedChance)
        return generatedChance > minToHit # Returns true if the generated chance is high enough

    def decideToSplit(self):
        chanceToSplit = genRandFloat(0.65,1)
        decidesToSplit = False
        chanceToSplit = chanceToSplit * self.experience
        if chanceToSplit > 0.75:
            decidesToSplit = True
        return decidesToSplit