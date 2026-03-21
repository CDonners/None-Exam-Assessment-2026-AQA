from pygameUtils.rand import genRandInt

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
        if currentHand.handValue < 12: # Always hit when hand value bellow 12
            action = self.ACTIONS[0]
        elif 17 <= currentHand.handValue <= 20: # Always stand with hand value between these points
            action = self.ACTIONS[1]
        else: # Placeholder to have game move
            action = self.ACTIONS[0]
        return action
    
    def calculateBet(self):
        pass # min bet + (min-bet * prosperity) and current count something or other

    def decideToSplit(self):
        print(self.experience)
        defaultChanceToSplit = 0.9
        decidesToSplit = False
        chanceToSplit = defaultChanceToSplit * self.experience
        if chanceToSplit > 0.75:
            decidesToSplit = True
        return decidesToSplit