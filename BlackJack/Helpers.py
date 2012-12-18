'''
Created on Dec 17, 2012

@author: Kevin
'''


# Constants and stuff
# Used by cardLookup to get info about a card
SUITS = ("h", "c", "d", "s")
FACE = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
FACE_VALUE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10)

class Action:
    '''
    The actions a player could make. My attempt at reproducing C-like enums
    '''
    (Stand, Hit, Split, Double) = range(0, 4)

def cardLookup(card):
    '''
    Returns a tuple of Face and Suit Symbols for a card.
    A card is an integer from 0-51
    '''
    face = card % 13
    suit = card / 13
    return (FACE[face], SUITS[suit])

def faceValue(card):
    '''
    Returns the lowest possible integer value of a card.
    A card is an integer from 0-51
    '''
    return FACE_VALUE[card % 13]
