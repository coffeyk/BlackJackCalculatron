'''
Created on Dec 17, 2012

@author: Kevin
'''

from BlackJack.Helpers import cardLookup, faceValue, Action

def theBook(hand, dealerFV, count):
    '''
    Play a hand by 'the book' for a 6 deck, H17, double after split game
    '''
    # TODO: Implement count adjustments
    # TODO: Make a version that can take into account all of the rules automatically
    handSum = hand.minHandSum()
    
    cards = hand.cards
    firstFV = faceValue(cards[0])
    
    # hasTwoCards is my check to see if doubling down is available.
    # Should be replaced by a canDouble function when unlimited debt is removed
    hasTwoCards = (len(hand.cards) == 2)
    if hasTwoCards and (cardLookup(cards[0])[0] == cardLookup(cards[1])[0]):
        # Pairs
        if firstFV == 1:  # ACE
            return Action.Split
        elif firstFV == 10:
            return Action.Stand
        elif firstFV == 9:
            if (dealerFV == 7) or (dealerFV == 10) or (dealerFV == 1):
                return Action.Stand
            else:
                return Action.Split
        elif firstFV == 8:
            return Action.Split
        elif firstFV >= 6:
            if (1 < dealerFV <= firstFV):
                return Action.Split
            else:
                return Action.Hit
        elif firstFV == 5:
            if (2 <= dealerFV <= 9):
                return Action.Double
            else:
                return Action.Hit
        elif firstFV == 4:
            if (dealerFV == 5) or (dealerFV == 6):
                return Action.Split
            else:
                return Action.Hit
        else:
            if (1 < dealerFV <= 7):
                return Action.Split
            else:
                return Action.Hit
    elif hand.isSoft():
        # Soft Hands
        if handSum >= 10:
            return Action.Stand
        elif handSum == 9:
            if hasTwoCards and dealerFV == 6:
                return Action.Double
            else:
                return Action.Stand
        elif handSum == 8:
            if hasTwoCards and (2 <= dealerFV <= 6):
                return Action.Double
            elif dealerFV >= 9:
                return Action.Hit
            else:
                return Action.Stand
        elif handSum == 7:
            if hasTwoCards and (3 <= dealerFV <= 6):
                return Action.Double
            else:
                return Action.Hit
        elif handSum == 5 or handSum == 6:
            if hasTwoCards and (4 <= dealerFV <= 6):
                return Action.Double
            else:
                return Action.Hit
        elif handSum == 3 or handSum == 4:
            if hasTwoCards and (5 <= dealerFV <= 6):
                return Action.Double
            else:
                return Action.Hit
        else:
            print "ERROR"
            return Action.Stand  # Shouldn't get here
    # Normal Hands
    elif handSum >= 17:
        return Action.Stand
    elif handSum >= 13:
        if (dealerFV >= 7):
            return Action.Hit
        else:
            return Action.Stand
    elif handSum == 12:
        if dealerFV <= 3 or dealerFV >= 7:
            return Action.Hit
        else:
            return Action.Stand
    elif handSum == 11:
        if hasTwoCards:
            return Action.Double
        else:
            return Action.Hit
    elif handSum == 10:
        if hasTwoCards and 1 < dealerFV < 10:
            return Action.Double
        else:
            return Action.Hit
    elif handSum == 9:
        if hasTwoCards and 3 <= dealerFV <= 6:
            return Action.Double
        else:
            return Action.Hit
    else:
        # handSum <= 8 is hit
        return Action.Hit


# Play a hand as a dealer, Hits on S17
def theHouseH17(hand, dealerFV, count):
    if hand.minHandSum() >= 17 or hand.maxHandSum() > 17 :
        return 0
    else:
        return 1

# Play a hand as a dealer, Stands on Soft 17
def theHouseS17(hand, dealerFV, count):
    if hand.maxHandSum() >= 17 :
        return 0
    else:
        return 1
