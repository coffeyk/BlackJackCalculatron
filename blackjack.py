'''
Created on Dec 17, 2012

@author: Kevin
'''

INTERACTIVE = False
DEBUG = False

from multiprocessing import Pool
import cProfile
from pprint import pprint
import pdb
import time

# External libraries
# #import matplotlib.pyplot as plt

from BlackJack.BetStyles import GET_BET
from blackJackWorkers import workerGame, workerGameBet

# #def playShoe():
# #    for _ in xrange(10000):
# #        g = Game(players = 2, decks=6)
# #        g.players[0].getBet = flatBet
# #        g.playShoe()
# #
# #cProfile.run('playShoe()')

# #for i in range(len(graphs[0])):
# #    rt = 0
# #    for g in graphs[:PLAYERS-1]:
# #        rt += g[i]
# #    graphs[PLAYERS-1][i] = rt

def calcWinPerPlayers():
    '''
    Play by the book with anywhere from 2 - 7 players, and report the results.
    Answers the question if the number of players makes a difference.
    '''
    pool = Pool(processes=1)
    
    winPct = [list() for _ in xrange(3, 8)]
    for win in winPct:
        win.append(0)
    for j in range(3, 8):
        plrPct = []
        for i in range(1):
            plrPct.extend(pool.map(workerGame, (j,) * 2))

        tot = 0
        # winPct[j].append(0) 
        for idx, res in enumerate(plrPct, 1):
            tot += res
            winPct[j - 3].append(tot / float(idx))
# #    for wg in winPct:
# #        plt.plot(wg)
# #    plt.savefig("blackjack_HANDSWIN%03d.png"%i)
    pool.close()
    return winPct
# #    plt.show()       


def calcWinPerBetting(numPlayers):
    '''
    Try out different betting strategies for a specific number of players.
    Answers the question of which betting strategy is best.
    '''
    pool = Pool(processes=2)

    size = len(GET_BET)
    
    winPct = [list() for _ in range(size)]
    for win in winPct:
        win.append(0)
    for j, getBet in enumerate(GET_BET):
        start = time.clock()
        plrPct = pool.map(workerGameBet, (getBet,) * 21)
        end = time.clock()
        tot = 0
        for idx, res in enumerate(plrPct, 1):
            tot += res
            winPct[j].append(tot / float(idx))
        print getBet, winPct[j][-1], end - start
# #        plt.plot(winPct[j])
# #        plt.show()
    for getBet, wg in zip(GET_BET, winPct):
# #        plt.plot(wg)
        print getBet, wg[-1]
# #    plt.savefig("blackjack_HANDSWIN%03d.png"%i)
    pool.close()
# #    plt.show()

if __name__ == '__main__':
    win = calcWinPerPlayers()
    print win
# #    calcWinPerBetting(6)
