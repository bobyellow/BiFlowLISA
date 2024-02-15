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
from os import path

# WfromPolig

def STweightsFromFlows(AREAS1,AREAS2,FlowValue1,FlowValue2, Time1, Time2, Level):
    #Wflow = {} #Output as dictionary, for each item (flow), the key is its (O,D,T) tuple, the value includes all the (O,D) tuples of its neighbor flows
    Wflow1 = {}
    Wflow1O = {}
    Wflow1D = {}
    Wflow2 = {}
    Wflow12 = {}
    WflowCont = {}
    WflowContO = {}
    WflowContD = {}
    WflowContOD = {}
    WflowCont2 = {}
    WflowLaggedDown = {}
    WflowLaggedDownO = {}
    WflowLaggedDownD = {}
    WflowLaggedDownOD = {}
    WflowLaggedDown2 = {}
    WflowHybrid = {}
    # Level=1: one of OD is the same and the other is neighbor; Level=2: both OD are neighbors
    # Level=3: Contemporaneous   Level =49: Lagged
    #Read input files
    areas1 = AREAS1 #list of O area
    areas2 = AREAS2 #list of D area
    Wflowtrue = FlowValue2 #flow data
    WflowMinusOne = FlowValue1 #t-1 flow data


    print 'Obtain O & D neighbors by contiguity (Rook or Queen)'
    Grid1Wrook = areas1.Wrook
    Grid2Wrook = areas2.Wrook
    #Grid2Wqueen = areas2.Wqueen
    KEY1 = Grid1Wrook.keys()
    KEY2 = Grid2Wrook.keys()
    yKeys = Wflowtrue.keys()
    yKeysMinusOne = WflowMinusOne.keys()

    print "you're using this py file"
    for key1Zero in range(len(KEY1)):  #because the ID in .shp started from zero.
        for key2Zero in range(len(KEY2)):    #because the ID in .shp started from zero.
            key1 = key1Zero+1
            key2 = key2Zero+1
            if (key1,key2) in yKeys:
                flowkey = (key1,key2,Time2)

                Wflow1[flowkey]=[]
                Wflow1O[flowkey]=[]
                Wflow1D[flowkey]=[]
                Wflow2[flowkey]=[]
                Wflow12[flowkey]=[]
                WflowCont[flowkey]=[]
                WflowContO[flowkey] = []
                WflowContD[flowkey] = []
                WflowContOD[flowkey] = []
                WflowCont2[flowkey] =[]
                WflowLaggedDown[flowkey] = []
                WflowLaggedDownO[flowkey] = []
                WflowLaggedDownD[flowkey] = []
                WflowLaggedDownOD[flowkey] = []
                WflowLaggedDown2[flowkey] = []
                WflowHybrid[flowkey] = []

                key1s=Grid1Wrook[key1Zero].append(key1Zero)#to add the polygon itself to its neighbor list
                key2s=Grid2Wrook[key2Zero].append(key2Zero)
                set1 = set(Grid1Wrook[key1Zero])#use set()to reorder and remove duplicates
                set2 = set(Grid2Wrook[key2Zero])
                list1 = list(set1)#switch back to list for indexing
                list2 = list(set2)
                for key1p in range(len(list1)):
                    for key2p in range(len(list2)):
                        tp = (list1[key1p]+1, list2[key2p]+1)
                        if tp != (key1,key2) and tp in yKeys: #the neighbor flow cannot be the main flow
                            tp = (list1[key1p]+1, list2[key2p]+1,Time2)
                            Wflow12[flowkey]+=[tp]
                            WflowCont[flowkey]+=[tp]
                            if list1[key1p]+1 != key1 and list2[key2p]+1 != key2:
                                Wflow2[flowkey]+=[tp]
                                WflowCont2[flowkey] += [tp]
                            elif list1[key1p]+1 == key1:
                                Wflow1D[flowkey]+=[tp]
                                Wflow1[flowkey] += [tp]
                                WflowContO[flowkey] += [tp]
                                WflowContOD[flowkey] += [tp]
                                WflowHybrid[flowkey] += [tp]
                            elif list2[key2p]+1 == key2:
                                Wflow1O[flowkey]+=[tp]
                                Wflow1[flowkey] += [tp]
                                WflowContD[flowkey] += [tp]
                                WflowContOD[flowkey] += [tp]
                                WflowHybrid[flowkey] += [tp]
                            else:
                                Wflow1[flowkey]+=[tp]
                        #elif tp in yKeysMinusOne:
                            #tp = (list1[key1p] + 1, list2[key2p] + 1, Time2)
                            #WflowCont[flowkey]+=[tp]
                for key1p in range(len(list1)):
                    for key2p in range(len(list2)):
                        tp = (list1[key1p] + 1, list2[key2p] + 1)
                        if tp != (key1,key2) and tp in yKeysMinusOne:
                            tp = (list1[key1p] + 1, list2[key2p] + 1, Time1)
                            WflowLaggedDown[flowkey] += [tp]
                            if list1[key1p] + 1 != key1 and list2[key2p] + 1 != key2:
                                WflowLaggedDown2[flowkey] += [tp]
                            elif list1[key1p]+1 == key1:
                                Wflow1D[flowkey]+=[tp]
                                Wflow1[flowkey] += [tp]
                                WflowLaggedDownO[flowkey] += [tp]
                                WflowLaggedDownOD[flowkey] += [tp]
                                WflowHybrid[flowkey] += [tp]
                            elif list2[key2p]+1 == key2:
                                Wflow1O[flowkey]+=[tp]
                                Wflow1[flowkey] += [tp]
                                WflowLaggedDownD[flowkey] += [tp]
                                WflowLaggedDownOD[flowkey] += [tp]
                                WflowHybrid[flowkey] += [tp]
                            else:
                                Wflow1[flowkey]+=[tp]
                        elif tp == (key1,key2):
                            if tp in yKeysMinusOne:
                                WflowCont[flowkey] += [(key1,key2,Time1)]
                                WflowContO[flowkey] += [(key1,key2,Time1)]
                                WflowContD[flowkey] += [(key1, key2, Time1)]
                                WflowContOD[flowkey] += [(key1, key2, Time1)]
                                WflowLaggedDownOD[flowkey] += [(key1, key2, Time1)]
                                WflowHybrid[flowkey] += [(key1, key2, Time1)]
                                WflowCont2[flowkey] += [(key1, key2, Time1)]


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
    elif Level == 3:
        Wflow = WflowCont
    elif Level == 31:
        Wflow = WflowContO
    elif Level == 32:
        Wflow = WflowContD
    elif Level == 33:
        Wflow = WflowContOD
    elif Level == 312:
        Wflow = WflowCont2
    elif Level == 49:
        Wflow = WflowLaggedDown
    elif Level == 491:
        Wflow = WflowLaggedDownO
    elif Level == 492:
        Wflow = WflowLaggedDownD
    elif Level == 494:
        Wflow = WflowLaggedDownOD
    elif Level == 412:
        Wflow = WflowLaggedUp2
    elif Level == 413:
        Wflow = WflowLaggedDown2
    elif Level == 55:
        Wflow = WflowHybrid
    else:
        Wflow = {}
        print 'you must choose a level of flow neighborhood'
    return Wflow
