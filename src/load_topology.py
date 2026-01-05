import json
import os
import sys

def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    # When running normally, use project directory (or current working directory)
    return os.path.join(os.path.dirname(__file__), relative_path)

def extract_topology(topology_file: str):
    path = resource_path(topology_file)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# TODO: Rewrite current topology with updated topology
# To keep persistance
def dump_topology(t):
    with open(f"{t}") as f:
        json.dumps
