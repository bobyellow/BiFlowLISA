# BiFlowLISA
**BiFlowLISA** (Tao and Thill, 2020) measures the bivariate spatial association of flow data. 

Run the codes of BiFlowLISA:
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/bobyellow/BiFlowLISA/blob/main/BiFlowLISA_main.ipynb)

![image](https://github.com/user-attachments/assets/39e615e6-aa1c-4341-b5c3-f59b0553733a)

![image](https://github.com/user-attachments/assets/376412bd-b7b9-471f-a6e8-0af5acd6633b)

The spatial weight between flows can be defined via contiguity of origin and destination, or the k nearest neighbors based on flow distance, or "a move-based flow distance (MBFD)" (see the FlowLISA repository).

![FlowMBFD](https://github.com/user-attachments/assets/5a43de00-7ba0-490a-b05f-b82cc96bd2d4)


The synthetic flow dataset was created between two lattices representing the origin and destination regions. Each lattice has 37 identical hexagonal grid cells as the basic spatial units. For any given OD pair (i,j), there is a type-I flow as well as a type-II flow. In total, there are 1,369 flows of each type.

![image](https://github.com/user-attachments/assets/20875587-1243-4cda-bed5-1e9ef7cd6927)


For the case study, we set our study area as the southern half of Manhattan that is south of East 96th and West 110th Streets. This region is ruled by the city administration as the “yellow taxi exclusive zone”, where only yellow taxis (as opposed to the green taxis) are allowed to pick up passengers. Therefore, we simplify this case study by focusing on the yellow taxis versus ride-hailing services, excluding the internal competition of taxi companies. 

The results of Local ‘HL’ and ‘LH’ patterns of taxi vs ride hailing AND ride hailing vs taxi:

![image](https://github.com/user-attachments/assets/5519c623-0475-4af4-8961-8ac197bb1071) ![image](https://github.com/user-attachments/assets/9fb10617-aa35-4f16-b651-4d8d1f6fc902)

The result interpretation is similar to other LISA methods. There are four categories of significant local patterns, namely ‘HH’ (high-high), ‘LL’ (low-low), ‘HL’ (high-low), and ‘LH’ (low-high). For the bivariate statistics, the results are also translated as acronyms but with slightly different interpretations. For instance, 'HH’ means the value of variable x is high at a given flow while the values of variable y in the flow neighborhood are high as well. In other words, a high-value type-I flow is surrounded by high-value type-II flows. 



To cite:

Tao, R., & Thill, J. C. (2020). BiFlowLISA: Measuring spatial association for bivariate flow data. Computers, Environment and Urban Systems, 83, 101519.
