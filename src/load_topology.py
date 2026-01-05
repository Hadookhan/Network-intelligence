import json

def extract_topology(t):
    with open(f"{t}") as f:
        topo = json.load(f)

    return topo

# TODO: Rewrite current topology with updated topology
# To keep persistance
def dump_topology(t):
    with open(f"{t}") as f:
        json.dumps
