# encoding: latin2
"""Algorithm utilities
G{packagetree core}
"""
__author__ = "Juan C. Duque"
__credits__ = "Copyright (c) 2009-11 Juan C. Duque"
__license__ = "New BSD License"
__version__ = "1.0.0"
__maintainer__ = "RiSE Group"
__email__ = "contacto@rise-group.org"

import numpy as np
from areacl import AreaCl

def indexMultiple(x,value):
    """
    Return indexes in x with multiple values.
    """
    return [ i[0] for i in enumerate(x) if i[1] == value ]

def calculateGetisG(keyList, dataMean, dataStd, dataDictionary, dataLength):
    """
    This function returns the local G statistic a given region.
    keyList is the list of keys of neighbors
    dataLength is the total number of input data units
    """
    sum = 0
    for i in keyList:
        #sum = sum + np.double(dataDictionary[i])
        #print 'dataDictionary[i]:  ' + str(dataDictionary[i])
        sum = sum + dataDictionary[i]
        #print sum
	neighborNumber = len(keyList)
    #print neighborNumber
    numerator = sum - (dataMean * neighborNumber)
    denominator = dataStd * ((float(dataLength * neighborNumber - (neighborNumber ** 2)) / (dataLength - 1)) ** 0.5)

    #  denominator = (dataStd*((dataLength*neighborNumber-(neighborNumber**2))/(dataLength-1))**0.5)

    G = numerator / denominator
    return G

def calculateMoranI(ikey, keyList, dataMean, dataStd, dataDictionary, dataLength):
    """
    This function returns the local Moran's I statistic a given region.
    keyList is the list of the keys of i's neighbors
    dataLength is the total number of input data units
    """
    sum = 0
    for j in keyList:
        sum = sum + np.double((dataDictionary[j]) - dataMean)
    global neighborNumber
    neighborNumber = len(keyList)

    
##    if ikey == (36,22):
##        print neighborNumber

    numerator = dataLength*(dataDictionary[ikey] - dataMean)*sum
    denominator = dataStd ** 2
    #To row standardize: sum of wij for each i equals 1
    denominator = denominator * neighborNumber
    
    I = (np.double(numerator))/(np.double(denominator))
    #print "numerator: " + str(numerator)
    #print "denominator: " + str(denominator)
    #print I
    return I

def calculateBivaraiteMoranI(ikey, keyList, dataDictionary):
    """
    This function returns the local bivaraite Moran's I statistic a given region.
    keyList is the list of the keys of i's neighbors
    dataLength is the total number of input data units
    dataDictionary has multivariates {key:[v1,v2,...,vk]}
    numVar is the total number of variables
    """
    sum = 0


    #dataDictionary1 = { key:value for key, value in dataDictionary.items() if value[0] > 0 }
    #dataDictionary1 = { key:value for key, value in dataDictionary.items()}
    #Although avoiding zero-value flows, it may have issue dealing with negative flow value
##    dataLength1 = len(dataDictionary1.keys())
##    var1_value = []
##    for i in range(dataLength1):
##        var1_value.append(dataDictionary1.values()[i][0])
##
##    dataSum1 = np.sum(np.double(var1_value))
##    dataMean1 = np.mean(np.double(var1_value))
##    dataStd1 = np.std(np.double(var1_value))
##
##
##    #standardize variable i
##    std_i_value = (dataDictionary1[ikey][0] - dataMean1)/dataStd1
##    
##
    #dataDictionary2 = { key:value for key, value in dataDictionary.items() if value[1] > 0 }
##    dataDictionary2 = { key:value for key, value in dataDictionary.items()}
##    dataLength2 = len(dataDictionary2.keys())
##    var2_value = []
##    for i in range(dataLength2):
##        var2_value.append(dataDictionary2.values()[i][1])
##
##    dataSum2 = np.sum(np.double(var2_value))
##    dataMean2 = np.mean(np.double(var2_value))
##    dataStd2 = np.std(np.double(var2_value))

##    dataSum2 = np.sum(np.double(dataDictionary2.values()[1]))
##    dataMean2 = np.mean(np.double(dataDictionary2.values()[1]))
##    dataStd2 = np.std(np.double(dataDictionary2.values()[1]))
##
##    if ikey == (36,22):
##        #print dataDictionary1[ikey]
##        print keyList

    neighborNumber = len(keyList)
##    if ikey == (2,20):
##        print neighborNumber
##        print keyList

    for j in keyList:
##        print 'j: '+ str(j)
##        neighborNumber = len(keyList)
        #if j in dataDictionary1.keys():
            #standardize variable j
##            std_j_value = (dataDictionary2[j][1] - dataMean2)/dataStd2
            #for the simplest case, bivaray wij, works as:
##            sum = sum + std_j_value
##            if ikey == (36,22):
##                print dataDictionary1[j][1]
        sum = sum + dataDictionary[j][1]
            #for non-binary wij, work as:
            #sum = sum + std_j_value * wij
            
##    if ikey == (36,22):
##        print sum
    #To row standardize: sum of wij for each i equals 1
    if neighborNumber!=0:
        sum = sum/neighborNumber
    bi = sum * dataDictionary[ikey][0]
    #BI = round(bi,2)
    BI = bi
##    print BI
    
    return BI

def calculateGearyC(ikey, keyList, dataDictionary):
    """
    This function returns the local Geary's c statistic a given region.
    keyList is the list of the keys of i's neighbors
    dataLength is the total number of input data units
    """
    sum = 0
    for j in keyList:
        sum = sum + np.double((dataDictionary[ikey]- dataDictionary[j])**2)
	neighborNumber = len(keyList)
    #numerator = dataLength* (dataDictionary[i] - dataMean)*sum
    #denominator = dataStd ** 2

    C = sum
    return C

def calculateMultiGearyC(ikey, keyList,dataDictionary,dataDictionaryPer, numVar):
    """
    This function returns the local Geary's c statistic a given region.
    keyList is the list of the keys of i's neighbors
    dataLength is the total number of input data units
    dataDictionary has multivariates {key:[v1,v2,...,vk]}
    numVar is the total number of variables
    """
    sum = 0
    for i in range(numVar):
        sum_var = 0
        dataSum = np.sum(np.double(dataDictionaryPer.values()[i]))
        dataMean = np.mean(np.double(dataDictionaryPer.values()[i]))
        dataStd = np.std(np.double(dataDictionaryPer.values()[i]))
        #print 'data mean is: ' + str(dataMean)
        if len(keyList) ==0:
            sum =0
        else:
            for j in keyList:
                std_i_value = (dataDictionary[ikey][i] - dataMean)/dataStd
                #print 'std_i_value: ' + str(std_i_value)
                #print 'dataDictionary[ikey][i] ' + str(dataDictionary[ikey][i])
                #print keyList
                #print 'dataDictionary[j][i] ' + str(dataDictionary[j][i])
                std_j_value = (dataDictionaryPer[j][i] - dataMean)/dataStd
                #print 'std_j_value: ' + str(std_j_value)
                sum_var = sum_var + np.double((std_i_value- std_j_value)**2)
            sum = sum + sum_var
    #numerator = dataLength* (dataDictionary[i] - dataMean)*sum
    #denominator = dataStd ** 2

    MC = sum/numVar
    return MC

def quickSortIntersection(dataList, keyList, discardList):
    """
    quickSortIntersection recursively sorts the list of values usinga
    quick sort algorithm.
    """
    if len(keyList) <= 1:
        return keyList
    else:
        lessData = []
        lessKey = []
        moreData = []
        moreKey = []
        pivot = dataList[-1]
        kpivot = keyList[-1]
        for i in range(len(dataList) - 1):
            if keyList[i] not in discardList:
                if dataList[i] <= pivot:
                    lessData.append(dataList[i])
                    lessKey.append(keyList[i])
                else:
                    moreData.append(dataList[i])
                    moreKey.append(keyList[i])
        return quickSortIntersection(lessData, lessKey, discardList) + [kpivot] + quickSortIntersection(moreData, moreKey, discardList)

def quickSort2(keys, y):
    """
    quickSortIntersection recursively sorts the list of values using a
    quick sort algorithm.
    """
    if len(keys) <= 1:
        return keys
    else:
        lessData = []
        lessKey = []
        moreData = []
        moreKey = []
        pivot = y[keys[-1]]
        kpivot = keys[-1]
        keys=keys[0: -1]
        for i in keys:
            if y[i] <= pivot:
                lessKey.append(i)
            else:
                moreKey.append(i)
        return quickSort2(lessKey, y) + [kpivot] + quickSort2(moreKey, y)

def neighborSort(dictionary, discardList):
    """
    Returns the list of keys of a dictionary sorted by the
    values that are assigned by them.
    """
    dataList = dictionary.values()
    keyList = dictionary.keys()
    return quickSortIntersection(dataList, keyList, discardList)

def vectorDistance(v1, v2):
    """
    this function calculates de euclidean distance between two
    vectors.
    """
    sum = 0
    for i in range(len(v1)):
        sum += (v1[i] - v2[i]) ** 2
    return sum ** 0.5

#  INTERNOS

def calculateCentroid(areaList):
    """
    This function return the centroid of an area list
    """
    pg = 0.0
    pk = []
    centroid = AreaCl(0, [], [])
    for area in areaList:
        pg += area.data[0]
        pk = pk + [area.data[0]]
    pkPg = np.matrix(pk).T / pg
    data = [0.0] * len(area.data)
    var = np.matrix(areaList[0].var) * 0.0
    j = 0
    for area in areaList:
        var += area.var * pow(pkPg[j, 0], 2)
        for i in range(len(area.data)):
            data[i] += area.data[i] * pkPg[j, 0]
        j += 1
    centroid.data = data
    centroid.var = var
    return centroid


def factorial(n):
    """
    Returns the factorial of a number.
    """
    fact = 1.0
    if n > 1:
        fact = n * factorial(n - 1)
    return fact

def comb(n, m):
    """
    This function calculates the number of possible combinations of n items
    chosen by m.
    """
    return factorial(n) / (factorial(m) * factorial(n - m))

def recode(X):
    """
    Tranform a list with regions begining in x to a lis begining in 0.
    """
    XP = X + []
    i = 0
    lenX = len(X)
    r = 0

    assigned = {}

    for i in xrange(lenX):
        if X[i] not in assigned:
            assigned[X[i]] = r
            r += 1

    for i in xrange(lenX):
        XP[i] = assigned[XP[i]]

    return XP

def sortedKeys(d):
    """
    Return keys of the dictionary d sorted based on their values.
    """
    values = d.values()
    sortedIndices = np.argsort(values)
    sortedKeys = [d.keys()[i] for i in sortedIndices]
    minVal = min(values)
    countMin = values.count(minVal)
    if countMin > 1:
        minIndices = sortedKeys[0: countMin]
        nInd = len(minIndices)
        idx = range(nInd)
        np.random.shuffle(idx)
        permMins = idx
        c = 0
        for i in range(nInd):
            place = permMins[c]
            sortedKeys[c] = minIndices[place]
            c += 1
    return sortedKeys

def feasibleRegion(feasDict):
    """
    Return if a list of areas are connected
    """
    areas2Eval = []
    areas = {}
    for key in feasDict.keys():
        try:
            neighbours = feasDict[key]
        except:
            neighbours = {}
        a = AreaCl(key, neighbours, [])
        areas[key] = a
        areas2Eval = areas2Eval + [key]
    feasible = 1
    newRegion = set([])
    for area in areas2Eval:
        newRegion = newRegion | (set(areas[area].neighs) & set(areas2Eval))
    if set(areas2Eval) - newRegion != set([]):
        feasible = 0
    return feasible

def randomOD(flow, ctrl):
    #Flow = open('Flow.txt', 'r')
    #Flow = open('Chendu/RegionLinkMatrix20160123.txt', 'r')
    #Flowstr = Flow.read()
    #FlowNoneZero = eval(Flowstr)
    FlowNoneZero = flow
    FlowKey = FlowNoneZero.keys()
    FlowValue = FlowNoneZero.values()

    Ctrl = ctrl
    #print FlowKey
    #print FlowValue
    FlowLen = len(FlowValue)
    ODlist = []
    Olist = []
    Dlist = []
    Ocount = {}
    Dcount = {}
    Osum = {}
    Dsum = {}
    OlistofD = {}
    DlistofO = {}
    randFlowCtrlO = {}
    randFlowCtrlD = {}
    randFlowCtrlOKeyList = []
    randFlowCtrlDKeyList = []

    for i in range(FlowLen):
        ODlist.append( FlowKey[i])
        O = ODlist[i][0]
        D = ODlist[i][1]
        #print O
        #print D
        Olist.append(O)
        Dlist.append(D)
        #initialization
        Ocount[O] = 0
        Dcount[D] = 0
        Osum[O] = 0
        Dsum[D] = 0
        OlistofD[O] = []
        DlistofO[D] = []

    for i in range(FlowLen):
        O = ODlist[i][0]
        D = ODlist[i][1]
        #stats of total amount and value
        Ocount[O] = Ocount[O]+1
        Dcount[D] = Dcount[D]+1
        Osum[O] = Osum[O] + FlowValue[i]
        Dsum[D] = Dsum[D] + FlowValue[i]
        OlistofD[O].append(D)
        DlistofO[D].append(O)
    #print OlistofD


    #print Ocount
    #print Dcount
    #print Dsum

    #control total flow out of every O, or into every D the same
    for i in range(FlowLen):
        O = ODlist[i][0]
        D = ODlist[i][1]
        #OD = FlowKey[i]
        randlist = []
        randlist = np.random.permutation(Ocount[O])
        randlist2 = []
        randlist2 = np.random.permutation(Dcount[D])
        #print randlist
        if Ctrl == 0: #control flow out of every O the same
            for randD in randlist:
                #print randD
                randDid = OlistofD[O][randD]

                #print str(O)+ ': '+ str(randDid)
                
                ##switch flow value
                randFlowValue = FlowNoneZero[(O,randDid)]
                randFlowCtrlO[(O,D)] = randFlowValue
                #print randFlow
            randFlow = randFlowCtrlO
            #if only switching ID (keys)
            #randFlowCtrlOKeyList.append((O,randDid))
            #Ocount[O] = Ocount[O] - 1
        else:
            for randO in randlist2:
                #print randD
                randOid = DlistofO[D][randO]
                #print str(O)+ ': '+ str(randDid)
                randFlowValue = FlowNoneZero[(randOid,D)]
                randFlowCtrlD[(O,D)] = randFlowValue
                #print randFlow
            randFlow = randFlowCtrlD
    return randFlow
