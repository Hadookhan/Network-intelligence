import heapq as hq # importing in-built heap for efficient Dijkstras
from queue import Queue # built-in queue for BFS
from graph import Graph

class HeapItem:
    def __init__(self, nodeID: str, distance: float) -> None:
        """
            Initialises HeapItem object to store
            nodes and their current distance travelled
        """
        self.nodeID = nodeID
        self.distance = distance

    def get_distance(self) -> float:
        """
            Returns distance of current node
        """
        return self.distance
    
    def get_node_id(self) -> str:
        """
            Returns current node
        """
        return self.nodeID

    # heapq uses __lt__ for ordering (min-heap)
    def __lt__(self, other: object) -> bool:
        """
            returns true if current nodes distance
            is shorter than compared nodes distance.
            Returns false if not.
            Used for min-heap ordering.
        """
        return self.distance < other.distance

class PathFinder:
    def __init__(self, graph: Graph) -> None:
        """
            Initialises PathFinder Object with
            specified topology.
        """
        self.graph = graph

    # Dijkstras defines the graphs performance
    # Simulates OSPF Routing
    def dijkstras(self, start_id: str) -> tuple:
        """
            Dijkstras will simulate OSPF routing in the topology.
            Given a start ID, it will traverse to each node with the
            shortest distance.
            Returns a tuple in order of:
            Shortest distances from start node to every other node in graph,
            Predecessor nodes visited during traversal to every other node,
            Sigma function, used to count number of shortest paths,
            Stack of all nodes in nondecreasing distance order.
        """
        adj = self.graph.get_nodes()

        # distances to be overriden by shorter distances from start to node_id
        distances = {node_id: float('inf') for node_id in adj}
        distances[start_id] = 0

        # number of shortest paths from start_id to v
        sigma = {v: 0.0 for v in adj}
        sigma[start_id] = 1.0

        # list of predecessors of v on shortest paths from start_id
        pred = {v: [] for v in adj}

        visited = set()
        heap: list[HeapItem] = []

        # nodes in nondecreasing distance order (push when finalized)
        S: list[str] = []

        hq.heappush(heap, HeapItem(start_id, 0))

        while heap:
            item = hq.heappop(heap)
            current_id = item.get_node_id()
            distance = item.get_distance()

            if distance != distances[current_id]:
                continue

            if current_id in visited:
                continue

            visited.add(current_id)
            S.append(current_id)

            for neighbour_id, weight in adj[current_id].items():
                if neighbour_id in visited:
                    continue

                new_dist = distances[current_id] + weight

                if new_dist < distances[neighbour_id]:
                    distances[neighbour_id] = new_dist
                    hq.heappush(heap, HeapItem(neighbour_id, new_dist))

                    sigma[neighbour_id] = sigma[current_id]
                    pred[neighbour_id] = [current_id]
                elif new_dist == distances[neighbour_id]:
                    sigma[neighbour_id] += sigma[current_id]
                    pred[neighbour_id].append(current_id)

        return distances, pred, sigma, S

    # BFS + DFS will help identify all traversable nodes in the graph (defines graphs connectivity)

    def BFS(self, start_id: str) -> set:
        """
            Breadth-first-search through the topology
            given a start node.
            Will traverse every node in the graph and
            return all nodes it visits.
        """
        queue = Queue()
        visited = set()
        
        queue.put(start_id)
        visited.add(start_id)

        while queue.qsize() > 0:
            cur_id = queue.get()
            neighbours = self.graph.get_nodes()[cur_id]

            for neighbour_id in neighbours:
                if neighbour_id not in visited:
                    queue.put(neighbour_id)
                    visited.add(neighbour_id)
        return visited

    def DFS(self, start_id: str) -> set:
        """
            Depth-first-search through the topology
            given a start node.
            Will traverse every node in the graph and
            return all nodes it visits.
        """
        stack = []
        visited = set()

        stack.append(start_id)
        visited.add(start_id)

        while len(stack) > 0:
            cur_id = stack.pop()
            neighbours = self.graph.get_nodes()[cur_id]

            for neighbour_id in neighbours:
                if neighbour_id not in visited:
                    stack.append(neighbour_id)
                    visited.add(neighbour_id)
        return visited
    
    def brandes(self, node1: str = None) -> tuple:
        """
            Brandes' will calculate the betweeness of nodes and
            edges in the graph using Dijkstras.
            -> Finds the shortest path between a pair of nodes
            and returns a tuple containing in order of:
            Centrality Betweeness,
            Edge Betweeness,
            Edge flow.
        """

        V = list(self.graph.get_nodes().keys())

        CB = {v: 0.0 for v in V} if not node1 else {node1: 0.0} # Betweenness centrality of either all nodes or nodes between source and target
        EB = {} # Edge betweenness
        edge_flow = {} # flow count for edges in fastest path
        
        if not node1:
            for u in V:
                for v in self.graph.get_edges(u):
                    if u == v:
                        continue
                    e = (u,v) if u < v else (v,u)
                    EB[e] = 0
                    edge_flow[e] = 0

            for s in V:
                # Distance + pred + sigma + stack order
                _, pred, sigma, S = self.dijkstras(s)
                flow_delta = {v: 0.0 for v in V}

                for t in V:
                    if t != s and sigma[t] > 0:   # reachable
                        flow_delta[t] += 1.0
                        
                # dependency accumulation
                delta = {v: 0.0 for v in V}

                # Process nodes in reverse order of distance from s
                while S:
                    w = S.pop()
                    if sigma[w] == 0:
                        continue
                    
                    for v in pred[w]:
                        if v == w:
                            continue
                        
                        share = (sigma[v] / sigma[w]) * flow_delta[w]
                        c = (sigma[v] / sigma[w]) * (1.0 + delta[w])
                        delta[v] += c

                        e = (v, w) if v < w else (w, v)

                        if e in edge_flow:
                            edge_flow[e] += share

                        flow_delta[v] += share

                        if e not in EB:
                            continue

                        EB[e] += c

                    if w != s:
                        CB[w] += delta[w]
            
            # Undirected graphs: each shortest path counted twice (s->t and t->s)
            for v in CB:
                CB[v] /= 2.0
            for e in EB:
                EB[e] /= 2.0
            for f in edge_flow:
                edge_flow[f] /= 2.0
        else:
            # Single-node mode: compute CB for node1, and EB/edge_flow for edges incident to node1
            if node1 not in V:
                raise ValueError("Node does not exist in current graph")

            edges = self.graph.get_edges(node1)
            # initialise node1 neighbours
            for neighbour in edges:
                if neighbour == node1:
                    continue
                e = (node1, neighbour) if node1 < neighbour else (neighbour, node1)
                EB[e] = 0.0
                edge_flow[e] = 0.0

            for s in V:
                # Run Dijkstra from each source
                _, pred, sigma, S = self.dijkstras(s)

                # flow demand: 1 unit to every reachable target t != s
                flow_delta = {v: 0.0 for v in V}
                for t in V:
                    if t != s and sigma[t] > 0:
                        flow_delta[t] = 1.0

                # Brandes dependency accumulation
                delta = {v: 0.0 for v in V}

                while S:
                    w = S.pop()
                    if sigma[w] == 0:
                        continue

                    for v in pred[w]:
                        if v == w:
                            continue

                        share = (sigma[v] / sigma[w]) * flow_delta[w]
                        c = (sigma[v] / sigma[w]) * (1.0 + delta[w])
                        delta[v] += c

                        e = (v, w) if v < w else (w, v)

                        # Only track edges incident to node1
                        if e in edge_flow:
                            edge_flow[e] += share
                        if e in EB:
                            EB[e] += c

                        flow_delta[v] += share

                    if w != s and w == node1:
                        CB[node1] += delta[w]

            # Undirected correction (each s->t counted twice)
            CB[node1] /= 2.0
            for e in EB:
                EB[e] /= 2.0
            for e in edge_flow:
                edge_flow[e] /= 2.0



        return CB, EB, edge_flow
