# Network Intelligence

## Overview -
A simulation of a network I have built in packet tracer, compressed into a JSON.
Usable by the user to simulate removed vertices/edges; calculating metrics based on new network utility.
Additionally, this will pin-point grey areas in the network by suggesting edges to create, removing unecessary nodes, etc, to improve efficiency while keeping a redundant WAN.

## Current Implementations -
- Ability to remove/add vertices and edges
- Calculates graph connectivity (unweighted BFS)
- Finding Fastest path (Dijkstras - simulates OSPF path)
- Calculates betweenness centrality, edge betweenness, and flow count of each node (Brandes' + Dijkstras)
- Calculates average shortest path (ASP) of graph
- Created simple Menu Driven Interface for usability
- Trained RandomForestRegressor Model with ~97% accuracy using metrics as features
- Predicts average and max risk score using ASP as feature target

## Future goals - 
- Model will suggest improvements to the network
- Create GUI in replacement for Menu Interface