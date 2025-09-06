from cardLogic import cards, playCards

playCards = playCards(4)
playCards.shuffle()

for i in playCards.deck:
    print(i.value)