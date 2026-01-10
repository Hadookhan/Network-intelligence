from pathfinder import PathFinder
from engine import Intelligence
from graph import Graph
from metric import *


def Display_Menu() -> None:
    """
        Displays Network intelligence Menu Interface.
    """
    print("\n-----------------------------------")
    print("NETWORK INTELLIGENCE PROGRAM")
    print("-----------------------------------")

    topology = "topology.json"
    g = Graph(topology)
    while True:
        cmd = __command()
        
        match cmd:
            case 1:
                g.display_graph()
            case 2:
                __add_node(g)
            case 3:
                __add_edge(g)
            case 4:
                __remove_node(g)
            case 5:
                __remove_edge(g)
            case 6:
                __view_metrics(g)
            case 7:
                __testing(g)
            case 8:
                return
            case _:
                print("Invalid input")



def __command() -> int:
    try:
        cmd = int(
            input(
                "\n1. Display Topology\n" \
                "2. Add new node\n" \
                "3. Add new edge\n" \
                "4. Delete node\n" \
                "5. Delete edge\n" \
                "6. View Metrics\n" \
                "7. Testing\n"
                "8. Exit\n"
            ))
    except:
        return 0
    
    if cmd <= 0 or cmd >= 9:
        return 0

    return cmd

def __add_node(graph: Graph) -> None:
    valid_types = ["switch","router"]
    node_id = input("Enter new node name: ")
    if node_id in graph.get_nodes():
        print("Node name already exists. Going back...")
        return
    node_type = input("Is the new node a Switch (s) or a Router (r)? ")
    
    if node_type.lower() == "s" or node_type.lower() == "switch":
        node_type = "Switch"
    elif node_type.lower() == "r" or node_type.lower() == "router":
        node_type = "Router"
    
    if node_type.lower() not in valid_types:
        print("Invalid node type. Going back...")
        return
    
    node_site = input("Enter the site name of the new node: ")

    graph.add_node(node_id, node_type, node_site)

    print("Node added!")

    return

def __add_edge(graph: Graph) -> None:
    node1 = input("Enter first node: ")
    node2 = input("Enter second node: ")

    graph_nodes = graph.get_nodes()
    if node1 not in graph_nodes or node2 not in graph_nodes:
        print("One or both nodes are not present in the current graph. Going back...")
        return
    if node2 in graph_nodes[node1]:
        print("Nodes are already connected. Going back...")
        return
    
    try:
        weight = int(input("Enter edge weight: "))
    except:
        print("Invalid weight. Going back...")
        return
    
    graph.add_edge(node1, node2, weight)

    print(f"Added edge ({node1} - {node2}) Cost: {weight}")
    return

def __remove_node(graph: Graph) -> None:
    node_id = input("Enter node: ")
    if node_id not in graph.get_nodes():
        print("Node does not exist in current graph. Going back...")
        return
    graph.remove_node(node_id)
    print("Node removed.")
    return

def __remove_edge(graph: Graph) -> None:
    node1 = input("Enter first node: ")
    node2 = input("Enter second node: ")

    graph_nodes = graph.get_nodes()
    if node1 not in graph_nodes or node2 not in graph_nodes:
        print("One or both nodes are not present in the current graph. Going back...")
        return
    if node2 not in graph_nodes[node1]:
        print("Nodes are not connected. Going back...")
        return
    
    graph.remove_edge(node1, node2)
    print("Edge removed.")
    return

def __view_metrics(graph: Graph) -> None:
    nodeToEdgeRatio = node_to_edge_ratio(graph)
    avgConnectivity = average_connectivity(graph)
    nearestNeighbourFreq = nearest_neighbour_frequency(graph)
    betweennessCentrality = betweenness_centrality(graph)
    degreeCentrality = degree_centrality(graph)
    closenessCentrality = closeness_centrality(graph)
    averageShortestPath = average_shortest_path(graph)
    edgeBetweenness = edge_betweenness(graph)
    flowCount = flow_count(graph)

    print(f"Node-to-Edge Ratio: {nodeToEdgeRatio}")
    print(f"Average Connectivity: {avgConnectivity}")
    print(f"Average Shortest Path : {averageShortestPath}")

    print(f"Closeness Centrality:")
    for node in closenessCentrality:
        print(f"    • {node} = {closenessCentrality[node]}")

    print("Degree Centrality:")
    for node in degreeCentrality:
        print(f"    • {node} = {degreeCentrality[node]}")

    print("Betweenness Centrality:")
    for node in betweennessCentrality:
        print(f"    • {node} = {betweennessCentrality[node]}")

    print("Edge Betweenness:")
    for pair in edgeBetweenness:
        print(f"    • {pair} = {edgeBetweenness[pair]}")
    
    print(f"Flow Count:")
    for pair in flowCount:
        print(f"    • {pair} = {flowCount[pair]}")
    
    print(f"Nearest-Neighbour Frequency:")
    for node in nearestNeighbourFreq:
        print(f"    • {node} is the nearest neighbour to {len(nearestNeighbourFreq[node])} nodes {f': {nearestNeighbourFreq[node]}' if nearestNeighbourFreq[node] else ''}")

def __testing(graph: Graph) -> None:
    print("Please choose a test to run...\n")
    pf = PathFinder(graph)
    graph_nodes = graph.get_nodes()

    while True:
        try:
            cmd = int(input(
                "1. Performance Test (Dijkstras): \n" \
                "2. Connectivity Test (BFS): \n" 
            ))
        except:
            print("Invalid command. Going back...")
            continue
        if cmd == 1:
            start_node = input("Please enter a starting Node: ")
            if start_node not in graph_nodes:
                print("Node does not exist.")
                continue
            fastest_path, _, _, _ = pf.dijkstras(start_node)
            for i, node in enumerate(fastest_path):
                if start_node == node:
                    continue
                print(f"{i+1} : {start_node} -> {node} = {fastest_path[node] if fastest_path[node] != float('inf') else None}")
            return
        if cmd == 2:
            connected_nodes = 0
            start_node = input("Please enter a starting Node: ")
            if start_node not in graph_nodes:
                print("Node does not exist.")
                continue
            traversed_graph = pf.BFS(start_node)
            for i, node in enumerate(traversed_graph):
                if start_node == node:
                    continue
                print(f"{i+1} : {node}")
                connected_nodes += 1
            print(f"{connected_nodes}/{len(graph_nodes)-1} connected. ({round((connected_nodes/(len(graph_nodes)-1))*100, 2)}% connectivity)")
            return

        
        
        

        
    