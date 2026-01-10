from load_topology import extract_topology

class Graph:
    def __init__(self, topology: str) -> None:
        """
            Initialise a graph from a loaded JSON stored topology
            Automatically builds from JSON.
        """
        self.topology: dict[str, list[dict[str, str]]] = extract_topology(topology)
        self.vertices: dict[str, dict[str, float]] = {}
        self.__build_graph()
    
    def __build_graph(self) -> None:
        """
            Builds current topology from JSON.
            Compacts data into a dictionary
        """
        nodes: list[str] = self.topology["nodes"]
        links: list[str] = self.topology["links"]

        # Stores each node ID in hashtable with array of its links
        for node in nodes:
            nodeID = node["id"]
            nodeType = node["type"]
            nodeSite = node["site"]
            self.add_node(nodeID, nodeType, nodeSite)

        # Appends all links to corresponding node (undirected graph joins links both ways)
        for link in links:
            self.add_edge(link["source"], link["target"], float(link["cost"]))
    
    def add_node(self, nodeID: str, type: str, site: str) -> None:
        """
            Adding a node to the current topology.
        """
        self.vertices[nodeID] = {}
        # Add persistence here...

    def add_edge(self, node1: str, node2: str, weight: float) -> None:
        """
            Adding an undirected edge between two nodes in the current topology.
        """
        if node1 not in self.vertices or node2 not in self.vertices:
            raise ValueError("One or both nodes are not in the graph")
        if node2 in self.vertices[node1]:
            raise ValueError("Nodes are already connected")
        self.vertices[node1][node2] = weight
        self.vertices[node2][node1] = weight

    # for simulating failures in graph links
    def remove_node(self, node: str) -> None:
        """
            Removing a node in the current topology.
        """
        if node not in self.vertices:
            raise ValueError("Node does not exist")
        for node2 in self.vertices:
            if node2 in self.vertices[node]:
                self.remove_edge(node, node2)
        
        del self.vertices[node]
    
    def remove_edge(self, node1: str, node2: str) -> None:
        """
            Removes undirected edge from graph.
        """
        del self.vertices[node1][node2]
        del self.vertices[node2][node1]
        
    def get_nodes(self) -> dict[str, dict[str, float]]:
        """
            Returns a dictionary object of all nodes in 
            the current topology.
        """
        return self.vertices
    
    def get_edges(self, node: str) -> dict[str, float]:
        """
            Returns a dictionary object mapping edges from
            a specified node to its corresponding weight.
        """
        return self.vertices[node]


    def display_graph(self) -> None:
        """
            Prints all nodes in the graph.
            Used for easier readability.
        """
        for node in self.vertices:
            print(f"{node} -> {self.vertices[node]}")
