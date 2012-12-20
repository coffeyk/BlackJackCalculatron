'''
Created on Dec 17, 2012

@author: Kevin
'''

INTERACTIVE = False
DEBUG = False

from BlackJack.Hand import Hand
from BlackJack.Player import Player
from BlackJack.PlayStyles import theHouseH17
from BlackJack.Helpers import Action, Card

import random

# Fixed seed helps spot functional changes to the algorithms
random.seed(0)

def getShoe(decks):
    '''
    Returns a shuffled shoe of n decks
    '''
    deck = [Card(c) for c in range(52)] * decks
    random.shuffle(deck)
    return deck

class Game:
    '''
    Keeps track of the deck, and the players past hands. 
    '''
    def __init__(self, players=1, decks=6):
        
        # Keeps track of all past hands for post processing
        self.history = []
        
        # The list of players in this shoe.
        # Dealer is always players[-1]
        self.players = [Player() for _ in xrange(players + 1)]
        
        self.deck = getShoe(decks)
        
        # The number of cards dealt so far.
        self.deckIdx = 0
        
        # The depth of the cut card. Once the cut card has been 
        # reached, no further rounds should be played.
        # TODO: deck penetration should be a configurable parameter
        self.deckEnd = int(len(self.deck) * 0.75)
        self.count = [-20]

        # the dealer sits in the last seat and has a special playRound function
        self.dealer = self.players[-1]
        self.dealer.getAction = theHouseH17

    def countCard(self, card):
        '''
        Implements the KO Strategy to card counting
        '''
        # 2 - 7 = +1
        # 8 , 9 =  0
        # 10- A = -1
        # TODO: Abstract out for different counting strategies
        adj = 0
        fv = card.faceValue
        if (2 <= fv <= 7):
            adj = 1
        elif 10 == fv or fv == 1:
            adj = -1
        self.count.append(self.count[-1] + adj)
        # print self.count
        
    def getCard(self):
        '''
        Returns the next card from the deck. Adjusts the count accordingly
        '''
        # TODO: allow players to use different counting strategies
        self.countCard(self.deck[self.deckIdx])
        self.deckIdx += 1
        return self.deck[self.deckIdx - 1]

    # probably slow?
    def archive(self):
        '''
        Stores the results of the round
        '''
        # TODO: use a nicer format for recording logs, perhaps a dictionary
        historyEntry = [(playerIdx, hand, hand.isWinner(self.dealer.hands[0]))
                        for (playerIdx, player) in enumerate(self.players)
                            for hand in player.hands]
        
        self.history.append(historyEntry)

    def playShoe(self):
        '''
        Plays out the rest of a shoe, until the cut card is reached.
        '''
        while self.deckIdx < self.deckEnd:        
            self.playRound()

    # #Black Jack Rules
    # # 0) get the money
    # # 1) Deal 2 cards to everyone
    # # 2) Dealer Card 1 an Ace?
    # # 2a) Offer Insurance
    # # 2b) Dealer BlackJack? End Game
    # # 3) Offer cards
    # # 3a) Hit -> goto 3
    # # 3b) Split -> goto 3
    # # 3c) Stand -> End
    # # 3d) Double -> End
    def playRound(self):
        '''
        Plays a single round of Black Jack.
        '''
        # Give the players new hands
        # 0)
        for player in self.players:
            player.hands = [Hand()]
            player.hands[0].bet = player.getBet(self.count[-1])
        # 1)
        for _ in xrange(2):
            for player in self.players:
                player.hands[0].cards.append(self.getCard())

        dealerHand = self.dealer.hands[0]
        dealerFaceValue = dealerHand.cards[0].faceValue

        if INTERACTIVE:
            for player in self.players:
                for hand in player.hands:
                    if player == self.dealer:
                        print "DEALER:"
                        print dealerFaceValue
                    else:
                        print hand.minHandSum(), hand
        
        # 2) Insurance
        if dealerFaceValue == 1:
            # Dealer ACE UP
            # Offer insurance
            for player in self.players:
                # The running count takes into consideration the dealers hole card,
                # which was the last card dealt. Therefore insurance should
                # be offered with the second to last count 
                player.insurance(self.count[-2])
        
        if dealerHand.isBJ():
            # Dealer BJ
            pass
        else:
            # 3) Offer cards
            allBust = True
            for player in self.players[:-1]:
                allBust &= self.playersTurn(player, dealerFaceValue)
                
            # Dealer is last player
            # Don't playRound dealer when everyone else is gone
            if not allBust:
                self.playersTurn(self.dealer, dealerFaceValue)

        # pprint ([str(player) for player in self.players])
        self.archive()

    # used to be part of Player class, but that gives players too much control
    def playersTurn(self, player, dealerFaceValue):
        '''
        Handles the given player's turn to play.
        '''
        # Assume the player busts by default
        previousHandsBust = True
        SPLIT_ACES = False
        for (hi, hand) in enumerate(player.hands):
            cards = hand.cards
            if (len(cards) < 2):
            # give newly created split hand its 2nd card
                cards.append(self.getCard())
                
            if hand.isBJ():
                continue
            
            if SPLIT_ACES:
                # Previous hand split Aces, so this hand can't do anything
                SPLIT_ACES = False
                continue

            # Default to hit so we make it into the while loop
            move = Action.Hit
            while move > Action.Stand and hand.minHandSum() < 21:
                if player.interactive:
                    print hand
                    print hand.minHandSum()
                    print """0)S 1)H 2)SP 3)DD """
                    move = input("What!: ")
                else:
                    move = player.getAction(hand, dealerFaceValue, self.count[-1])
                # Blindly accept players move
                # TODO: Validate player move
                hand.action.append(int(move))
                if move == Action.Hit:
                    cards.append(self.getCard())
                    
                elif move == Action.Split:
                    player.split(hi)
                    cards.append(self.getCard())
                    if cards[0].faceValue == 1:
                        SPLIT_ACES = True
                        # Stop after splitting Aces
                        move = Action.Stand
                elif move == Action.Double:
                    cards.append(self.getCard())
                    # Stop after a double down
                    move = Action.Stand
            if previousHandsBust:
                if hand.minHandSum() <= 21 and not hand.isBJ():
                    # At least one hand requires the dealer to play
                    previousHandsBust = False

        return previousHandsBust


    def calcGameHistoryValue(self):
        '''
        Returns each players payroll adjustment for all historyEntry in the game's history.
        The last list entry is the number of rounds played.
        '''
        roundId = 0
        
        # Keep track of the number of cards dealt so the count can be displayed
        cards = 0
        
        dealerEntry = self.history[0][-1]
        dealerId = dealerEntry[0]
        
        numPlayers = dealerId + 1
        wins = [0, ] * numPlayers
        
        for historyEntry in self.history:
            roundId += 1
            if DEBUG:
                print "%3d $%d" % (self.count[cards], self.dealer.getBet(self.count[cards]))
                print "%2i)  " % roundId,
            
            # dealerEntry's wins tracks number of historyEntry per game
            wins[dealerId] += 1
            
            dealerEntry = historyEntry[-1]
            dealerHand = dealerEntry[1]
    
            if DEBUG:
                print "%2d: " % dealerHand.maxHandSum(),
                print dealerHand
            for (playerID, hand, result) in historyEntry[:-1]:
                cards += len(hand.cards)
                
                # Did the player double down this hand?
                if Action.Double in list(hand.action):
                    wins[playerID] += result * hand.bet * 2
                else:
                    wins[playerID] += result * hand.bet
                
                # Does insurance pay out?
                if hand.insurance:
                    if dealerHand.isBJ():
                        wins[playerID] += hand.bet
                    else:
                        wins[playerID] -= hand.bet / 2
                    
                if DEBUG:
                    hs = hand.maxHandSum()
                    print " %d%2s  %2d: " % (playerID, ("D" if 3 in list(hand.action) else " ") + {0:"P", -1:"L", 1:"W", 1.5:"B"}[result], hs),
                    print hand,
                    print
            if DEBUG:
                print
        # dealer's wins tracks number of historyEntry per game
        wins[dealerId] = roundId
        
        return wins
    
    def fastCalcGameHistoryValue(self):
        '''
        Returns the net payroll adjustment of all players for all historyEntry in game's history,
        and the total number of historyEntry played.
        '''
        
        winnings = 0
        for historyEntry in self.history:           
            dealerEntry = historyEntry[-1]
            dealerHand = dealerEntry[1]
            
            # Exclude the last handEntry (dealer's)
            for (playerID, hand, result) in historyEntry[:-1]:
                # get the win/loss/BJ net result
                if Action.Double in list(hand.action):
                    result *= 2
                winnings += result * hand.bet
                
                # Does insurance pay out?
                if hand.insurance:
                    if dealerHand.isBJ():
                        winnings += hand.bet
                    else:
                        winnings -= hand.bet / 2
        
        return (winnings, len(self.history))
    
    def calcHandEVByCount(self):
        '''
        Returns the net value for all players, and the number of historyEntry played
        for each 'count' in the game's history.
        '''
        handEV = {}
    
        numCards = 0
        for historyEntry in self.history:
            count = self.count[numCards]
            netResult, totHands = handEV.get(count, (0, 0))
            totHands += len(self.players) - 1
            
            dealerEntry = historyEntry[-1]
            dealerHand = dealerEntry[1]
            
            for (playerID, hand, result) in historyEntry[:-1]:
                numCards += len(hand.cards)
                
                # EV does not take into account betting amount
                if Action.Double in list(hand.action):
                    result *= 2                
                # Does insurance pay out?
                if hand.insurance:
                    if dealerHand.isBJ():
                        result += 1
                    else:
                        result -= 0.5
                netResult += result
    
            handEV[count] = (netResult, totHands)
    
        return handEV
                
