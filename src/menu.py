from pathfinder import PathFinder
from engine import Intelligence
from graph import Graph
from metric import *


def Display_Menu():
    topology = "topology.json"
    g = Graph(topology)
    while True:
        cmd = __command()
        
        match cmd:
            case 1:
                g.display_graph()
            case 2:
                add_node(g)
            case 3:
                add_edge(g)
            case 4:
                remove_node(g)
            case 5:
                remove_edge(g)
            case 6:
                view_metrics(g)
            case 7:
                pass
            case 8:
                return
            case _:
                print("Invalid input")



def __command():
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
        return None
    
    if cmd <= 0 or cmd >= 9:
        return None

    return cmd

def add_node(graph):
    valid_types = ["switch","router"]
    node_id = input("Enter new node name: ")
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

def add_edge(graph):
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

def remove_node(graph):
    node_id = input("Enter node: ")
    if node_id not in graph.get_nodes():
        print("Node does not exist in current graph. Going back...")
        return
    graph.remove_node(node_id)
    print("Node removed.")
    return

def remove_edge(graph):
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

def view_metrics(graph):
    nodeToEdgeRatio = node_to_edge_ratio(graph)
    avgConnectivity = average_connectivity(graph)

    print(f"Node-to-Edge Ratio: {nodeToEdgeRatio}")
    print(f"Average Connectivity: {avgConnectivity}")
    