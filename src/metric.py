from pathfinder import PathFinder

def node_to_edge_ratio(graph):
    n = len(graph.get_nodes())
    m = 0
    
    for node in graph.get_nodes():
        for _ in graph.get_edges(node):
            m += 1
    m = m/2
    return n/m

def average_connectivity(graph):
    n = len(graph.get_nodes())
    m = 0
    for node in graph.get_nodes():
        for _ in graph.get_edges(node):
            m += 1
    m = m*2
    return m/n

def nearest_neighbour_frequency(graph):

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

def betweeness_centrality(graph):
    pf = PathFinder(graph)

    return pf.brandes()
        



