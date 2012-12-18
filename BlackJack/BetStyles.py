'''
Created on Dec 17, 2012

@author: Kevin
'''

# The betting functions. Can be given to a player to use
def flatBet(count):
    return 15

def getBet_Simple(count):
    if count >= 10:
        return 100
    elif count >= 2:
        return 75
    elif count >= -4:
        return 50
    else:
        return 15

def getBet_Smooth(count):
    if count >= 2:
        return 25 + (count * 20)
    else:
        return 15  # 15

def getBet_Official(count):  # Official
    if count >= 4:
        r = 75
    elif count >= 2:
        r = 50
    elif count >= -1:
        r = 25
    elif count > -4:
        r = 10
    else:
        r = 5
    return r * 3

def getBet_Ours(count):
    if count >= 4:
        r = 150
    elif count >= 2:
        r = 100
    elif count >= -1:
        r = 75
    elif count > -4:
        r = 50
    else:
        r = 15
    return r

# TODO: Should use introspection here
GET_BET = [getBet_Official, getBet_Ours, getBet_Simple, getBet_Smooth]
