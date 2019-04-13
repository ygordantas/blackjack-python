'''
Here are the requirements:

You need to create a simple text-based BlackJack game
The game needs to have one player versus an automated dealer.
The player can stand or hit.
The player must be able to pick their betting amount.
You need to keep track of the player's total money.
You need to alert the player of wins, losses, or busts, etc...
'''

import random

isPlayerRound = False
isComputerRound = False
isGameOn = False


class Card():
    def __init__(self, suit, name):
        self.suit = suit
        self.name = name
        self.value = 0

    def __str__(self):
        return f'--------\n{self.suit}\n {self.name}\n--------'

    def setValue(self, value):
        self.value = value


class Deck():
    def __init__(self):
        self.deck = []

    def createDeck(self):
        suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
        cardName = ['Ace', '2', '3', '4', '5', '6', '7',
                    '8', '9', '10', 'Jack', 'Queen', 'King']
        deck = []

        for suit in suits:
            for name in cardName:
                if name == 'Ace':
                    card = Card(suit, name)
                elif name == 'Jack' or name == 'Queen' or name == 'King':
                    card = Card(suit, name)
                    card.setValue(10)
                else:
                    card = Card(suit, name)
                    card.setValue(int(name))
                deck.append(card)

        # Shuffle deck
        random.shuffle(deck)

        self.deck = deck
        return 'Deck successfully created!'

    def reShuffle(self, pcHand=[], plHand=[]):
        fullDeck = self.deck + pcHand + plHand
        random.shuffle(fullDeck)
        self.deck = fullDeck
        return 'Deck shuffled and ready to go!'

    def drawCard(self):
        return self.deck.pop()


class Player():
    def __init__(self):
        self.balance = 0
        self.hand = []
        self.points = 0

    def setBalance(self, balance):
        self.balance = balance
        return f'Your balance is ${self.balance}'

    def addToHand(self, card):
        self.hand.append(card)
        return self.hand

    def clearHand(self):
        self.hand = []

    def setPoints(self, points=0):
        self.points = points


class ComputerDealer():
    def __init__(self):
        self.cardsFaceUp = []
        self.cardFaceDown = []
        self.balance = 0
        self.points = 0

    def setBalance(self, balance):
        self.balance = balance

    def drawCardFaceUp(self, card):
        self.cardsFaceUp.append(card)
        return self.cardsFaceUp

    def drawCardFaceDown(self, card):
        self.cardFaceDown.append(card)

    def clearHand(self):
        self.cardsFaceUp = []
        self.cardFaceDown = []

    def turnCardUp(self):
        # Remove card down placeholder. the placeholder is always going to be cardsFaceUp[1]
        self.cardsFaceUp.pop()

        self.cardsFaceUp += self.cardFaceDown
        self.cardFaceDown = []

    def setPoints(self, points=0):
        self.points = points


def displayHand(pcHand=[], playerHand=[]):
    if len(pcHand) == 1:
        pcHand.append('--------\n   BACK\n  CARD\n--------')
    print('** Computer Dealer Cards **')
    print("\n" * 1)
    print('----------')
    for c in pcHand:
        print(f"  {c}  ")
    print("\n" * 1)
    print('-------###################----------')
    print("\n" * 1)
    for c in playerHand:
        print(f"  {c}  ")
    print('----------')
    print("\n" * 1)
    print('** Your Cards **')


def askHitOrStay():
    inp = input('Do you want to HIT(h) or STAY(s)')
    while inp != 'h' and inp != 'H' and inp != 'S' and inp != 's':
        print('Invalid entry. Try again!')
        inp = input('Do you want to HIT(h) or STAY(s)')
    return inp.upper()


def calculatePoints(hand=[]):
    cardsValues = []
    for c in hand:
        cardsValues.append(c.value)
    return sum(cardsValues)


def playAnotherBetQuestion(plBalance, pcBalance):
    global isPlayerRound
    global isComputerRound
    global isGameOn

    # if you don't have a winner ask for a bet
    if not checkWinner(plBalance, pcBalance):
        inp = ''

        while inp != 'y' and inp != 'Y' and inp != 'n' and inp != 'N':
            inp = input('Place another bet? (y or n)')
        if inp.upper() == 'Y':
            isPlayerRound = False
            isComputerRound = False
        else:
            # Player does not want to place another bet. End the game.
            endGame()


def endGame():
    global isGameOn
    global isPlayerRound
    global isComputerRound

    isPlayerRound = False
    isComputerRound = False
    isGameOn = False
    print('Game Over')


def checkWinner(plBalance, pcBalance):

    if plBalance == 0:
        print('You are out of funds. Computer won!')
        endGame()
        return True
    elif pcBalance == 0:
        print('Computer is out of funds. You won!')
        endGame()
        return True
    return False


def assignAceValue(card):
    '''
    INPUT: a card object
    PROCESS: Check If card is an Ace. Then the function will aks the player to assing value of 11 or 1.
            Else it keeps the original value of the card
    '''

    if card.name == 'Ace':
        aceQuestion = input(
            'You just got an "Ace"! Do you want your card to have a value of 1 or 11?')
        while aceQuestion != '11' and aceQuestion != '1':
            aceQuestion = input(
                'You just got an "Ace"! Do you want your card to have a value of 1 or 11?')
        card.setValue(int(aceQuestion))


def wonRoundInfo(whoWon, pl, pc, bet, infoMsg):
    if whoWon == 'pl':
        displayHand(pc.cardsFaceUp, pl.hand)
        print(infoMsg)
        pl.setBalance(pl.balance + bet)
        pc.setBalance(pc.balance - bet)
        print(f'Your new balance is {pl.balance}')
        playAnotherBetQuestion(pl.balance, pc.balance)
    elif whoWon == 'pc':
        displayHand(pc.cardsFaceUp, pl.hand)
        print(infoMsg)
        pl.setBalance(pl.balance - bet)
        pc.setBalance(pc.balance + bet)
        print(f'Your new balance is {pl.balance}')
        playAnotherBetQuestion(pl.balance, pc.balance)


def init():
    print("Let's get started!")

    # Create a deck
    global deck
    deck = Deck()
    deck.createDeck()

    # Create player
    global pl
    pl = Player()

    # Create computer dealer
    global pc
    pc = ComputerDealer()

    # Player chooses how much credits to start with.
    while True:
        balance = 0
        try:
            balance = int(
                input('First choose how much your balance is going to be: '))
            if balance <= 0:
                raise Exception('Balance must be greater than 0')
        except:
            print('Please enter a valid number')
        else:
            # Computer dealer and player are going to have same amount of credits in the beggining of the game
            pl.setBalance(balance)
            pc.setBalance(balance)
            break
    game()


def game():

    global isGameOn
    global isPlayerRound
    global isComputerRound

    isGameOn = True

    print('Game on!')
    print('Rules: For this blackjack game you have only two options HIT or STAY')
    print('For HIT press (h) your keyboard and for STAY press (s)')

    while isGameOn:
        # Set bet
        bet = 0

        while True:
            try:
                bet = int(input('How much do you want to bet?'))
                if bet <= 0 or bet > pl.balance:
                    raise Exception('Invalid amount')
            except:
                print('Invalid amount. Please try again')
            else:
                print(f'Nice, you are betting {bet}')
                break

        # Reshuffle deck
        pcHand = pc.cardFaceDown + pc.cardsFaceUp
        deck.reShuffle(pcHand, pl.hand)

        # Empty players hands
        pl.clearHand()
        pc.clearHand()

        # Clear points
        pl.setPoints()
        pc.setPoints()

        # Draw cards

        # -- Player goes first drawing 2 cards
        pl.addToHand(deck.drawCard())
        pl.addToHand(deck.drawCard())

        # -- Computer Dealer draw 2 cards (1 face up and 1 face down)
        pc.drawCardFaceUp(deck.drawCard())
        pc.drawCardFaceDown(deck.drawCard())

        displayHand(pc.cardsFaceUp, pl.hand)

        # Check for aces in player's hand and assign them 1 or 11 values
        for card in pl.hand:
            assignAceValue(card)

        # Sum players cards points to check if he won the round
        pl.setPoints(calculatePoints(pl.hand))
        if pl.points == 21:
            wonRoundInfo('pl', pl, pc, bet, 'You won the bet! :)')
        else:
            isPlayerRound = True

        while isPlayerRound:

            # Player chooses (HIT or STAY)
            if askHitOrStay() == 'H':
                newCard = deck.drawCard()
                print(newCard)
                assignAceValue(newCard)
                pl.addToHand(newCard)

                #  Sum cards
                pl.setPoints(calculatePoints(pl.hand))

                if pl.points > 21:
                    wonRoundInfo('pc', pl, pc, bet,
                                 'BUST! you lost your bet :(')

                elif pl.points == 21:
                    wonRoundInfo('pl', pl, pc, bet, 'You won the bet :)')
                else:
                    # Player still has < 21 pts ... Starts round again
                    displayHand(pc.cardsFaceUp, pl.hand)
                    print(f'Your cards currently sum {pl.points}')
            else:
                #  If player decides to stays then PC's turn starts
                pl.setPoints(calculatePoints(pl.hand))

                isPlayerRound = False
                isComputerRound = True

                print('*** Computer dealer\'s turn ***')

                #  Turn pc cards face down up
                pc.turnCardUp()

                displayHand(pc.cardsFaceUp, pl.hand)

            print("\n" * 5)

        while isComputerRound:

            pc.setPoints(calculatePoints(pc.cardsFaceUp))

            # Loop through pc cards and assign aces values
            # The first aces are always going to be 11 and the latest aces will be 1
            for card in pc.cardsFaceUp:
                if card.value == 0:
                    if (pc.points + 11) <= 21:
                        card.setValue(11)
                    else:
                        card.setValue(1)
                    # Update PC points
                    print(
                        f'Computer choose its Ace to have a value of {card.value}')
                    pc.setPoints(calculatePoints(pc.cardsFaceUp))

            if pc.points > pl.points and pc.points <= 21:
                wonRoundInfo('pc', pl, pc, bet, 'Computer wins the bet')
            elif pc.points > 21:
                wonRoundInfo('pl', pl, pc, bet,
                             'Computer BUSTED... You WON the bet :)')
            else:
                pc.drawCardFaceUp(deck.drawCard())
                displayHand(pc.cardsFaceUp, pl.hand)
            print("\n" * 5)


init()
