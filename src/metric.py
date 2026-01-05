
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