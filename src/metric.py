from pathfinder import PathFinder
from graph import Graph

def node_to_edge_ratio(graph: Graph) -> float:
    n = len(graph.get_nodes())
    m = 0
    
    for node in graph.get_nodes():
        for _ in graph.get_edges(node):
            m += 1
    m = m/2
    return n/m

def average_connectivity(graph: Graph) -> float:
    n = len(graph.get_nodes())
    m = 0
    for node in graph.get_nodes():
        for _ in graph.get_edges(node):
            m += 1
    m = m*2
    return m/n

def nearest_neighbour_frequency(graph: Graph) -> dict:

    nodes = graph.get_nodes()
    pf = PathFinder(graph)
    
    cur_min_edge = float("inf")
    cur_min_node = None

    node_contains_shortest_path_count = {n:set() for n in nodes}

    for node in nodes:
        cur_min_edge = float("inf")
        cur_min_node = None

        distance, _, _, _ = pf.dijkstras(node)
        for to_node in distance:
            if distance[to_node] < cur_min_edge and to_node != node:
                cur_min_edge = distance[to_node]
                cur_min_node = to_node
        if cur_min_node:        
            node_contains_shortest_path_count[cur_min_node].add(node)
    
    return node_contains_shortest_path_count

def betweenness_centrality(graph: Graph) -> dict:
    """
    Calculates the betweeness centrality for all nodes in graph 
    then stores and returns them in a dictionary.
    """
    pf = PathFinder(graph)

    return pf.brandes()
        
def degree_centrality(graph: Graph) -> dict:
    """
    Calculates the degree centrality for all nodes in graph 
    then stores and returns them in a dictionary. Each value will be 
    between 0.0 and 1.0.
    """
    nodes = graph.get_nodes()

    if len(nodes) <= 1:
        return {node: 0.0 for node in nodes}

    # All nodes in list, minus current node
    node_count = len(nodes) - 1

    Dc_map = {n:0 for n in nodes}

    for node in nodes:
        edges = graph.get_edges(node)
        Dc_map[node] = len(edges) / node_count
    
    return Dc_map

def closeness_centrality(graph: Graph) -> dict:
    """
    Calculates the closeness centrality for all nodes in graph 
    then stores and returns them in a dictionary. Each value will be 
    between 0.0 and 1.0.
    """
    pf = PathFinder(graph)
    nodes = graph.get_nodes()
    

    Cc_map = {n:0 for n in nodes}

    for node in nodes:
        total = 0
        reachable = 0
        shortest_path, _, _, _ = pf.dijkstras(node)
        for target, dist in shortest_path.items():
            if target != node:
                total += dist
                reachable += 1

        if total > 0:
            Cc_map[node] = reachable / total
        else:
            Cc_map[node] = 0

    return Cc_map


def average_shortest_path(graph: Graph) -> float:
    nodes = graph.get_nodes()
    pf = PathFinder(graph)

    total = 0.0
    pair_count = 0

    # To avoid double-counting in undirected graphs
    seen = set()

    for u in nodes:
        dist, _, _, _ = pf.dijkstras(u)
        if not dist:
            continue

        for v, d in dist.items():
            if u == v:
                continue

            pair = (u, v) if u < v else (v, u)
            if pair in seen:
                continue

            seen.add(pair)
            total += d
            pair_count += 1

    return total / pair_count if pair_count > 0 else 0.0


def edge_betweenness(graph: Graph):
    pass

def flow_count(graph: Graph):
    pass

def redundancy_score(graph: Graph):
    pass



