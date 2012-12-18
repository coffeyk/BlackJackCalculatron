'''
Created on Dec 17, 2012

@author: Kevin
'''

from BlackJack.Helpers import cardLookup, faceValue, Action

def theBook(hand, dfv, count):
    '''
    Play a hand by 'the book' for a 6 deck, H17, double after split game
    '''
    # TODO: Implement count adjustments
    # TODO: Make a version that can take into account all of the rules automatically
    hs = hand.minHandSum()
    # (len(hand) == 2) is my check to see if doubling down is available.
    # Should be replaced by a canDouble function when unlimited debt is removed
    if (len(hand) == 2) and (cardLookup(hand[0])[0] == cardLookup(hand[1])[0]):
        # Pairs
        if faceValue(hand[0]) == 1: #ACE
            return Action.Split
        elif faceValue(hand[0]) == 10:
            return Action.Stand
        elif faceValue(hand[0]) == 9:
            if (dfv== 7) or (dfv == 10) or (dfv == 1):
                return Action.Stand
            else:
                return Action.Split
        elif faceValue(hand[0]) == 8:
            return Action.Split
        elif faceValue(hand[0]) >= 6:
            if (1 < dfv <= faceValue(hand[0])):
                return Action.Split
            else:
                return Action.Hit
        elif faceValue(hand[0]) == 5:
            if (2 <= dfv <= 9):
                return Action.Double
            else:
                return Action.Hit
        elif faceValue(hand[0]) == 4:
            if (dfv == 5) or (dfv == 6):
                return Action.Split
            else:
                return Action.Hit
        else:
            if (1 < dfv <= 7):
                return Action.Split
            else:
                return Action.Hit
    elif hand.isSoft():
        # Soft Hands
        if hs >= 10:
            return Action.Stand
        elif hs == 9:
            if (len(hand) == 2) and dfv == 6:
                return Action.Double
            else:
                return Action.Stand
        elif hs == 8:
            if (len(hand) == 2) and (2 <= dfv <= 6):
                return Action.Double
            elif dfv >= 9:
                return Action.Hit
            else:
                return Action.Stand
        elif hs == 7:
            if (len(hand) == 2) and (3 <= dfv <= 6):
                return Action.Double
            else:
                return Action.Hit
        elif hs == 5 or hs == 6:
            if (len(hand) == 2) and (4 <= dfv <= 6):
                return Action.Double
            else:
                return Action.Hit
        elif hs == 3 or hs == 4:
            if (len(hand) == 2) and (5 <= dfv <= 6):
                return Action.Double
            else:
                return Action.Hit
        else:
            print "ERROR"
            return Action.Stand #Shouldn't get here
    # Normal Hands
    elif hs >= 17:
        return Action.Stand
    elif hs >= 13:
        if (dfv >= 7):
            return Action.Hit
        else:
            return Action.Stand
    elif hs == 12:
        if dfv <= 3 or dfv >= 7:
            return Action.Hit
        else:
            return Action.Stand
    elif hs == 11:
        if (len(hand) == 2):
            return Action.Double
        else:
            return Action.Hit
    elif hs == 10:
        if (len(hand) == 2) and 1 < dfv < 10:
            return Action.Double
        else:
            return Action.Hit
    elif hs == 9:
        if (len(hand) == 2) and 3 <= dfv <= 6:
            return Action.Double
        else:
            return Action.Hit
    else:
        # hs <= 8 is hit
        return Action.Hit


# Play a hand as a dealer, Hits on S17
def theHouseH17(h, dfv, count):
    if h.minHandSum() >= 17 or h.maxHandSum() > 17 :
        return 0
    else:
        return 1

# Play a hand as a dealer, Stands on Soft 17
def theHouseS17(h, dfv, count):
    if h.maxHandSum() >= 17 :
        return 0
    else:
        return 1