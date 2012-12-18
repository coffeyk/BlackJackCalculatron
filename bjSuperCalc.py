'''
Created on Dec 17, 2012

@author: Kevin
'''

from pprint import pprint
import time
import pickle

import cloud
from blackJackWorkers import workerHandEVByCount

from pycloud_config import pycloudKey


cloud.setkey(3220, pycloudKey)


def cloudHandEVByCount(players=6, TOTAL_SHOES=100000000, CHUNKING=100000):
    '''
    Accumulate the calcHandEVByCount of __many__ games using pycloud.
    '''
    CHUNKS = TOTAL_SHOES / CHUNKING
    totEV = {}
    totEVName = "HandEVByCount-%d-p%d.p" % (TOTAL_SHOES, players)
    
    # benchmarking
    start = time.clock()
    
    cloudIds = cloud.map(workerHandEVByCount, (players,)*CHUNKS, (CHUNKING,)*CHUNKS)
    
    for ev in cloud.iresult(cloudIds, ignore_errors=True):
        if not isinstance(ev, dict):
            print "error"
            print ev
        else:
            for (key, (gResult, gTotHands)) in ev.iteritems():
                result, totHands = totEV.get(key, (0,0))
                result += gResult
                totHands += gTotHands
                totEV[key] = (result, totHands)

    # benchmarking
    end = time.clock()
    print end-start
    
    totEVFile = open(totEVName, 'w')
    pickle.dump(totEV, totEVFile)
    totEVFile.close
    
    return totEV

#
#def getValue(EV, getBet):
#    tot = 0
#    hands = 0
#    for count, (r, h) in EV.items():
#        tot += getBet(count) * r
#        hands += h
#    return tot/hands

if __name__ == '__main__':
    print "AND GO!"
##    totEV = cloudHandEVByCount(players=6, TOTAL_SHOES=100000000, CHUNKING=50000)

    totEVName = "HandEVByCount-%d-p%d.p" % (100000000, 6)
    totEVFile = open(totEVName, 'r')
    totEV = pickle.load(totEVFile)
    totEVFile.close()
##    pprint(totEV)
    keys = totEV.keys()
    keys.sort(int.__cmp__)
    hs = sum((x[1] for x in totEV.itervalues()))
    totHands = 0
    glVal = [0,0]
    glHands = [0,0]
    for key, (r, h) in ((x, totEV[x]) for x in keys):
        totHands += h
        glVal[key < -2] += r
        glHands[key < -2] += h

        print "%3d: %10.1f / %9d , %8.5f %12.8f" % (key, r, h, (100.0*(r + (h-r)/2.0)/h)-50.0, totHands*100.0/hs)

    for val, hands in zip(glVal, glHands):
        print val, hands, hands*1.0/totHands, val/hands
