from load_topology import extract_topology

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

    # for simulating failures in graph links
    def remove_node(self, node):
        if node not in self.vertices:
            raise ValueError("Node does not exist")
        for node2 in self.vertices:
            if node2 in self.vertices[node]:
                self.remove_edge(node, node2)
        
        del self.vertices[node]
    
    def remove_edge(self, node1, node2):
        del self.vertices[node1][node2]
        del self.vertices[node2][node1]
        
    def get_nodes(self):
        return self.vertices
    
    def get_edges(self, node):
        return self.vertices[node]


    def display_graph(self):
        print(self.vertices)

    def display_all_nodes(self):
        for node in self.vertices:
            print(node)


# top = "topology.json"
# G = Graph(top)
# G.build_graph()
# G.display_all_nodes()
# G.display_graph()
# G.display_all_edges()
