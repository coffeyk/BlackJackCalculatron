'''
Created on Dec 17, 2012

@author: Kevin
'''
from BlackJack.Hand import Hand
from BlackJack.PlayStyles import theBook
from BlackJack.BetStyles import getBet_Official
from BlackJack.Helpers import cardLookup, Action

class Player:
    def __init__(self):
        # Splits create multiple hands
        self.hands = [Hand()]
        # Called to determine the action this player takes
        self.playFunc = theBook
        # BE the player in this once in a lifetime experience. breaks in multithreading
        self.interactive = False

        # Called to determine the bet for the player
        self.getBet = getBet_Official

    def __str__(self):
        return "W:0 " + "\n".join(" ".join(("%2s%s" % cardLookup(c) for c in h)) for h in self.hands)

    def split(self, hIndex):
        '''
        Splits the hIndex'd hand into two new hands
        '''
        h1 = self.hands[hIndex]
        self.hands.insert(hIndex + 1, Hand((h1[-1],)))
        h1.pop()
        h2 = self.hands[hIndex + 1]
        h2.bet = h1.bet
        h2.action.append(Action.Split)


    def insurance(self, count):
        '''
        Returns the player's insurance bet, based on the count.
        '''
        # TODO: actually take insurance
        # TODO: abstract out the insurance function to allow for different strategies
        for h in self.hands:
            if count >= 2:
                h.insurance = 0  # self.getBet(count)
        
