import random as rand
import pandas as pd
from sklearn.model_selection import train_test_split
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
                __predictive_testing(g, 500)
            case 9:
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
                "7. Testing\n" \
                "8. Predictive Testing\n" \
                "9. Exit\n"
            ))
    except:
        return 0
    
    if cmd <= 0 or cmd >= 10:
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
    nodes = graph.get_nodes()
    nodeToEdgeRatio = node_to_edge_ratio(graph)
    avgConnectivity = average_connectivity(graph)
    nearestNeighbourFreq = nearest_neighbour_frequency(graph)
    betweennessCentrality = betweenness_centrality(graph)
    degreeCentrality = degree_centrality(graph)
    closenessCentrality = closeness_centrality(graph)
    averageShortestPath = average_shortest_path(graph)
    edgeBetweenness = edge_betweenness(graph)
    flowCount = flow_count(graph)

    # Impact levels for users
    impact_levels = {
        0.0: "NO IMPACT",
        0.1: "Very low",
        0.2: "Very low",
        0.3: "Low",
        0.4: "Low",
        0.5: "Mid",
        0.6: "Mid",
        0.7: "High",
        0.8: "High",
        0.9: "Very high",
        1.0: "VERY HIGH"
    }

    print(f"Node-to-Edge Ratio: {nodeToEdgeRatio}")
    print(f"Average Connectivity: {round(avgConnectivity, 2)}")
    print(f"Average Shortest Path : {round(averageShortestPath, 2)}")

    print(f"Nearest-Neighbour Frequency:    (How often a node is the closest choice from another node.)")
    for node in nearestNeighbourFreq:
        print(f"    • {node} is the nearest neighbour to {len(nearestNeighbourFreq[node])} nodes {f': {nearestNeighbourFreq[node]}' if nearestNeighbourFreq[node] else ''}")

    print("Closeness Centrality:    (How quickly each node reaches all other nodes)")
    for node in closenessCentrality:
        print(f"    • {node} = {round(closenessCentrality[node], 2)}")

    print("Degree Centrality:   (How many direct connection a node has relative to other nodes)")
    for node in degreeCentrality:
        print(f"    • {node} = {round(degreeCentrality[node], 2)} | Impact -> {impact_levels[round(degreeCentrality[node], 1)]}")

    print("Betweenness Centrality:  (How often each node lies on the shortest path between other nodes)")
    for node in betweennessCentrality:
        print(f"    • {node} = {round(betweennessCentrality[node], 2)}")

    print("Edge Betweenness:    (How often an edge lies on the shortest path between nodes)")
    for pair in edgeBetweenness:
        print(f"    • {pair[0]} - {pair[1]} = {round(edgeBetweenness[pair], 2)}")
    
    print(f"Flow Count:     (Normalised shortest-path flow share)")
    for pair in flowCount:
        print(f"    • {pair[0]} - {pair[1]} = {round(flowCount[pair], 2)}")

def __testing(graph: Graph) -> None:
    print("Please choose a test to run...\n")
    pf = PathFinder(graph)
    graph_nodes = graph.get_nodes()
    cur_shortest_path = average_shortest_path(graph)

    while True:
        try:
            cmd = int(input(
                "1. Performance Test (Dijkstras): \n" \
                "2. Connectivity Test (BFS): \n" \
                "3. Average Shortest Path on removed node: \n" \
                "4. Average Shortest Path on removed edge: \n" 
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
        elif cmd == 2:
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
            print(f"{connected_nodes}/{len(graph_nodes)-1} connected | ({round((connected_nodes/(len(graph_nodes)-1))*100, 2)}% connectivity)")
            return
        elif cmd == 3:
            rm_node = input("Enter a node to remove: ")
            if rm_node not in graph_nodes:
                print("Node does not exist.")
                continue
            new_shortest_path, failureImpactScore = failure_impact_score(graph, rm_node=rm_node)
            failureImpactScore = round(failureImpactScore, 3)
            print(f"Average shortest path BEFORE removing {rm_node}: {round(cur_shortest_path, 2)}")
            print(f"Average shortest path AFTER removing {rm_node}: {round(new_shortest_path, 2)}")
            print(f"Performance has {'INCREASED (how?)' if new_shortest_path < cur_shortest_path else 'DECREASED (valuable edge)' if new_shortest_path > cur_shortest_path else 'not changed (redundant node)'}")
            print(f"Failure impact score: {failureImpactScore} | {round((failureImpactScore-1)*100, 1)}%")
            return
        elif cmd == 4:
            print("You are removing an edge, please enter the two nodes of this edge: ")
            node1 = input("Enter node 1: ")
            node2 = input("Enter node 2: ")
            if node1 not in graph_nodes or node2 not in graph_nodes:
                print("One or both nodes do not exist.")
                continue

            edges = graph.get_edges(node1)
            if node2 not in edges:
                print("Edge does not exist in this graph")
                continue
            new_shortest_path, failureImpactScore = failure_impact_score(graph, rm_edge=(node1,node2))
            print(f"Average shortest path BEFORE removing edge: ({node1} - {node2}): {round(cur_shortest_path, 2)}")
            print(f"Average shortest path AFTER removing edge: ({node1} - {node2}): {round(new_shortest_path, 2)}")
            print(f"Performance has {'INCREASED (how?)' if new_shortest_path < cur_shortest_path else 'DECREASED (valuable edge)' if new_shortest_path > cur_shortest_path else 'not changed (redundant edge)'}")
            print(f"Failure impact score: {failureImpactScore} | {round((failureImpactScore-1)*100, 1)}%")
            return
        else:
            print("Invalid command. Going back...")
            return
        
def __predictive_testing(graph: Graph, sample_size: int = 50) -> None:
    target = input(
        "Enter a target feature -\n"
        "- Betweenness Centrality (bc)\n" \
        "- Closeness Centrality (cc)\n" \
        "- Degree Centrality (dc)\n" \
        "- Flow Count (fc)\n" \
        "- Delta (Δ) Average Shortest Path (asp)\n"
        )
    
    rows = []

    match target.lower():
        case "bc":
            target = "betweenness"
        case "cc":
            target = "closeness"
        case "dc":
            target = "degree"
        case "fc":
            target = "flow_count"
        case "asp":
            target = "delta_asp"
        case _:
            print("Invalid target. Going back...")
            return
        
    graphs: list[Graph] = []
    
    for i in range(sample_size):
        g = graph.clone()
        __perturb_weights_once(g)
        graphs.append(g)
    
    train_graphs, test_graphs = train_test_split(
    graphs,
    test_size=0.2,
    random_state=42
    )

    for i, g in enumerate(train_graphs):
        __gen_rows(g, i, rows)
        
    model = Intelligence(rows, target)
    max_risk = float("-inf")

    if target == "delta_asp":
        risk_score = __risk_score(model, *test_graphs)
        max_risk, worst_node = __max_risk_score(model, max_risk, *test_graphs)
        spike = __risk_spike(risk_score, max_risk)
        print(f"Risk score: {risk_score} | ASP increases by around {round(risk_score, 2)} path cost on average with an equal probability on one removed node")
        print(f"Max risk score: {max_risk} | ASP increases by around {round(max_risk, 2)} path cost on the most critical singular node failure -> Removed {worst_node}")
        print(f"Worst case is {round((spike-1)*100, 1)}% worse than average")

    model.display_model_score()
    model.save()

def __gen_rows(graph: Graph, id: int, rows: list = []):
    nodes = graph.get_nodes()

    __perturb_weights_once(graph)

    bc = betweenness_centrality(graph)
    cc = closeness_centrality(graph)
    dc = degree_centrality(graph)

    for node in nodes:
        flow_c = 0
        flowCount = flow_count(graph, node)
        for neighbour in flowCount:
            flow_c += flowCount[neighbour]
        rows.append(
            {
                "variant_id": id,
                "node": node,
                "degree": dc[node],
                "closeness": cc[node],
                "betweenness": bc[node],
                "flow_count": flow_c,
                "delta_asp": failure_impact_score(graph, node)[1],
            }
        )

# models congestion on edges
def __perturb_weights_once(g: Graph, low=0.8, high=1.2):
    seen = set()
    for u in g.get_nodes():
        for v, w in g.get_edges(u).items():
            e = (u, v) if u < v else (v, u)
            if e in seen:
                continue
            seen.add(e)

            factor = rand.uniform(low, high)
            new_w = w * factor

            # update both directions (undirected)
            g.get_edges(u)[v] = new_w
            g.get_edges(v)[u] = new_w

def __risk_score(model: Intelligence, *graphs: Graph):
    
    rows = []
    risk = 0.0

    for graph in graphs:
        nodes = graph.get_nodes()
        dc = degree_centrality(graph)
        cc = closeness_centrality(graph)
        bc = betweenness_centrality(graph)

        for n in nodes:
            flow_c = 0
            flowCount = flow_count(graph, n)
            for neighbour in flowCount:
                flow_c += flowCount[neighbour]
            
            rows.append({
                "degree": dc[n],
                "closeness": cc[n],
                "betweenness": bc[n],
                "flow_count": flow_c
                })

    X_df = pd.DataFrame(rows)

    preds = model.predict(X_df)

    risk += preds.mean()
    
    return risk

def __max_risk_score(model: Intelligence, max_risk: float, *graphs: Graph):

    rows = []
    node_index = []

    for i, graph in enumerate(graphs):
        nodes = graph.get_nodes()
        dc = degree_centrality(graph)
        cc = closeness_centrality(graph)
        bc = betweenness_centrality(graph)
        for n in nodes:
            flow_c = 0
            flowCount = flow_count(graph, n)
            for neighbour in flowCount:
                flow_c += flowCount[neighbour]
            
            rows.append({
                "degree": dc[n],
                "closeness": cc[n],
                "betweenness": bc[n],
                "flow_count": flow_c
                })
            
            node_index.append((i, n))

    X_df = pd.DataFrame(rows)

    preds = model.predict(X_df)

    i = int(preds.argmax())
    worst_case = float(preds[i])
    _, worst_node = node_index[i]

    return max(max_risk, worst_case), worst_node

def __risk_spike(mean_risk: float, max_risk: float) -> float:
    return max_risk/mean_risk