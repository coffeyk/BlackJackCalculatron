'''
Created on Dec 17, 2012

@author: Kevin
'''     

from BlackJack.Helpers import cardLookup, FACE_VALUE, Action    

class Hand:
    '''
    Contains all the important info about a player's hand. 
    '''
    
    def __init__(self, cards=None):
        '''
        Constructor
        '''
        # Expressions in default arguments are only calculated once, so we need this check!
        if cards is None:
            cards = list()
        
        self.cards = cards
        self.action = list()
        self.bet = 0
        self.insurance = False

    def __str__(self):
        return ("I" if self.insurance else "") + " ".join(("%2s%s" % cardLookup(c) for c in self.cards))
    
    def __repr__(self):
        return self.__str__()
    
    def minHandSum(self):
        '''
        Returns the hand value counting Aces as 1.
        '''
        handSum = 0
        for card in self.cards:
            handSum += card.faceValue
        return handSum
        # # This is slower:
        #    return sum([card.faceValue for card in hand])
        
    def maxHandSum(self):
        '''
        Returns the hand value counting an Ace as 11. Only have to
        take into account one Ace, anymore is a guaranteed bust.
        '''
        handSum = self.minHandSum()
        # Only have to take into account one Ace, anymore is a guaranteed bust
        if self.isSoft(handSum):
            handSum += 10
        return handSum
    
    def isSoft(self, mHandSum=None):
        '''
        Returns True if the hand contains an Ace that could
        count as an 11 without busting.
        '''
        # Don't want to keep calculating minHandSum unnecessarily
        # Passing in a min hand sum makes this slightly faster. 
        if mHandSum == None:
            mHandSum = self.minHandSum()
        return (mHandSum + 10 <= 21) and (FACE_VALUE[0] in (c.faceValue for c in self.cards))
    
    def isBJ(self):
        '''
        Returns True if the hand is a Black Jack.
        '''
        if (len(self.cards) == 2):
            mHandSum = self.minHandSum()
            return  mHandSum == 11 and (Action.Split) not in list(self.action) and self.isSoft(mHandSum)
        else:
            return False

    def isWinner(self, dealer):
        '''
        Returns the bet multiplier for this hand vs the dealer's hand.
        '''
        #  1.5 player win with blackjack
        #  1   player win
        #  0   push
        # -1   player lose
        result = 0

        # Does dealer have blackjack?
        if dealer.isBJ():
            # Do I have blackjack?
            if self.isBJ():
                # Push
                result = 0
            else:
                # Lose
                result = -1
        # Do I have blackjack?
        elif self.isBJ():
            # BJ win
            result = 1.5
        # Without busting, do I beat the dealer or did the dealer bust?
        else:
            ds = dealer.maxHandSum()
            hs = self.maxHandSum()
            if (ds < hs <= 21) or (hs <= 21 < ds):
                # Win
                result = 1
            # Without busting, do I tie the dealer?
            elif (ds == hs) and (hs <= 21):
                # Push
                result = 0
            else:
                # Lose
                result = -1
        return result
