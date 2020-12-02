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
            n = node
            self.nti[n] = idx
            self.itn[idx] = n
        self.mat = np.zeros((self.n,self.n))

    def add(self, nodeFrom, nodeTo, weight):
        nF = nodeFrom
        nT = nodeTo
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
        self.sort_matrix()
        for node in self.nti:
            levels = [0,0,0,0]
            levels[0] += 1
            neighbors = self.get_neighbors(node)
            for v_idx, v_w in enumerate(neighbors):
                levels[1] += 1
                if v_w == 0.0:
                    continue
                v = self.itn[v_idx]
                if node < v:
                    v_neighbors = self.get_neighbors(v)
                    for w_idx, w_w in enumerate(v_neighbors):
                        levels[2] += 1
                        if w_w == 0.0:
                            continue
                        w = self.itn[w_idx]
                        if v < w:
                            connections = 0
                            for i in range(v_idx+1, len(neighbors)):
                                levels[3] += 1
                                if neighbors[i] == 0.0:
                                    continue
                                connections += 1
                                if self.itn[i] == w:
                                    triangles += 1
                                else:
                                    triads += 1
                            if connections == 0:
                                triads += 1
        ts = 3*triangles
        try:
            result = ts/(ts+triads)
        except ZeroDivisionError:
            result = 0
        return result

    def sort_matrix(self):
        sorted_nodes = sorted(self.nti.keys())
        temp_mat = np.zeros((self.n,self.n))
        temp_nti = dict()
        temp_itn = dict()
        for node_idx, node in enumerate(sorted_nodes):
            temp_nti[node] = node_idx
            temp_itn[node_idx] = node
        for node_idx, node in enumerate(sorted_nodes):
            for idx, n_w in enumerate(self.get_neighbors(node)):
                if n_w == 0.0:
                    continue
                neighbor_idx = temp_nti[self.itn[idx]]
                temp_mat[node_idx,neighbor_idx] = n_w
        self.mat = temp_mat
        self.nti = temp_nti
        self.itn = temp_itn
    
    def average_path_length(self):
        costs = 0
        for node in self.nti.keys():
            costs += self.BFS(node)
        apl = costs/(self.n*(self.n-1))
        return apl
    
    def BFS(self, source):
        visited = {}
        for n in self.nti.keys():
            visited[n] = False
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

df = pd.read_csv(in_file, names=["from", "to", "weight"], skiprows=1)
#df = df[df.groupby('to').to.transform(len) > 1]
model = AdjMatrix(df)
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(f"N={model.num_nodes()}")
print(f"M={model.num_edges()}")

#algos
print(f"Degree Distribution={model.degree_distribution()}")
print(f"Global CC={model.clustering_coefficient()}")
print(f"APL={model.average_path_length()}")