__author__ = "Ran Tao"
__credits__ = "Copyright (c) 2018-01 Ran Tao"
__license__ = "New BSD License"
__version__ = "1.0.0"
__maintainer__ = "RiSE Group"
__email__ = "contacto@rise-group.org"

import time as tm
import numpy as np
import clusterpy
import operator
import csv
import math
import pdb
from scipy import stats
from componentsAlg import calculateGetisG,calculateMoranI,calculateBivaraiteMoranI,calculateGearyC,calculateMultiGearyC,quickSort2,neighborSort,randomOD 
from contiguity import weightsFromFlows 
__all__ = ['execAMOEBA']

def execBIFLOWLISA(AREAS1, AREAS2,FlowValue,NeiLvl):
    start = tm.time()
    
    print "01182024; Running BiFlowLISA by Ran Tao, built on clusterpy by Duque et al."

    areas1 = AREAS1 #list of O area
    areas2 = AREAS2 #list of D area
    flowvalue = FlowValue ##OD pairs with non-zero value
    y1 = areas1.Y #Read OD features
    y2 = areas2.Y

    #Read flow data
    y = flowvalue #y is a dictionary of input polygons: key+values
    yOutput = flowvalue

    #Get the flow dictionary keys, i.e. (O,D) tuple
    yKeys = y.keys()
    yValues= y.values()

    #Obtain flow neighbors based on O&D contiguity, by default Rook's case
    #Wflow is a dictionary, for each item (flow), the key is its (O,D) tuple, the value includes all the (O,D) tuples of its neighbor flows
    neighborLevel = NeiLvl
    Wflow = weightsFromFlows(areas1, areas2, y, neighborLevel)
    #the last parameter decides the level of flow neighbors.
    #level 1 has O (D) the same, while D (O) is neighbor; level 2 has both O and D as neighbor; level 12 = level 1 + level 2
    ## need to add level 0

    #wValues = Wflow.values()
    print 'finish calculating Wflow'

    ### select a subset of y, to calculate BiLISA only when type-a flow is non-zero
    #y1 = { key:value for key, value in y.items() if value[0] > 0 } #Need to think of a way to deal with null OD pair
    y1 = { key:value for key, value in y.items() if value[0] != 0 }
    y1=y
    #print y1
    #print len(y1)
    y1Keys = y.keys()
    y1Values= y.values()

    #y2 = { key:value for key, value in y.items() if value[1] != 0 }
    y2=y
    #print y2
    #print len(y2)
    y2Keys = y.keys()
    y2Values= y.values()


    # add head/tail break filter here y1_head = ...
    
    dataLength = len(y) ## be careful if two variables have different length
    dataLength1 = len(y1)
    dataLength2 = len(y2)

    #dataRange = range(dataLength)
    #dataRange1 = range(dataLength1)
    dataRange2 = range(dataLength2)


    # get mean value of variable i for later judging HH, HL, LH, LL
    #dataDictionary1 = { key:value for key, value in y.items() if value[0] > 0 } # no need to require positive-value flow only
    #dataDictionary1 = { key:value for key, value in y.items()}

    sum1 = 0
    for i in range(dataLength1):
        #print 'calculating sum now: ' +str(i)
        sum1 = sum1 + y.values()[i][0]
        
    #dataMean1 = np.mean(np.double(dataDictionary1.values()[0])) #wrong way to calcualte the mean

    dataMean1 = np.double(sum1/dataLength1)
    print 'mean1:'+str(dataMean1)
    
    
    GBI = 0 #initiate global Bivariate Flow Moran's I
    #the denominator of global BI is ignored here, since it doesn't affect result. It only standardizes GBI.

    for s in yKeys:
        #if s in Wflow: #w = Wflow, dictionary of flow's neighbors
        BI = 0
        #print 'yKeys is ' + str(s) + ' now'
        neighbors = Wflow[s] #Get the list of neighbors of flow s
        BI = BI + calculateBivaraiteMoranI(s, neighbors,y1)

        #print s
        #print BI
        yOutput[s].append(BI) #append original MC value to the data dicitonary
        yOutput[s].append(0) #original P value as 1

        GBI = GBI + BI
        #outputStr = outputStr +'\n' + str(MC)
        #print str(I)
        #outputStrList.append(I)
        #print yOutput

    print 'GBI: ' + str(GBI)
    #Monte-Carlo with conditional permutation: fix type-a flow's value, while permutating type-b
    
    #pValue = []
    #for i in range(dataLength):
        #pValue[i]= 1

    var1_value = []
    var1_value1 = []#when var1 != zero
    var2_value = []
    var2_value1 = []#when var1 != zero
    var2_value2 = []#when var2 != zero

    for i in range(dataLength2):
        var2_value2.append(y2Values[i][1])
        var1_value1.append(y1Values[i][0])
        var2_value1.append(y1Values[i][1])
        var1_value.append(yValues[i][0])
        var2_value.append(yValues[i][1])
    #print var2_value
    Pearson = stats.pearsonr(var1_value, var2_value)
    Pearson1 = stats.pearsonr(var1_value1, var2_value1) #when var1 != zero
    print 'Pearson: '+ str(Pearson)
    print 'Pearson1: '+ str(Pearson1)
    print 'start 1000-time permutation'

    GBI_sim = [None] * 1000
    randlist = []
    for i in range(1000):

        randomList = np.random.permutation(dataRange2)##reshuffle Flow ID, keep total number the same

        var2_value_random = []
        yRandom = {}
        for j in range(dataLength2):
           randKey1 = randomList[j]
           randVar2 = var2_value2[randKey1]
           var2_value_random.append(randVar2)
           randKey = yKeys[j]
           randV1 = yValues[j][0]
           randV2 = var2_value_random[j]
           yRandom[randKey] = [randV1,randV2]
        randlist.append(yRandom)
    print "finish create randlist"


    for i in range(1000):
        GBI_sim[i] = 0
        yRandom = randlist[i]
        for s in yRandom.keys():
            randomNeighbors = Wflow[s]
            BI = calculateBivaraiteMoranI(s, randomNeighbors,yRandom)
            if (yOutput[s][2] >= 0) and (BI > yOutput[s][2]):
                yOutput[s][3] = yOutput[s][3] + 1
            if (yOutput[s][2] < 0) and (BI < yOutput[s][2]):
                yOutput[s][3] = yOutput[s][3] + 1

            GBI_sim[i] = GBI_sim[i]+BI

        print GBI_sim[i]
        

    GBI_sim.sort()
    #print GBI_sim
    GBI_str = "Global BiFI value is: " + str(GBI)
    if GBI >= 0:
        if GBI >= GBI_sim[950]:
            GBI_str = GBI_str +'. It is significantly positive at 0.01 level'
        else:
            GBI_str = GBI_str +'. It is positive but insignificant at 0.01 level'
    else:
        if GBI <= GBI_sim[49]:
            GBI_str = GBI_str +'. It is significantly nevative at 0.01 level'
        else:
            GBI_str = GBI_str +'. It is nevative but insignificant at 0.01 level'

    print GBI_str
    #yOutput1 = { key:value for key, value in yOutput.items() if value[0] > 0 } #no need to require positive value flow only
    yOutput1 = { key:value for key, value in yOutput.items()}

    #outputStr = GBI_str + '\n' +'O, D, V1, V2, BI, p-value, BI_Result'
    outputStr = 'O, D, V1, V2, BI, p-value, BI_Result'
    #print yOutput
    Okeys = yOutput1.keys()
    Ovalue = yOutput1.values()
    for i in range(dataLength1):
        Ovalue[i][3] = Ovalue[i][3]/1000.000
        outputStr = outputStr +'\n' + str(Okeys[i])+', ' + str(Ovalue[i])
        
        if  Ovalue[i][3] == 0 and Ovalue[i][2] == 0:
            outputStr = outputStr + ', NS' # No BI value; probably no non-zero flow neighbors
        elif Ovalue[i][3] <= 0.01:
            if Ovalue[i][2] > 0:
                if Ovalue[i][0] > dataMean1:
                    outputStr = outputStr + ', HH'
                    #print 'HH: xi: '+ str(Ovalue[i][0]) +' mean: '+ str(dataMean1)
                else:
                    outputStr = outputStr + ', LL'
            else:
                if Ovalue[i][0] > dataMean1:
                    outputStr = outputStr + ', HL'
                else:
                    outputStr = outputStr + ', LH'
        else:
            outputStr = outputStr + ', NS' # NS means not significant
        


    outputStr1 = outputStr.replace('(','')
    outputStr2 = outputStr1.replace(')','')
    outputStr3 = outputStr2.replace('[','')
    outputStr4 = outputStr3.replace(']','')
    endtime = tm.time()
    elapsed_time = endtime - start
    print('Execution time:', elapsed_time, 'seconds')
    return outputStr4
