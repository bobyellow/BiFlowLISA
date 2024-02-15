# encoding: latin2
""" Contiguity matrix creator
"""
__author__ = "Ran Tao, modified from Juan C. Duque, Alejandro Betancourt"
__credits__ = "Copyright (c) 2010-11 Juan C. Duque"
__license__ = "New BSD License"
__version__ = "1.0.0"
__maintainer__ = "RiSE Group"
__email__ = "contacto@rise-group.org"
__all__ = ['WfromPolig']

import struct
import numpy
# from contiguity import weightsFromAreas
from os import path


# WfromPolig

def weightsFromFlows(AREAS1, AREAS2, FlowValue, Level):
    Wflow = {}  # Output as dictionary, for each item (flow), the key is its (O,D) tuple, the value includes all the (O,D) tuples of its neighbor flows
    Wflow1 = {}
    Wflow1O = {}
    Wflow1D = {}
    Wflow2 = {}
    Wflow12 = {}
    # Level=1: one of OD is the same and the other is neighbor; Level=2: both OD are neighbors
    # Read input files
    areas1 = AREAS1  # list of O area
    areas2 = AREAS2  # list of D area
    Wflowtrue = FlowValue  # flow data
    print 'Using contiguity WeightFromFlows'
    print 'running from contiguity'
    print 'Obtain O & D neighbors by contiguity (Rook or Queen)'
    print "Weight level is " + str(Level)
    Grid1Wrook = areas1.Wrook
    Grid2Wrook = areas2.Wrook
    # Grid2Wqueen = areas2.Wqueen
    KEY1 = Grid1Wrook.keys()
    KEY2 = Grid2Wrook.keys()
    yKeys = Wflowtrue.keys()
    # print len(KEY1)
    # print 'Obtain flow W matrix based on O & D W matrices'
    for key1Zero in range(len(KEY1)):
        for key2Zero in range(len(KEY2)):
            key1 = key1Zero + 1
            key2 = key2Zero + 1
            if (key1, key2) in yKeys:
                flowkey = (key1, key2)
                # print str(flowkey)
                # Wflow[flowkey]=[]
                Wflow1[flowkey] = []
                Wflow1O[flowkey] = []
                Wflow1D[flowkey] = []
                Wflow2[flowkey] = []
                Wflow12[flowkey] = []
                key1s = Grid1Wrook[key1Zero].append(key1Zero)  # to add the polygon itself to its neighbor list
                key2s = Grid2Wrook[key2Zero].append(key2Zero)
                set1 = set(Grid1Wrook[key1Zero])  # use set()to reorder and remove duplicates
                set2 = set(Grid2Wrook[key2Zero])
                list1 = list(set1)  # switch back to list for indexing
                list2 = list(set2)
                for key1p in range(len(list1)):
                    for key2p in range(len(list2)):
                        # if Wflowtrue[(key1p,key2p)]<> 0:
                        tp = (list1[key1p] + 1, list2[key2p] + 1)
                        if tp != (key1, key2) and tp in yKeys:
                            Wflow12[flowkey] += [tp]
                            if list1[key1p] + 1 != key1 and list2[key2p] + 1 != key2:
                                Wflow2[flowkey] += [tp]
                            elif list1[key1p] + 1 == key1:
                                Wflow1D[flowkey] += [tp]
                                Wflow1[flowkey] += [tp]
                            elif list2[key2p] + 1 == key2:
                                Wflow1O[flowkey] += [tp]
                                Wflow1[flowkey] += [tp]
                            else:
                                Wflow1[flowkey] += [tp]

    if Level == 1:
        Wflow = Wflow1
    elif Level == 18:
        Wflow = Wflow1O
    elif Level == 19:
        Wflow = Wflow1D
    elif Level == 10:
        Wflow = Wflow1
        for key in Wflow.keys():
            Wflow[key].append(key)
    elif Level == 108:
        Wflow = Wflow1O
        for key in Wflow.keys():
            Wflow[key].append(key)
    elif Level == 109:
        Wflow = Wflow1D
        for key in Wflow.keys():
            Wflow[key].append(key)
    elif Level == 2:
        Wflow = Wflow2
    elif Level == 12:
        Wflow = Wflow12
    elif Level == 120:
        Wflow = Wflow12
        for key in Wflow.keys():
            Wflow[key].append(key)
    else:
        Wflow = {}
        print 'you must choose a level of flow neighborhood'
    return Wflow
