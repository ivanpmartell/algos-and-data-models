import sys
import pandas as pd
from queue import PriorityQueue

class AdjList:
    adj: dict
    temp: dict
    n: int
    m: int
    def __init__(self):
        self.temp = dict()
        self.adj = dict()
        self.nodes = dict()
        self.n = self.m = 0

    def add(self, nodeFrom, nodeTo, weight):
        nF = int(nodeFrom)
        nT = int(nodeTo)
        w = float(weight)
        self.addNode(nF)
        self.addNode(nT)
        self.adj[nF].append((nT,w))
        self.m += 1
    
    def addNode(self, node):
        try:
            self.adj[node]
        except:
            self.adj[node] = []
            self.n += 1

    def get_neighbors(self, node):
        return self.adj[node]
    
    def num_nodes(self):
        #assert self.n == len(self.adj)
        return self.n

    def num_edges(self):
        return self.m
    
    def degree_distribution(self):
        dd = dict()
        for n, e in self.adj.items():
            try:
                dd[len(e)] += 1
            except:
                dd[len(e)] = 1
        return dd
    
    def clustering_coefficient(self):
        triangles = 0
        triads = 0
        for node in sorted(self.adj):
            neighbors = self.get_neighbors(node)
            for v, _ in neighbors:
                if node < v:
                    v_neighbors = self.get_neighbors(v)
                    connections = 0.0
                    for w, _ in v_neighbors:
                        connections += 1
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
        for node in self.adj:
            costs += self.BFS(node)
        apl = costs/(self.n*(self.n-1))
        return apl
    
    def BFS(self, source):
        visited = {}
        for n, _ in self.get_neighbors(source):
            visited[n] = False
        visited[source] = True
        pq = PriorityQueue()
        pq.put((0, source))
        cost = 0
        while pq.empty() == False:
            w, u = pq.get()
            cost += w
            for v, c in self.get_neighbors(u):
                if visited[v] == False:
                    visited[v] = True
                    pq.put((c, v))
        return cost

in_file = sys.argv[1]

df = pd.read_csv(in_file, names=["from", "to", "weight"])
df = df[df.groupby('to').to.transform(len) > 1]
model = AdjList()
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(f"N={model.num_nodes()}")
print(f"M={model.num_edges()}")

#algos
print(f"Degree Distribution={model.degree_distribution()}")
print(f"Global CC={model.clustering_coefficient()}")
print(f"APL={model.average_path_length()}")