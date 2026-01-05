from pathfinder import PathFinder
from engine import Intelligence
from graph import Graph
from metric import *
from menu import Display_Menu

def main():
    topology = "topology.json"
    graph = Graph(topology)
    
    pf = PathFinder(graph)
    nodeID = "DnsRouter"
    print(f"Performance: {pf.dijkstras(nodeID)}")
    print(f"Connectivity: {pf.BFS(nodeID)}")
    #print(pf.DFS(nodeID))
    print(f"Node to Edge ratio: {node_to_edge_ratio(graph)}")
    print(f"Average Connectivity: {average_connectivity(graph)}")

    node2ID = "CenRouter"

    graph.remove_node(node2ID)
    
    print(f"Performance: {pf.dijkstras(nodeID)}")
    print(f"Connectivity: {pf.BFS(nodeID)}")
    print(f"Node to Edge ratio: {node_to_edge_ratio(graph)}")
    print(f"Average Connectivity: {average_connectivity(graph)}")

    Display_Menu()
if __name__ == "__main__":
    main()