import sys
import pandas as pd
import numpy as np
class AdjMatrix:
    mat: np.ndarray
    nti: dict #nameToIndex
    n: int
    m: int
    def __init__(self, df):
        all_nodes = np.append(df["from"].unique(), df["to"].unique()).tolist()
        unique_nodes = set(all_nodes)
        self.nti = dict()
        self.n = len(unique_nodes)
        self.m = 0
        for idx, node in enumerate(unique_nodes):
            self.nti[node] = idx
        self.mat = np.zeros((self.n,self.n))

    def add(self, nodeFrom, nodeTo, weight):
        self.mat[self.nti[nodeFrom], self.nti[nodeTo]] = float(weight)
        self.m += 1

    def get_neighbors(self, node):
        return self.mat[self.nti[node]]

    def num_nodes(self):
        return self.n

    def num_edges(self):
        return self.m

in_file = sys.argv[1]

df = pd.read_csv(in_file, names=["from", "to", "weight"])
df = df[df.groupby('to').to.transform(len) > 1]
model = AdjMatrix(df)
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(model.num_nodes())
print(model.num_edges())