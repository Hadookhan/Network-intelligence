import heapq as hq # importing in-built heap for efficient Dijkstras

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

    # Simulates OSPF Routing
    def dijkstras(self, start_id):
        adj = self.graph.get_nodes()

        # distances to be overriden by shorter distances
        distances = {node_id: float('inf') for node_id in adj}
        previous = {node_id: None for node_id in adj}
        visited = set()
        heap = []

        distances[start_id] = 0
        hq.heappush(heap, HeapItem(start_id, 0))

        while heap:
            item = hq.heappop(heap)
            current_id = item.get_node_id()

            if current_id in visited:
                continue

            visited.add(current_id)

            for neighbour_id, weight in adj[current_id].items():
                if neighbour_id in visited:
                    continue

                new_dist = distances[current_id] + weight
                if new_dist < distances[neighbour_id]:
                    distances[neighbour_id] = new_dist
                    previous[neighbour_id] = current_id
                    hq.heappush(heap, HeapItem(neighbour_id, new_dist))

        return distances, previous

    def BFS(self):
        pass

    def DFS(self):
        pass