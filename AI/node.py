
class Node:

    def __init__(self, id, links=[]):
        self.id = id
        self.links = links

    def get_id(self):
        return self.id