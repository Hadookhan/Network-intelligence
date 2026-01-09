import heapq as hq # importing in-built heap for efficient Dijkstras
from queue import Queue # built-in queue for BFS

class HeapItem:
    def __init__(self, nodeID, distance):
        self.nodeID = nodeID
        self.distance = distance

    def get_distance(self):
        return self.distance
    
    def get_node_id(self):
        return self.nodeID

    # heapq uses __lt__ for ordering (min-heap)
    def __lt__(self, other):
        return self.distance < other.distance

class PathFinder:
    def __init__(self, graph):
        self.graph = graph

    # Dijkstras defines the graphs performance
    # Simulates OSPF Routing
    def dijkstras(self, start_id):
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
        heap = []

        # nodes in nondecreasing distance order (push when finalized/popped)
        S = []

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
                    pred[neighbour_id] = pred[current_id]
                elif new_dist == distances[neighbour_id]:
                    sigma[neighbour_id] += sigma[current_id]
                    pred[neighbour_id].append(current_id)

        return distances, pred, sigma, S

    # BFS + DFS will help identify all traversable nodes in the graph (defines graphs connectivity)

    def BFS(self, start_id):
        queue = Queue()
        visited = set()
        
        queue.put(start_id)
        visited.add(start_id)
        cur_weight = 0

        while queue.qsize() > 0:
            cur_id = queue.get()
            neighbours = self.graph.get_nodes()[cur_id]

            for neighbour_id in neighbours:
                if neighbour_id not in visited:
                    queue.put(neighbour_id)
                    visited.add(neighbour_id)
        return visited

    def DFS(self, start_id):
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
    
    def brandes(self):
        V = list(self.graph.get_nodes().keys())
        CB = {v: 0.0 for v in V}

        for s in V:
            # Dijkstra + pred + sigma + stack order
            _, pred, sigma, S = self.dijkstras(s)

            # dependency accumulation
            delta = {v: 0.0 for v in V}

            # Process nodes in reverse order of distance from s
            while S:
                w = S.pop()
                for v in pred[w]:
                    # fraction of shortest paths via v
                    if sigma[w] != 0:
                        delta_contrib = (sigma[v] / sigma[w]) * (1.0 + delta[w])
                        delta[v] += delta_contrib

                # Don't count the source itself
                if w != s:
                    CB[w] += delta[w]

        # Undirected graphs: each shortest path counted twice (s->t and t->s)
        for v in CB:
            CB[v] /= 2.0

        return CB


            










        
        

