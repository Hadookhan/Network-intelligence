from pathfinder import PathFinder
from engine import Intelligence
from graph import Graph

def main():
    topology = "topology.json"
    graph = Graph(topology)
    
    pf = PathFinder(graph)

if __name__ == "__main__":
    main()