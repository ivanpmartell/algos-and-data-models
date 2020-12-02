import sys
import pandas as pd
from queue import PriorityQueue

class EdgeList:
    edges: list
    n: int
    m: int
    def __init__(self):
        self.edges = []
        self.n = 0
        self.m = 0

    def add(self, nodeFrom, nodeTo, weight):
        nF = nodeFrom
        nT = nodeTo
        if(self.count_node(nF)):
            self.n += 1
        if(self.count_node(nT)):
            self.n += 1
        self.edges.append((nF,nT,float(weight)))
        self.m += 1

    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge[0] == node:
                neighbors.append((edge[1],edge[2]))
        return neighbors
    
    def get_nodes(self):
        nodes = set()
        for f, t, _ in self.edges:
            nodes.add(f)
            nodes.add(t)
        return nodes

    def count_node(self, node):
        for f, t, w in self.edges:
            if node == f:
                return False
            if node == t:
                return False
        return True
    
    def num_nodes(self):
        #assert self.n == len(self.adj)
        return self.n

    def num_edges(self):
        return self.m
    
    def degree_distribution(self):
        dd = dict()
        for node in self.get_nodes():
            try:
                dd[len(self.get_neighbors(node))] += 1
            except:
                dd[len(self.get_neighbors(node))] = 1
        return dd

    def clustering_coefficient(self):
        triangles = 0
        triads = 0
        self.sort_list()
        for node in sorted(self.get_nodes()):
            levels = [0,0,0,0]
            levels[0] += 1
            neighbors = self.get_neighbors(node)
            for idx, v_e in enumerate(neighbors):
                levels[1] += 1
                v, _ = v_e
                if node < v:
                    v_neighbors = self.get_neighbors(v)
                    for w, _ in v_neighbors:
                        levels[2] += 1
                        if v < w:
                            connections = 0
                            for i in range(idx+1, len(neighbors)):
                                levels[3] += 1
                                connections += 1
                                if neighbors[i][0] == w:
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
    
    def sort_list(self):
        self.edges = sorted(self.edges)

    def average_path_length(self):
        costs = 0
        for node in self.get_nodes():
            costs += self.BFS(node)
        apl = costs/(self.n*(self.n-1))
        return apl
    
    def BFS(self, source):
        visited = {}
        for n in self.get_nodes():
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

df = pd.read_csv(in_file, names=["from", "to", "weight"], skiprows=1)
#df = df[df.groupby('to').to.transform(len) > 1]
model = EdgeList()
for idx, row in df.iterrows():
    model.add(row["from"], row["to"], row["weight"])
print(f"N={model.num_nodes()}")
print(f"M={model.num_edges()}")

#algos
print(f"Degree Distribution={model.degree_distribution()}")
print(f"Global CC={model.clustering_coefficient()}")
print(f"APL={model.average_path_length()}")