import networkx as nx
import random
import time
import matplotlib.pyplot as plt
# Linear Programming for Max Flow
class Vertex_LP:
    def __init__(self, h=0, e_flow=0):
        self.h = h
        self.e_flow = e_flow

class Edge_LP:
    def __init__(self, v, capacity, flow=0, rev=None):
        self.v = v
        self.capacity = capacity
        self.flow = flow
        self.rev = rev  # Reverse edge reference

class maxFlow_LP:
    def __init__(self, V):
        self.V = V
        self.adj = [[] for _ in range(V)]

    def add_edge(self, u, v, capacity):
        # Add forward edge: u -> v
        forward_edge = Edge_LP(v, capacity, 0, len(self.adj[v]))
        # Add reverse edge: v -> u
        reverse_edge = Edge_LP(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(forward_edge)
        self.adj[v].append(reverse_edge)

    def _bfs(self, source, sink):
        queue = [source]
        levels = [-1] * self.V
        levels[source] = 0
        while queue:
            u = queue.pop(0)
            for edge in self.adj[u]:
                if levels[edge.v] == -1 and edge.flow < edge.capacity:
                    levels[edge.v] = levels[u] + 1
                    queue.append(edge.v)
                    if edge.v == sink:
                        return levels
        return levels

    def _dfs(self, u, flow, sink, levels):
        if u == sink:
            return flow
        for edge in self.adj[u]:
            if levels[edge.v] == levels[u] + 1 and edge.flow < edge.capacity:
                cur_flow = min(flow, edge.capacity - edge.flow)
                pushed = self._dfs(edge.v, cur_flow, sink, levels)
                if pushed > 0:
                    edge.flow += pushed
                    # Update reverse flow using the 'rev' attribute to find the reverse edge
                    self.adj[edge.v][edge.rev].flow -= pushed
                    return pushed
        return 0

    def calculate_max_flow(self, source, sink):
        max_flow = 0
        while True:
            levels = self._bfs(source, sink)
            if levels[sink] == -1:
                break
            flow = self._dfs(source, float('inf'), sink, levels)
            while flow > 0:
                max_flow += flow
                flow = self._dfs(source, float('inf'), sink, levels)
        return max_flow