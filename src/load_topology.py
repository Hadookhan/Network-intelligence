import json

def extract_topology(t):
    with open(f"{t}") as f:
        topo = json.load(f)

    return topo
