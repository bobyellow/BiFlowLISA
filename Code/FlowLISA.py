# Script metadata for reference and credits
__author__ = "Ran Tao"
__credits__ = "Copyright (c) 2018-01 Ran Tao"
__license__ = "New BSD License"
__version__ = "1.0.0"
__maintainer__ = "RiSE Group"
__email__ = "contacto@rise-group.org"

import time as tm
import numpy as np
from componentsAlg import (calculateGetisG, calculateGearyC, 
                           calculateMultiGearyC, calculateMoranI)
from contiguity import weightsFromFlows

__all__ = ['execFLOWLISA']

def execFLOWLISA(AREAS1, AREAS2, FlowValue, Spatstat, NeiLvl):
    """
    Execute FlowLISA method based on the provided spatial statistic type (Spatstat).

    Parameters:
    - AREAS1: List of Origin areas.
    - AREAS2: List of Destination areas.
    - FlowValue: OD pairs with non-zero value.
    - Spatstat: Specifies the type of spatial statistic to be used.
    - NeiLvl: Neighbor Level for weights computation.

    Returns:
    - String: Results including Moran's I or Geary's C values, p-values, and other relevant information.
    """

    # Initialization: Start measuring time for performance benchmarks
    start = tm.time()
    
    # Print out the program's banner
    print("Running FlowLISA by Ran Tao, built on clusterpy by Duque et al.")

    # Initializing main data structures from input arguments
    areas1 = AREAS1 
    areas2 = AREAS2 
    flowvalue = FlowValue

    # Extracting Y values from areas
    y1 = areas1.Y 
    y2 = areas2.Y

    # Depending on the Spatstat value, format the flow values accordingly
    yOutput = {k: [v] if Spatstat != 5 else v for k, v in y.items()}
    yKeys = list(y.keys())

    # Calculating weights (Wflow) which represent the flow between areas
    neighborLevel = NeiLvl
    Wflow = weightsFromFlows(areas1, areas2, y, neighborLevel)
    print(f"Finished calculating Wflow. Length: {len(Wflow)}")

    # Compute global statistics that will be used for the local calculations
    dataSum = np.sum(list(y.values()))
    dataMean = np.mean(list(y.values()))
    dataStd = np.std(list(y.values()))

    # The GMoranI will store the overall Moran's I value
    GMoranI = 0

    # Calculate spatial statistics for each flow
    for s in yKeys:
        neighbors = Wflow.get(s, [])

        # For univariate data, calculate Local Moran's I
        if Spatstat == 1 and neighbors:
            MoranI = calculateMoranI(s, neighbors, dataMean, dataStd, y, len(yKeys))
            yOutput[s].extend([MoranI, 0])
            GMoranI += MoranI
        # GeisG Calculate
        if Spatstat == 2:
            GetisG = calculateGetisG(neighbors, dataMean, dataStd, y, len(yKeys)) if neighbors else 0
            yOutput[s].extend([GetisG, 0])
        # Geary C Calculate
        if Spatstat == 3:
            GearyC = calculateGearyC(s,neighbors, y) if neighbors else 0
            yOutput[s].extend([GearyC, 0])
        # For multivariate data, calculate Multivariate Geary's C
        elif Spatstat == 5:
            MC = 999 if not neighbors else calculateMultiGearyC(s, neighbors, y, y, 2)
            yOutput[s].extend([MC, 0])

    # For significance testing, conduct a Monte-Carlo simulation
    GMoranI_sim = [0] * 1000
    for i in range(1000):
        # Create a randomized version of the flow data
        yRandom = {rk: y[ok] for rk, ok in zip(np.random.permutation(yKeys), yKeys)}

        # Recalculate spatial statistics based on the randomized data
        for pk in yRandom:
            neighbors = Wflow.get(pk, [])
            if Spatstat == 1 and neighbors:
                MoranI = calculateMoranI(pk, neighbors, dataMean, dataStd, yRandom, len(yKeys))
                GMoranI_sim[i] += MoranI
                if abs(MoranI) > abs(yOutput[pk][1]):
                    yOutput[pk][2] += 1
            elif Spatstat == 5:
                MC = calculateMultiGearyC(pk, neighbors, y, yRandom, 2)
                if MC > yOutput[pk][2]:
                    yOutput[pk][3] += 1

    # Analyze the results of the Monte-Carlo simulation
    GMoranI_sim.sort()
    GMoranI_str = f"Global Moran's I value is: {GMoranI}. It is {'positive' if GMoranI >= 0 else 'negative'}, but "
    GMoranI_str += "insignificant at 0.01 level"
    if GMoranI >= 0 and GMoranI >= GMoranI_sim[950] or GMoranI <= 0 and GMoranI <= GMoranI_sim[49]:
        GMoranI_str = GMoranI_str.replace("insignificant", "significantly")

    # Construct the final output, formatted based on spatial statistic type and significance
    output_str_list = []
    if Spatstat == 1:
        output_str_list.append(GMoranI_str)
        output_str_list.append('O, D, V, MoranI, p-value, I_Result')
        for k, v in yOutput.items():
            v[2] /= 1000.0
            significance = "NS"
            if v[1] != 0 or v[2] != 0:
                if v[2] <= 0.05:
                    if v[1] > 0:
                        significance = "HH" if v[0] > dataMean else "LL"
                    else:
                        significance = "HL" if v[0] > dataMean else "LH"
            output_str_list.append(f"{k}, {', '.join(map(str, v))}, {significance}")
    elif Spatstat == 5:
        output_str_list.append('O, D, V1, V2, MC, p-value')
        for k, v in yOutput.items():
            v[3] /= 1000.0
            output_str_list.append(f"{k}, {', '.join(map(str, v))}")

    return '\n'.join(output_str_list)
