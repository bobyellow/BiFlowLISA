# BiFlowLISA
Bivariate local Moran's I for spatial flow data

Tao, R., & Thill, J. C. (2020). BiFlowLISA: Measuring spatial association for bivariate flow data. Computers, Environment and Urban Systems, 83, 101519.
Before running the code, there are several steps you need to prepare. 

First, import the origin and destination shapefile.

AREAS1 = clusterpy.importArcData("yourpath/Origin_shapefile")
AREAS2 = clusterpy.importArcData("yourpath/Destination_shapefile")

Second, this is the execute code for FlowLISA
execBIFLOWLISA(AREAS1, AREAS2, FlowValue, NeiLvl)
    Parameters:
    - AREAS1: List of Origin areas.
    - AREAS2: List of Destination areas.
    - FlowValue: OD pairs with non-zero value.
    - NeiLvl: Neighbor Level for weights computation. level 1 has O (D) the same, while D (O) is neighbor; level 2 has both O and D as neighbor; level 12 = level 1 + level 2

Third, we adopt Monte Carlo simulation based on conditional permutations to evaluate the statistical significance. The default number is 1000.

Finally, after execute the code, export the results to the path you want to save.
outputFile = open('yourpath/file_name.txt','w')
outputFile.write(outputStr)
