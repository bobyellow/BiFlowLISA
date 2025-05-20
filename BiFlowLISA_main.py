import core.shapefile
import pandas as pd
from collections import defaultdict
from core.FlowLISA import execBIFLOWLISA

# Import input flow data from .txt files
#flowdf1 = pd.read_csv('input/Flow37xLL.txt', sep='\s+')
flowdf1 = pd.read_csv('input/YellowTaxiFlow_02012019_aggNjoin.txt', sep='\s+')
F_dt1 = dict(zip(zip(flowdf1['O'], flowdf1['D']), flowdf1['Flow']))


#flowdf2 = pd.read_csv('input/Flow37yMM.txt', sep='\s+')
flowdf2 = pd.read_csv('input/fhvhvFlow_02012019_aggNjoin.txt', sep='\s+')
F_dt2 = dict(zip(zip(flowdf2['O'], flowdf2['D']), flowdf2['Flow']))


# The input flow data should not contain zero-value flow (OD pair)
# The input flow data are stored as dictionary format, (O,D) tuple as key, flow values as lists

FlowMultiDic = defaultdict(list)
# Merge multiple flow dictionaries into one
for d in (F_dt1, F_dt2):  
    for key, value in d.items():  
        FlowMultiDic[key].append(value)

# after merging into FlowMultiDic
all_keys = set(F_dt1) | set(F_dt2)
FlowMultiDic = {
    k: [ F_dt1.get(k, 0),    # first var (or 0 if missing)
         F_dt2.get(k, 0) ]   # second var (or 0 if missing)
    for k in all_keys
}


# Import Origin and Destination shapefiles using core.shapefile
#StationPolygon1 = core.shapefile.Reader("input/Hex37_O.shp")
#StationPolygon2 = core.shapefile.Reader("input/Hex37_D.shp")
StationPolygon1 = core.shapefile.Reader("input/taxi_zones_yellow.shp")
StationPolygon2 = core.shapefile.Reader("input/taxi_zones_yellowb.shp")

# Extract polygon shapes
shapes1 = StationPolygon1.shapes()
shapes2 = StationPolygon2.shapes()

# Prepare AREAS input for Queen's and Rook's contiguity
AREAS1 = [[shape.points] for shape in shapes1]  # Ensure proper structure for AREAS
AREAS2 = [[shape.points] for shape in shapes2]  # Ensure proper structure for AREAS

# Execute FlowLISA function
outputStr = execBIFLOWLISA(AREAS1, AREAS2, FlowMultiDic, 120)
"""
    Execute BiFlowLISA to analyze spatial autocorrelation in bivariate flow data
    
    Parameters of execFLOWLISA(AREAS1, AREAS2, FlowValue, Spatstat, NeiLvl):
    1. AREAS1: Origin areas (list of polygons)
    2. AREAS2: Destination areas (list of polygons)
    3. FlowValue: Dictionary of (O, D) flow values
    4. NeiLvl: Neighborhood level for flow connections
        # Level=1: one of OD is the same and the other is neighbor;
        # Level=2: both OD are neighbors, so level ==12 means a combination of the two above
        # 18 means same D, Os are neighbors
        # 19 means same O, Ds are neighbors
        # adding 0 means including the situation of flows sharing the same O & D as flow i
        # refer to getFlowNeighbors.py for more details

    Returns:
    - A formatted output string containing results
"""
   

# Save output to text file
#output_filename = 'result/BiFlowLISA_I_Fake37xLL_yMM_Nei120_0002.txt'
output_filename = 'result/BiFlowLISA_I_NYC_taxi_fhv_Nei120_03.txt'
with open(output_filename, 'w') as outputFile:
    outputFile.write(outputStr)

print(f"Processing complete. Results saved to {output_filename}")
