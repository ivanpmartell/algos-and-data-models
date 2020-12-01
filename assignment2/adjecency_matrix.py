import sys
import pandas as pd
import numpy as np
from queue import PriorityQueue

class AdjMatrix:
    mat: np.ndarray
    nti: dict #nameToIndex
    itn: dict #indexToName
    n: int
    m: int
    def __init__(self, df):
        all_nodes = np.append(df["from"].unique(), df["to"].unique()).tolist()
        unique_nodes = set(all_nodes)
        self.nti = dict()
        self.itn = dict()
        self.n = len(unique_nodes)
        self.m = 0
        for idx, node in enumerate(unique_nodes):
            n = int(node)
            self.nti[n] = idx
            self.itn[idx] = n
        self.mat = np.zeros((self.n,self.n))

    def add(self, nodeFrom, nodeTo, weight):
        nF = int(nodeFrom)
        nT = int(nodeTo)
        self.mat[self.nti[nF], self.nti[nT]] = float(weight)
        self.m += 1

    def get_neighbors(self, node):
        return self.mat[self.nti[node]]

    def num_nodes(self):
        return self.n

    def num_edges(self):
        return self.m

    def degree_distribution(self):
        dd = dict()
        for i in range(len(self.mat)):
            node_degree = 0
            for j in range(len(self.mat[0])):
                if self.mat[i,j] > 0:
                    node_degree += 1
            try:
                dd[node_degree] += 1
            except KeyError:
                dd[node_degree] = 1
        return dd
    
    def clustering_coefficient(self):
        triangles = 0
        triads = 0
        for node in sorted(self.nti):
            neighbors = self.get_neighbors(node)
            for v_idx, v_w in enumerate(neighbors):
                if v_w == 0.0:
                    continue
                v = self.itn[v_idx]
                if node < v:
                    v_neighbors = self.get_neighbors(v)
                    connections = 0
                    for w_idx, w_w in enumerate(v_neighbors):
                        connections += 1
                        if w_w == 0.0:
                            continue
                        w = self.itn[w_idx]
                        if v < w:
                            triangles += 1
                        else:
                            triads += 1
                    if connections == 0:
                        triads += 1
        ts = 3*triangles
        return ts/(ts+triads)
    
    def average_path_length(self):
        costs = 0
        for node in self.nti.keys():
            costs += self.BFS(node)
        apl = costs/(self.n*(self.n-1))
        return apl
    
    def BFS(self, source):
        visited = {}
        for n_idx, n_w in enumerate(self.get_neighbors(source)):
            if n_w == 0.0:
                continue
            visited[self.itn[n_idx]] = False
        visited[source] = True
        pq = PriorityQueue()
        pq.put((0, source))
        cost = 0
        while pq.empty() == False:
            w, u = pq.get()
            cost += w
            for v_idx, c in enumerate(self.get_neighbors(u)):
                if c == 0.0:
                    continue
                v = self.itn[v_idx]
                if visited[v] == False:
                    visited[v] = True
                    pq.put((c, v))
        return cost

in_file = sys.argv[1]

df = pd.read_csv(in_file, names=["from", "to", "weight"])
df = df[df.groupby('to').to.transform(len) > 1]
model = AdjMatrix(df)
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(f"N={model.num_nodes()}")
print(f"M={model.num_edges()}")

#algos
print(f"Degree Distribution={model.degree_distribution()}")
print(f"Global CC={model.clustering_coefficient()}")
print(f"APL={model.average_path_length()}")