# each sentence is represented by a node (vertex)
class Node:
    def __init__(self, vertex):
        self.vertex = vertex
        self.connected_nodes = []  # store tuple (connected_node, similarity)
        self.index = -1   # index of sentence in original text
        self.weight = 0   # weight is actually the node's similarity with other nodes

    def calculate_similarity(self, sa, sb):
        sa = list(set(sa))
        sb = list(set(sb))
        intersect = 0
        for sa_word in sa:
            if sa_word in sb: intersect += 1
        return intersect / (log2(len(sa) + 0.00001) + log2(len(sb) + 0.00001))
        # the longer the sentence, the more similarity it has with other ones,
        # so logarithm is used to avoid this phenomenon,
        # since a longer sentence is not guaranteed to have more meaning than the shorter one.

    def detect_connection(self, node):
        #two nodes are connected if they have similarity.
        similarity = self.calculate_similarity(self.vertex, node.vertex)
        if similarity > 0:
            self.connected_nodes.append((node, similarity))

    def sumup_weight(self):
        for conn_node in self.connected_nodes:
            self.weight += conn_node[1]  # cummulate weight

    def set_index(self, new_index):
        self.index = new_index

    def get_weight(self):
        return self.weight

