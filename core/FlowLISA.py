import numpy as np
import random
from core.getFlowNeighbors import getFlowNeighborsContiguity  # Obtain neighbors of flow data
from core.spatstats import (
    calculateMoranI, 
    calculateGetisG, 
    calculateGearyC, 
    calculateMultiGearyC,
    calculateBivariateT,
    calculateBivariteMoranI,
    calculateLocalL
)

# Define the bivariate flow LISA
def execBIFLOWLISA(AREAS1, AREAS2, FlowValue, NeiLvl):
    """
    Parameters:
    1. AREAS1: Origin areas (list of polygons)
    2. AREAS2: Destination areas (list of polygons)
    3. FlowValue: Dictionary of (O, D) flow values (each value is [v1, v2])
    4. NeiLvl: Neighborhood level for flow connections

    Returns:
    - A formatted output string containing results
    """
    # Obtain flow neighbors based on O&D contiguity (default: Rook's case)
    y = FlowValue  # Dictionary with flow values
    Wflow = getFlowNeighborsContiguity(AREAS1, AREAS2, y, NeiLvl)
    print("Finished calculating Wflow")

    # Initialize result dictionary: [v1, v2, BI, p_count]
    yOutput = {key: list(values) + [None, 0] for key, values in y.items()}

    # Select flows where v1 > 0
    y1 = {k: v for k, v in y.items() if v[0] > 0}
    y1_keys = list(y1.keys())

    # Mean of v1 over non-zero flows
    v1_values = [v[0] for v in y1.values()]
    data_mean1 = np.mean(v1_values)

    # Compute local Bivariate Moran's I and accumulate global
    GBI = 0.0
    for s in y1_keys:
        neighbors = Wflow.get(s, [])
        BI = calculateBivariteMoranI(s, neighbors, y)
        yOutput[s][2] = BI
        yOutput[s][3] = 0
        GBI += BI

    # Monte Carlo permutation
    print("Start Monte Carlo permutation")
    GBI_sim = []
    y_keys = list(y.keys())
    for _ in range(1000):
        # Shuffle using pure-Python to keep keys as tuples
        permuted = random.sample(y_keys, len(y_keys))

        # Build the conditional permuted dictionary
        y_random = {
            orig: [y[orig][0], y[rnd][1]]
            for orig, rnd in zip(y_keys, permuted)
        }

        sim_sum = 0.0
        for s in y1_keys:
            BIp = calculateBivariteMoranI(s, Wflow.get(s, []), y_random)
            obs = yOutput[s][2]
            if (obs >= 0 and BIp > obs) or (obs < 0 and BIp < obs):
                yOutput[s][3] += 1
            sim_sum += BIp

        GBI_sim.append(sim_sum)

    # Determine global significance
    GBI_sim.sort()
    GBI_str = f"Global BiFlowLISA value is: {GBI:.4f}"
    if GBI >= 0:
        if GBI >= GBI_sim[950]:
            GBI_str += ". It is significantly positive at 0.05 level"
        else:
            GBI_str += ". It is positive but insignificant at 0.05 level"
    else:
        if GBI <= GBI_sim[49]:
            GBI_str += ". It is significantly negative at 0.05 level"
        else:
            GBI_str += ". It is negative but insignificant at 0.05 level"

    print(GBI_str)

    # Build output string
    lines = [GBI_str, "O, D, V1, V2, BI, p-value, pattern"]
    for key in y1_keys:
        vals = yOutput[key]
        pval = vals[3] / 1000.0
        # determine pattern
        if pval == 0 and vals[2] == 0:
            pattern = "NS"
        elif pval < 0.05:
            if vals[2] > 0:
                pattern = "HH" if vals[0] > data_mean1 else "LL"
            else:
                pattern = "HL" if vals[0] > data_mean1 else "LH"
        else:
            pattern = "NS"
        #lines.append(f"{key}, {vals}, {pattern}")
        lines.append(f"{key[0]}, {key[1]}, {vals[0]}, {vals[1]}, {vals[2]}, {pval}, {pattern}")

    return "\n".join(lines)



# Define the univariate flow LISA of which users can select the foundational spatial stat

def execFLOWLISA(AREAS1, AREAS2, FlowValue, Spatstat, NeiLvl):
    """
    Execute FlowLISA to analyze spatial autocorrelation in univariate flow data.

    Parameters:
    1. AREAS1: Origin areas (list of polygons)
    2. AREAS2: Destination areas (list of polygons)
    3. FlowValue: Dictionary of (O, D) flow values
    4. Spatstat:
        1 -> Local Moran's I
        2 -> Local Getis-Ord G
        3 -> Local Geary's C
    5. NeiLvl: Neighborhood level for flow connections

    Returns:
    - A formatted output string containing results
    """
    
    areas1, areas2 = AREAS1, AREAS2  # Assign origin and destination areas
    y = FlowValue  # Dictionary containing flow values
    yKeys, yValues = list(y.keys()), list(y.values())

    # Initialize output dictionary with original values
    yOutput = {k: [v] if Spatstat != 5 else v for k, v in y.items()}

    # Obtain flow neighbors based on O&D contiguity (default: Rook's case)
    Wflow = getFlowNeighborsContiguity(areas1, areas2, y, NeiLvl)

    # Compute global statistics for local calculations
    dataSum, dataMean, dataStd = np.sum(yValues), np.mean(yValues), np.std(yValues)
    GMoranI = 0  # Global Moran's I initialization

    # Calculate spatial statistics for each flow
    for s in yKeys:
        neighbors = Wflow.get(s, [])
        
        if Spatstat == 1 and neighbors:
            MoranI = calculateMoranI(s, neighbors, dataMean, dataStd, y, len(yKeys))
            #print(MoranI)
            yOutput[s].extend([MoranI, 0])  # Moran's I and initial p-value
            GMoranI += MoranI
        elif Spatstat == 2:
            GetisG = calculateGetisG(neighbors, dataMean, dataStd, y, len(yKeys)) if neighbors else 0
            #print(GetisG)
            yOutput[s].extend([GetisG, 0])
        elif Spatstat == 3:
            GearyC = calculateGearyC(s, neighbors, y) if neighbors else 0
            yOutput[s].extend([GearyC, 0])


    # Monte-Carlo significance testing (1000 simulations)
    print("Start Monte Carlo permutation")
    GMoranI_sim = np.zeros(1000)

    for i in range(1000):
        # Ensure randomized keys are tuples
        shuffled_keys = [tuple(key) for key in np.random.permutation(yKeys)]  # Convert to list of tuples

        # Create randomized dictionary
        yRandom = {rk: y[tuple(ok)] for rk, ok in zip(shuffled_keys, yKeys)}
        
        for pk in yRandom:
            neighbors = Wflow.get(pk, [])
            if Spatstat == 1 and neighbors:
                MoranI = calculateMoranI(pk, neighbors, dataMean, dataStd, yRandom, len(yKeys))
                GMoranI_sim[i] += MoranI
                if abs(MoranI) > abs(yOutput[pk][1]):
                    yOutput[pk][2] += 1
            elif Spatstat == 2 and neighbors:
                GetisG = calculateGetisG(neighbors, dataMean, dataStd, yRandom, len(yKeys))
                if GetisG > yOutput[pk][1]:
                    yOutput[pk][2] += 1
            elif Spatstat == 3 and neighbors:
                GearyC = calculateGearyC(pk, neighbors, yRandom) 
                if GearyC > yOutput[pk][1]:
                    yOutput[pk][2] += 1


    # Analyze Monte-Carlo simulation results
    GMoranI_sim.sort()
    significance_msg = (
        f"Global Moran's I value is: {GMoranI:.4f}. It is "
        f"{'positive' if GMoranI >= 0 else 'negative'}, "
        f"{'significantly' if GMoranI >= GMoranI_sim[950] or GMoranI <= GMoranI_sim[49] else 'insignificantly'} at 0.05 level."
    )

    # Construct output strings based on Spatstat type
    output_str_list = []
    if Spatstat == 1:
        output_str_list.append(significance_msg)
        output_str_list.append('O, D, V, MoranI, p-value, pattern')
        for k, v in yOutput.items():
            v[2] /= 1000.0
            significance = "NS"
            if v[1] != 0 or v[2] != 0:
                if v[2] <= 0.05:
                    significance = "HH" if v[0] > dataMean else "LL" if v[1] > 0 else "HL" if v[0] > dataMean else "LH"
            output_str_list.append(f"{k[0]}, {k[1]}, {', '.join(map(str, v))}, {significance}")
    
    if Spatstat == 2:
        output_str_list.append('O, D, V, GetisG, p-value, pattern')
        for k, v in yOutput.items():
            v[2] /= 1000.0
            significance = "NS"
            if v[1] != 0 or v[2] != 0:
                if v[2] <= 0.05:
                    significance = "hot" 
                elif v[2] >= 0.95:
                    significance = "cold" 
            output_str_list.append(f"{k[0]}, {k[1]}, {', '.join(map(str, v))}, {significance}")

    if Spatstat == 3:
        output_str_list.append('O, D, V, GearyC, p-value, pattern')
        for k, v in yOutput.items():
            v[2] /= 1000.0
            significance = "NS"
            if v[1] != 0 or v[2] != 0:
                if v[2] <= 0.05:
                    significance = "dissimilar" 
                elif v[2] >= 0.95:
                    significance = "similar" 
            output_str_list.append(f"{k[0]}, {k[1]}, {', '.join(map(str, v))}, {significance}")

    return '\n'.join(output_str_list)





