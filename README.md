# Network Intelligence

## Overview -
A simulation of a network I have built in packet tracer, compressed into a JSON.
Usable by the user to simulate removed vertices/edges; calculating metrics based on new network utility.
Additionally, this will pin-point grey areas in the network by suggesting edges to create, removing unecessary nodes, etc, to improve efficiency while keeping a redundant WAN.

## Current Implementations -
- Ability to remove/add vertices and edges
- Calculates graph connectivity (unweighted BFS)
- Finding Fastest path (Dijkstras - simulates OSPF path)
- Calculates betweeness centrality of each node (Brandes' + Dijkstras)
- Created simple Menu Driven Interface for usability

## Future goal - 
Using current metrics, implement an intelligence which can analyse current graph and predict better connectivity.
