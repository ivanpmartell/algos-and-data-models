import sys
import pandas as pd

class AdjList:
    adj: dict
    temp: dict
    n: int
    m: int
    def __init__(self):
        self.adj = dict()
        self.nodes = dict()
        self.n = self.m = 0

    def add(self, nodeFrom, nodeTo, weight):
        try:
            self.adj[nodeFrom].append((nodeTo,weight))
            self.count_nodeTo(nodeTo)
            self.m += 1
        except:
            self.adj[nodeFrom] = [(nodeTo,weight)]
            self.m += 1
            self.count_nodeTo(nodeTo)
            self.n += 1

    def count_nodeTo(self, nodeTo):
        try:
            if self.temp[nodeTo] == False:
                pass
        except:
            self.temp[nodeTo] = True
            self.n += 1

    def get_neighbors(self, node):
        return self.adj[node]
    
    def num_nodes(self):
        #assert self.n == len(self.adj)
        return self.n

    def num_edges(self):
        return self.m

in_file = sys.argv[1]

df = pd.read_csv(in_file, names=["from", "to", "weight"])
df = df[df.groupby('to').to.transform(len) > 1]
model = AdjList()
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(model.num_nodes())
print(model.num_edges())