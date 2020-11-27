import sys
import pandas as pd

class EdgeList:
    edges: list
    temp: dict
    n: int
    m: int
    def __init__(self):
        self.edges = []
        self.temp = dict()
        self.n = 0
        self.m = 0

    def add(self, nodeFrom, nodeTo, weight):
        self.edges.append((nodeFrom,nodeTo,weight))
        self.m += 1
        self.count_node(nodeFrom)
        self.count_node(nodeTo)

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge[0] == node:
                neighbors.append((edge[1],edge[2]))
        return neighbors

    def count_node(self, node):
        try:
            if self.temp[node] == False:
                pass
        except:
            self.temp[node] = True
            self.n += 1

    def get_neighbors(self, node):
        return self.edges[node]
    
    def num_nodes(self):
        #assert self.n == len(self.adj)
        return self.n

    def num_edges(self):
        return self.m

in_file = sys.argv[1]

df = pd.read_csv(in_file, names=["from", "to", "weight"])
df = df[df.groupby('to').to.transform(len) > 1]
model = EdgeList()
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(model.num_nodes())
print(model.num_edges())