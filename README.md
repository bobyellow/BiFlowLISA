# BiFlowLISA
**BiFlowLISA** (Tao and Thill, 2020) measures the bivariate spatial association of flow data. 

Run the codes of BiFlowLISA:
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bobyellow/BiFlowLISA/blob/main/BiFlowLISA_main.ipynb)

As detailed in Equation (3) (Tao et al. 2023), $FI_{i,j}$ is the local Moran’s I statistic, or the spatial autocorrelation measure of flow between origin $i$ and destination $j$. $f_{i,j}$ represents the value (or volume) of flow between regions $i$ and $j$. $n$ is the total number of flows in the study area. $\bar{f}$ is the average value of all flows. $w_{ij,uv}$ is the spatial flow weight between $f_{i,j}$ and $f_{u,v}$.

Equation (3):

![image](https://github.com/user-attachments/assets/c94ee5f0-263e-4ddb-b2d0-d2d0b2334dc8)

The spatial weight between flows can be defined via contiguity of origin and destination, and the k nearest neighbors based on flow distance (Tao and Thill 2016). In FlowLISA codes, a creative way of calculating spatial weight is called "a move-based flow distance (MBFD)". For any two given flows, the distance can be defined as the total number of “moves” across grid cells that the origin and destination of one flow need to take to overlap with the other. The figure below shows flows having different MBFD from flow a. 

![FlowMBFD](https://github.com/user-attachments/assets/5a43de00-7ba0-490a-b05f-b82cc96bd2d4)


The result interpretation is similar to other LISA methods. There are four categories of significant local patterns, namely ‘HH’ (high-high), ‘LL’ (low-low), ‘HL’ (high-low), and ‘LH’ (low-high). The ‘HH’ and ‘LL’ local patterns are the two types of flow clusters of strong spatial autocorrelation, i.e., flows in spatial proximity share similar values. An ‘HH’ pattern means the flow in focus has a high value while its neighboring flows exhibit a dominance of high values as well, compared with the global average. In contrast, an ‘LL’ pattern is its counterpart in the case of low values. Conversely, the ‘HL’ and ‘LH’ local patterns are the two types of outliers indicating dissimilar flow values locally. An ‘HL’ pattern means the flow in focus has a high value while its neighboring flows on average have low values compared with the global average. 

The figure below shows the results of FlowLISA at the 5% significance level, using the American Community Survey (ACS) state-to-state migration flows sourced from the U.S. Census Bureau website:

![SFlowLISA_06_17_005](https://github.com/user-attachments/assets/e0cbc289-8bf3-449a-a166-adfa93644bca)


To cite:

Tao, R., & Thill, J. C. (2020). BiFlowLISA: Measuring spatial association for bivariate flow data. Computers, Environment and Urban Systems, 83, 101519.
