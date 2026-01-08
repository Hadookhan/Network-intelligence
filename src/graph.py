from load_topology import extract_topology

class Graph:
    def __init__(self, topology):
        self.topology = extract_topology(topology)
        self.vertices = {}
        self.__build_graph()
    
    # Builds current topology from JSON
    def __build_graph(self):
        nodes = self.topology["nodes"]
        links = self.topology["links"]

        # Stores each node ID in hashtable with array of its links
        for node in nodes:
            nodeID = node["id"]
            nodeType = node["type"]
            nodeSite = node["site"]
            self.add_node(nodeID, nodeType, nodeSite)

        # Appends all links to corresponding node (undirected graph joins links both ways)
        for link in links:
            self.add_edge(link["source"], link["target"], link["cost"])
    
    def add_node(self, nodeID, type, site):
        self.vertices[nodeID] = {}
        # Add persistence here...

    def add_edge(self, node1, node2, weight):
        if node1 not in self.vertices or node2 not in self.vertices:
            raise ValueError("One or both nodes are not in the graph")
        if node2 in self.vertices[node1]:
            raise ValueError("Nodes are already connected")
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
        for node in self.vertices:
            print(f"{node} -> {self.vertices[node]}")

    def display_all_nodes(self):
        for node in self.vertices:
            print(node)


# top = "topology.json"
# G = Graph(top)
# G.build_graph()
# G.display_all_nodes()
# G.display_graph()
# G.display_all_edges()
