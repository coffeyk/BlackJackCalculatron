'''
Created on Dec 17, 2012

@author: Kevin
'''
from BlackJack.Game import Game
INTERACTIVE = False
DEBUG = False

# TODO: Make this actually print logs from 'remote' processes in main window
# #log_to_stderr(10)

# TODO: unify the player count to start at n or n-1 

def fasterWorkerGame(PLAYERS, getBet=None, numShoes=10000):
    '''
    Accumulate the results of several games' fastCalcGameHistoryValue
    for a given number of players, betting strategy, and number of games
    '''
    netValue = 0
    netHands = 0
    
    for _ in xrange(numShoes):
        game = Game(players=PLAYERS - 1, decks=6)

        if getBet != None:
            for player in game.players:
                player.getBet = getBet
        
        game.playShoe()

        value, hands = game.fastCalcGameHistoryValue()

        netValue += value
        netHands += hands

    return netValue / (netHands * float((PLAYERS - 1)))

def workerGameBet(getBet):
    return workerGame(7, getBet)

def workerGame(PLAYERS, getBet=None):
    '''
    Accumulate the results of several games' calcGameHistoryValue
    for a given number of players and betting strategy
    '''
    wins = [0, ] * PLAYERS

#    for i in xrange(100000):
    for _ in xrange(1000):
        game = Game(players=PLAYERS - 1, decks=8)

        if getBet != None:
            for player in game.players:
                player.getBet = getBet
        
        # game.players[0].getBet = flatBet
        if INTERACTIVE:
            game.players[1].interactive = True
     
        game.playShoe()
        
        w = game.calcGameHistoryValue()

        wins = map(lambda x, y: x + y, w, wins)

        if DEBUG:
            print "-"*20

    return sum(wins[:PLAYERS - 1]) / (wins[PLAYERS - 1] * float((PLAYERS - 1)))


def workerHandEVByCount(players=6, numGames=1000):
    '''
    Accumulate the results of several game' calcHandEVByCount
    for a given number of players and games.
    '''
    totEV = {}

    for _ in xrange(numGames):
        game = Game(players=players, decks=6)

        game.playShoe()

        gHandEV = game.calcHandEVByCount()

        for (key, (gResult, gTotHands)) in gHandEV.iteritems():
            result, totHands = totEV.get(key, (0, 0))
            result += gResult
            totHands += gTotHands
            totEV[key] = (result, totHands)
    return totEV
