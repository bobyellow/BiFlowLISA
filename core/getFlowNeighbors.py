import struct
import numpy as np  
from os import path
from core.getNeighbors import getNeighborsAreaContiguity

def getFlowNeighborsContiguity(AREAS1, AREAS2, FlowValue, Level):
    """
    Obtain flow neighbors using spatial contiguity.
    """
    # Compute neighbors within function
    Wqueen, Wrook = getNeighborsAreaContiguity(AREAS1)  # For origin areas
    _, Wrook2 = getNeighborsAreaContiguity(AREAS2)  # For destination areas
    
    Grid1Wrook = Wrook  # Assign Rook's contiguity to Grid1
    Grid2Wrook = Wrook2  # Assign Rook's contiguity to Grid2
    
    Wflow = {}  # Output dictionary
    Wflow1 = {}
    Wflow1O = {}
    Wflow1D = {}
    Wflow2 = {}
    Wflow12 = {}

    print('Obtain O & D neighbors by contiguity (Rook or Queen)') 
    KEY1 = list(Grid1Wrook.keys())  
    KEY2 = list(Grid2Wrook.keys())  
    yKeys = list(FlowValue.keys())  

    for key1Zero in range(len(KEY1)):
        for key2Zero in range(len(KEY2)):
            key1 = key1Zero + 1
            key2 = key2Zero + 1
            if (key1, key2) in yKeys:
                flowkey = (key1, key2)
                Wflow1[flowkey] = []
                Wflow1O[flowkey] = []
                Wflow1D[flowkey] = []
                Wflow2[flowkey] = []
                Wflow12[flowkey] = []
                Grid1Wrook[key1Zero].append(key1Zero)
                key1s = Grid1Wrook[key1Zero]
                Grid2Wrook[key2Zero].append(key2Zero)
                key2s = Grid2Wrook[key2Zero]
                set1 = set(Grid1Wrook[key1Zero])
                set2 = set(Grid2Wrook[key2Zero])
                list1 = list(set1)
                list2 = list(set2)
                for key1p in range(len(list1)):
                    for key2p in range(len(list2)):
                        tp = (list1[key1p] + 1, list2[key2p] + 1)
                        if tp != (key1, key2) and tp in yKeys:
                            Wflow12[flowkey] += [tp]
                            if list1[key1p] + 1 != key1 and list2[key2p] + 1 != key2:
                                Wflow2[flowkey] += [tp]
                            elif list1[key1p] + 1 == key1:
                                Wflow1D[flowkey] += [tp]
                            elif list2[key2p] + 1 == key2:
                                Wflow1O[flowkey] += [tp]
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
        print('You must choose a level of flow neighborhood')
        # Level=1: one of OD is the same and the other is neighbor;
        # Level=2: both OD are neighbors, so level ==12 means a combination of the two above
        # 18 means same D, Os are neighbors
        # 19 means same O, Ds are neighbors
        # adding 0 means including the situation of flows sharing the same O & D as flow i
      
    return Wflow
