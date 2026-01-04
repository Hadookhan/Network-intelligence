from load_topology import extract_topology
from node import Node

def get_topology(topology):
    return extract_topology(topology)

class Graph:
    def __init__(self, topology):
        self.topology = get_topology(topology)
        self.vertices = {}
        self.__build_graph()
    
    # Builds current topology from JSON
    def __build_graph(self):
        nodes = self.topology["nodes"]
        links = self.topology["links"]

        # Stores each node ID in hashtable with array of its links
        for node in nodes:
            self.add_node(node)

        # Appends all links to corresponding node (undirected graph joins links both ways)
        for link in links:
            self.add_edge(link["source"], link["target"], link["cost"])
    
    def add_node(self, node):
        self.vertices[node["id"]] = {}

    def add_edge(self, node1, node2, weight):
        self.vertices[node1][node2] = weight
        self.vertices[node2][node1] = weight
        
    def get_nodes(self):
        return self.vertices

    def display_graph(self):
        print(self.vertices)

    def display_all_nodes(self):
        for node in self.vertices:
            print(node)

    ### TODO: FIX
    def display_all_edges(self):
        nodes = self.topology["nodes"]

        edges = set()
        for node in nodes:
            for edge in self.vertices[node["id"]]:
                if (node['id'], edge) not in edges:
                    print(f"{node['id']} -> {edge}")
                    edges.add((node['id'], edge))


# top = "topology.json"
# G = Graph(top)
# G.build_graph()
# G.display_all_nodes()
# G.display_graph()
# G.display_all_edges()
