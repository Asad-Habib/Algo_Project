import networkx as nx
import random
import time
import matplotlib.pyplot as plt


# Python implementation of Dinic's Algorithm
class Edge_Dinic:
    def __init__(self, v, flow, C, rev):
        self.v = v
        self.flow = flow
        self.C = C
        self.rev = rev
 
# Residual Graph
class Graph_Dinic:
    def __init__(self, V):
        self.adj = [[] for i in range(V)]
        self.V = V
        self.level = [0 for i in range(V)]
 
    # add edge to the graph
    def addEdge(self, u, v, C):
 
        # Forward edge : 0 flow and C capacity
        a = Edge_Dinic(v, 0, C, len(self.adj[v]))
 
        # Back edge : 0 flow and 0 capacity
        b = Edge_Dinic(u, 0, 0, len(self.adj[u]))
        self.adj[u].append(a)
        self.adj[v].append(b)
 
    # Finds if more flow can be sent from s to t
    # Also assigns levels to nodes
    def BFS(self, s, t):
        for i in range(self.V):
            self.level[i] = -1
 
        # Level of source vertex
        self.level[s] = 0
 
        # Create a queue, enqueue source vertex
        # and mark source vertex as visited here
        # level[] array works as visited array also
        q = []
        q.append(s)
        while q:
            u = q.pop(0)
            for i in range(len(self.adj[u])):
                e = self.adj[u][i]
                if self.level[e.v] < 0 and e.flow < e.C:
 
                    # Level of current vertex is
                    # level of parent + 1
                    self.level[e.v] = self.level[u]+1
                    q.append(e.v)
 
        # If we can not reach to the sink we
        # return False else True
        return False if self.level[t] < 0 else True
 
# A DFS based function to send flow after BFS has
# figured out that there is a possible flow and
# constructed levels. This functions called multiple
# times for a single call of BFS.
# flow : Current flow send by parent function call
# start[] : To keep track of next edge to be explored
#           start[i] stores count of edges explored
#           from i
# u : Current vertex
# t : Sink
    def sendFlow(self, u, flow, t, start):
        # Sink reached
        if u == t:
            return flow
 
        # Traverse all adjacent edges one -by -one
        while start[u] < len(self.adj[u]):
 
            # Pick next edge from adjacency list of u
            e = self.adj[u][start[u]]
            if self.level[e.v] == self.level[u]+1 and e.flow < e.C:
 
                # find minimum flow from u to t
                curr_flow = min(flow, e.C-e.flow)
                temp_flow = self.sendFlow(e.v, curr_flow, t, start)
 
                # flow is greater than zero
                if temp_flow and temp_flow > 0:
 
                    # add flow to current edge
                    e.flow += temp_flow
 
                    # subtract flow from reverse edge
                    # of current edge
                    self.adj[e.v][e.rev].flow -= temp_flow
                    return temp_flow
            start[u] += 1
 
    # Returns maximum flow in graph
    def DinicMaxflow(self, s, t):
 
        # Corner case
        if s == t:
            return -1
 
        # Initialize result
        total = 0
 
        # Augument the flow while there is path
        # from source to sink
        while self.BFS(s, t) == True:
 
            # store how many edges are visited
            # from V { 0 to V }
            start = [0 for i in range(self.V+1)]
            while True:
                flow = self.sendFlow(s, float('inf'), t, start)
                if not flow:
                    break
 
                # Add path flow to overall flow
                total += flow
 
        # return maximum flow
        return total
 
class Edge_PushRelabel: 
    
    def __init__(self, flow, capacity, u, v):
        self.flow = flow
        self.capacity = capacity
        self.u = u
        self.v = v

# Represent a Vertex 
class Vertex_PushRelabel:
  
    def __init__(self, h, e_flow):
        self.h = h
        self.e_flow = e_flow

# To represent a flow network 
class Graph_PushRelabel:
    
    # int V;    # No. of vertices 
    # vector<Vertex> ver; 
    # vector<Edge> edge; 
    def __init__(self, V):
        
        self.V = V; 
        self.edge = []
        self.ver = []
        # all vertices are initialized with 0 height 
        # and 0 excess flow 
        for i in range(V):
            self.ver.append(Vertex_PushRelabel(0, 0))
    
    def addEdge(self, u, v, capacity):
        # flow is initialized with 0 for all edge 
        self.edge.append(Edge_PushRelabel(0, capacity, u, v))


    def preflow(self, s):
        
        # Making h of source Vertex equal to no. of vertices 
        # Height of other vertices is 0. 
        self.ver[s].h = len(self.ver); 

        for i in range(len(self.edge)): 
            
            # If current edge goes from source 
            if (self.edge[i].u == s):
                # Flow is equal to capacity 
                self.edge[i].flow = self.edge[i].capacity

                # Initialize excess flow for adjacent v 
                self.ver[self.edge[i].v].e_flow += self.edge[i].flow

                # Add an edge from v to s in residual graph with 
                # capacity equal to 0 
                self.edge.append(Edge_PushRelabel(-self.edge[i].flow, 0, self.edge[i].v, s))
                

    # returns index of overflowing Vertex 
    def overFlowVertex(self):
        
        for i in range(1, len(self.ver)-1): 
            
            if(self.ver[i].e_flow > 0):
                return i

        # -1 if no overflowing Vertex 
        return -1
    

    # Update reverse flow for flow added on ith Edge 
    def updateReverseEdgeFlow(self, i, flow):
        
        u = self.edge[i].v
        v = self.edge[i].u 

        for j in range(0, len(self.edge)): 
            if (self.edge[j].v == v and self.edge[j].u == u):
                self.edge[j].flow -= flow
                return

        # adding reverse Edge in residual graph 
        e = Edge_PushRelabel(0, flow, u, v)
        self.edge.append(e)
        

    # To push flow from overflowing vertex u 
    def push(self, u): 
        
        # Traverse through all edges to find an adjacent (of u) 
        # to which flow can be pushed 
        for i in range(0, len(self.edge)): 
            
            # Checks u of current edge is same as given 
            # overflowing vertex 
            if (self.edge[i].u == u):
                # if flow is equal to capacity then no push 
                # is possible 
                if (self.edge[i].flow == self.edge[i].capacity):
                    continue; 

                # Push is only possible if height of adjacent 
                # is smaller than height of overflowing vertex 
                if (self.ver[u].h > self.ver[self.edge[i].v].h):
                    
                    # Flow to be pushed is equal to minimum of 
                    # remaining flow on edge and excess flow. 
                    flow = min(self.edge[i].capacity - self.edge[i].flow, self.ver[u].e_flow)

                    # Reduce excess flow for overflowing vertex 
                    self.ver[u].e_flow -= flow; 

                    # Increase excess flow for adjacent 
                    self.ver[self.edge[i].v].e_flow += flow; 

                    # Add residual flow (With capacity 0 and negative 
                    # flow) 
                    self.edge[i].flow += flow; 

                    self.updateReverseEdgeFlow(i, flow); 

                    return True; 

        return False;  
    
    
    # function to relabel vertex u 
    def relabel(self, u):
        # Initialize minimum height of an adjacent 
        mh = 2100000

        # Find the adjacent with minimum height 
        for i in range(len(self.edge)):  
            if (self.edge[i].u == u):
                
                # if flow is equal to capacity then no 
                # relabeling 
                if (self.edge[i].flow == self.edge[i].capacity):
                    continue; 

                # Update minimum height 
                if (self.ver[self.edge[i].v].h < mh):
                    mh = self.ver[self.edge[i].v].h; 

                    # updating height of u 
                    self.ver[u].h = mh + 1; 

    
    # main function for printing maximum flow of graph 
    def getMaxFlow(self, s, t):
        
        self.preflow(s); 

        # loop until none of the Vertex is in overflow 
        while (self.overFlowVertex() != -1):
            
            u = self.overFlowVertex(); 
            if (self.push(u) == False):
                self.relabel(u); 

        # ver.back() returns last Vertex, whose 
        # e_flow will be final maximum flow 
        return self.ver[len(self.ver)-1].e_flow
    


def read_dimacs(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_vertices = 0
    edges = []

    for line in lines:
        tokens = line.strip().split()
        if tokens[0] == 'p':
            num_vertices = int(tokens[2])
        elif tokens[0] == 'a':
            u, v, capacity = map(int, tokens[1:])
            edges.append((u - 1, v - 1, capacity))  # Convert to 0-indexed vertices

    graph = Graph_Dinic(num_vertices)
    for u, v, capacity in edges:
        graph.add_edge(u, v, capacity)

    file_name = file_path.split('/')[-1]  # Extract file name
    parts = file_name.split('_')
    num_vertices = int(parts[1])
    num_edges = int(parts[3])
    max_capacity = int(parts[5])
    print(f"Nodes: {num_vertices}, Edges: {num_edges}, Max Capacity: {max_capacity}")

    return graph


def generate_random_graph(size, density = 1.0):
    # Generate a random graph using networkx
    G = nx.dense_gnm_random_graph(size, size * density)
    # Convert networkx graph to the format required by Dinic's Algorithm
    graph_dinic = Graph_Dinic(size)
    graph_pushR = Graph_PushRelabel(size)
    for u, v in G.edges():

        capacity = random.randint(size/10, size)  # Random capacity for each edge

        graph_dinic.addEdge(u, v, capacity)
        graph_pushR.addEdge(u, v, capacity)
    
    return graph_dinic, graph_pushR

def run_experiment(sizes):
    times_1 = []
    times_2 = []
    for size in sizes:
        g_1, g_2= generate_random_graph(size) 
        print("Graph Size: ", size) 

        start_time = time.time()
        max_flow_1 = g_1.DinicMaxflow(0, size - 1)  # Assuming the sink is the last vertex
        end_time = time.time()
        elapsed_time = end_time - start_time
        times_1.append(elapsed_time)
        
        print(f"Graph DINIC's Time: {elapsed_time}")

        
        start_time = time.time()
        max_flow_2 = g_2.getMaxFlow(0, size-1)  # Assuming the sink is the last vertex
        end_time = time.time()
        elapsed_time = end_time - start_time
        times_2.append(elapsed_time)

        print(f"Graph PUSH-RELABEL's Time: {elapsed_time}")

        try:
            assert max_flow_1 == max_flow_2
        except:
            print("Max flow not equal")
            print(f"Max flow Dinic: {max_flow_1}")
            print(f"Max flow PushRelabel: {max_flow_2}")
            

        # print(f"Graph size: {size}, Max flow: {max_flow_1}, Time taken: {elapsed_time} seconds")
    return times_1, times_2

def plot_results(sizes, times_1, times_2):
    plt.plot(sizes, times_1, label='Dinic\'s Algorithm Performance', marker='o')
    plt.plot(sizes, times_2, label='Push-Relabel\'s Algorithm Performance', marker='x')
    plt.title('Algorithm Performance')
    plt.xlabel('Graph Size')
    plt.ylabel('Time (seconds)')
    plt.grid(True)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    sizes = []  # Example sizes, adjust as needed
    for i in range(100, 2001, 100):
        sizes.append(i)
    times_1, times_2 = run_experiment(sizes)
    plot_results(sizes, times_1, times_2)



 
# This code is contributed by rupasriachanta421.
#https://www.geeksforgeeks.org/dinics-algorithm-maximum-flow/