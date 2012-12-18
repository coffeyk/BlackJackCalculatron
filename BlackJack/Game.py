'''
Created on Dec 17, 2012

@author: Kevin
'''

INTERACTIVE = False
DEBUG = False

from BlackJack.Hand import Hand
from BlackJack.Player import Player
from BlackJack.PlayStyles import theHouseH17
from BlackJack.Helpers import faceValue, Action

import random

# Fixed seed helps spot functional changes to the algorithms
random.seed(0)

def getShoe(decks):
    '''
    Returns a shuffled shoe of n decks
    '''
    deck = range(52) * decks
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
        self.dealer.playFunc = theHouseH17

    def countCard(self, card):
        '''
        Implements the KO Strategy to card counting
        '''
        # 2 - 7 = +1
        # 8 , 9 =  0
        # 10- A = -1
        # TODO: Abstract out for different counting strategies
        adj = 0
        fv = faceValue(card)
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
        # TODO: use a nicer format for recording logs
        hands = [(playerIdx, hand, hand.isWinner(self.dealer.hands[0]))
                    for (playerIdx, player) in enumerate(self.players)
                        for hand in player.hands]
        
        self.history.append(hands)

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
        for player in self.players:
            player.hands = [Hand()]
        
        # 0)
        for player in self.players:
            player.hands[0].bet = player.getBet(self.count[-1])
        # 1)
        for _ in xrange(2):
            for player in self.players:
                player.hands[0].append(self.getCard())

        dh = self.dealer.hands[0]
        dealerFaceValue = faceValue(dh[0])

        if INTERACTIVE:
            for player in self.players:
                for hand in player.hands:
                    if player == self.dealer:
                        print "DEALER:"
                    if player != self.dealer:
                        print hand.minHandSum(), hand
                    else:
                        print dealerFaceValue
        
        # 2) Insurance
        if dealerFaceValue == 1:
            # Dealer ACE UP
            # Offer insurance
            for player in self.players:
                player.insurance(self.count[-1])
        
        if dh.isBJ():
            # Dealer BJ
            pass
        else:
            # 3) Offer cards
            allBust = True
            for player in self.players:
                
                # Dealer is last player
                if player == self.dealer and allBust:
                    # Don't playRound dealer when everyone else is gone
                        continue
                else:
                    allBust &= self.playersTurn(player, dealerFaceValue)

        # pprint ([str(player) for player in self.players])
        self.archive()

    # used to be part of Player class, but that gives players too much control
    def playersTurn(self, player, dealerFaceValue):
        '''
        Handles the given player's turn to play.
        '''
        busted = True
        SPLIT_ACES = False
        for (hi, h) in enumerate(player.hands):
            # give other split its 2nd card
            if (len(h) < 2):
                h.append(self.getCard())
                
            if h.isBJ():
                continue
            
            if SPLIT_ACES:
                SPLIT_ACES = False
                continue

            move = 1
            while move > 0 and h.minHandSum() < 21:
                if player.interactive:
                    print h
                    print h.minHandSum()
                    print """0)S 1)H 2)SP 3)DD """
                    move = input("What!: ")
                else:
                    move = player.playFunc(h, dealerFaceValue, self.count[-1])
                # Blindly accept players move
                # TODO: Validate player move
                h.action.append(int(move))
                if move == Action.Hit:
                    h.append(self.getCard())
                    
                elif move == Action.Split:
                    player.split(hi)
                    h.append(self.getCard())
                    if faceValue(h[0]) == 1:
                        SPLIT_ACES = True
                        move = -1   
                elif move == Action.Double:
                    # Stop after a double down
                    h.append(self.getCard())
                    move = -1             
            if busted:
                if h.minHandSum() <= 21 and not h.isBJ():
                    busted = False

        return busted


    def calcGameHistoryValue(self):
        '''
        Returns each players payroll adjustment for all hands in the game's history.
        The last list entry is the number of rounds played.
        '''
        c = 1
        cards = 0
        numPlayers = self.history[0][-1][0] + 1
        wins = [0, ] * numPlayers
        
        for hands in self.history:
            if DEBUG:
                print "%3d $%d" % (self.count[cards], self.dealer.getBet(self.count[cards]))
                print "%2i)  " % c,
            c += 1
            dealer = hands[-1]
            d = dealer[1].maxHandSum()
            # dealer's wins tracks number of hands per game
            wins[dealer[0]] += 1
    
            if DEBUG:
                print "%2d: " % d,
                print dealer[1]
            for hand in hands:
                cards += len(hand[1])
                
                if hand[0] == dealer[0]:
                    continue
                
                result = hand[2]
                if Action.Double in list(hand[1].action):
                    result *= 2
                wins[hand[0]] += result * hand[1].bet
                
                if hand[1].insurance and dealer[1].isBJ():
                    wins[hand[0]] += hand[1].insurance * 2
                else:
                    # when insurance is 0, this has no effect
                    wins[hand[0]] -= hand[1].insurance
                if DEBUG:
                    hs = hand[1].maxHandSum()
                    print " %d%2s  %2d: " % (hand[0], ("D" if 3 in list(hand[1].action) else " ") + {0:"P", -1:"L", 1:"W", 1.5:"B"}[hand[2]], hs),
                    print hand[1],
                    print
            if DEBUG:
                print
        return wins
    
    def fastCalcGameHistoryValue(self):
        '''
        Returns the net payroll adjustment of all players for all hands in game's history,
        and the total number of hands played.
        '''
        wins = 0
        totHands = 0
        
        for hands in self.history:
            
            dealer = hands[-1]
#            d = dealer[1].maxHandSum()
    
            totHands += 1
            
            for hand in hands:
                if hand[0] == dealer[0]:
                    continue
    
                # get the win/loss/BJ result
                result = hand[2]
                if Action.Double in list(hand[1].action):
                    result *= 2
                wins += result * hand[1].bet
    
                # calculate insurance win/loss
                if hand[1].insurance and dealer[1].isBJ():
                    wins += hand[1].insurance * 2
                else:
                    # when insurance is 0, this has no effect
                    wins -= hand[1].insurance
        
        return (wins, totHands)
    
    def calcHandEVByCount(self):
        '''
        Returns the net value for all players, and the number of hands played
        for each 'count' in the game's history.
        '''
        handEV = {}
        totHands = 0
    
        cards = 0
        for hands in self.history:
            dealer = hands[-1]
    
            count = self.count[cards]
            result, totHands = handEV.get(count, (0, 0))
            totHands += len(self.players) - 1
            for hand in hands:
                cards += len(hand[1])
                
                if hand[0] == dealer[0]:
                    continue
                
                r = hand[2]
                if Action.Double in list(hand[1].action):
                    r *= 2
                # TODO: Insurance
                    
                result += r
    
            handEV[count] = (result, totHands)
    
        return handEV
                
