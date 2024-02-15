from __future__ import division
import clusterpy
import numpy as np
import shapefile
import pandas as pd

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


    numerator = (dataDictionary[ikey] - dataMean) * sum #why here multipy dataLength
    denominator = dataStd ** 2
    # To row standardize: sum of wij for each i equals 1
    denominator = denominator * neighborNumber

    I = (np.double(numerator)) / (np.double(denominator))

    return I

def calculateEqualWeightMoranI(ikey, keyList, dataMean, dataStd, dataDictionary, dataLength,time):
    """
    This function returns the local Moran's I statistic a given region.
    keyList is the list of the keys of i's neighbors
    dataLength is the total number of input data units
    """
    sum = 0
    count = 0
    count1 = 0
    for x in keyList:
        if x[2] == time:
            count = count + 1
        else:
            count1 = count1 + 1

    if count == 0:
        wt_spatial = 0
    else:
        wt_spatial = 1/count
    if count1 == 0:
        wt_temporal = 0
    else:
        wt_temporal = 1/count1

    for j in keyList:
        if j[2] == time:
            sum = sum +np.double(wt_spatial*((dataDictionary[j]) - dataMean))
        else:
            sum = sum + np.double(wt_temporal*((dataDictionary[j]) - dataMean))
        #global neighborNumber
        #neighborNumber = len(keyList)


    numerator = (dataDictionary[ikey] - dataMean) * sum #why here multipy dataLength
    denominator = dataStd ** 2
    # To row standardize: sum of wij for each i equals 1
    #denominator = denominator * neighborNumber

    I = (np.double(numerator)) / (np.double(denominator))

    return I
