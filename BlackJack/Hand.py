'''
Created on Dec 17, 2012

@author: Kevin
'''     

from BlackJack.Helpers import cardLookup, faceValue, FACE_VALUE, Action

# TODO: Remove the list dependency for accessing cards
class Hand(list):
    '''
    Contains all the important info about a player's hand. 
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        super(Hand, self).__init__(*args, **kwargs)
        self.action = list()
        self.bet = 0
        self.insurance = 0

    def __str__(self):
        return ("I" if self.insurance else "") + " ".join(("%2s%s" % cardLookup(c) for c in iter(self)))
    
    def minHandSum(self):
        '''
        Returns the hand value counting Aces as 1.
        '''
        handSum = 0
        for card in self:
            handSum += faceValue(card)
        return handSum
        # # This is slower:
        #    return sum([faceValue(card) for card in hand])
        
    def maxHandSum(self):
        '''
        Returns the hand value counting an Ace as 11. Only have to
        take into account one Ace, anymore is a guaranteed bust.
        '''
        handSum = self.minHandSum()
        # Only have to take into account one Ace, anymore is a guaranteed bust
        if self.isSoft():
            handSum += 10
        return handSum
    
    def isSoft(self):
        '''
        Returns True if the hand contains an Ace that could
        count as an 11 without busting.
        '''
        return (self.minHandSum() + 10 <= 21) and (FACE_VALUE[0] in (faceValue(c) for c in self))
    
    def isBJ(self):
        '''
        Returns True if the hand is a Black Jack.
        '''
        return (len(self) == 2) and self.isSoft() and self.minHandSum() == 11 and (Action.Split) not in list(self.action)

    def isWinner(self, dealer):
        '''
        Returns the bet multiplier for this hand vs the dealer's hand.
        '''
        #  1.5 player win with blackjack
        #  1   player win
        #  0   push
        # -1   player lose
        result = 0
        ds = dealer.maxHandSum()
        hs = self.maxHandSum()
        #Does dealer have blackjack?
        if dealer.isBJ():
            #Do I have blackjack?
            if self.isBJ():
                # Push
                result = 0
            else:
                # Lose
                result = -1
        #Do I have blackjack?
        elif self.isBJ():
            # BJ win
            result = 1.5
        #Without busting, do I beat the dealer or did the dealer bust?
        elif (ds < hs <= 21) or (hs <= 21 < ds):
            # Win
            result = 1
        #Without busting, do I tie the dealer?
        elif (ds == hs) and (hs <= 21):
            # Push
            result = 0
        else:
            # Lose
            result = -1
        return result