### example ###

from MaxFlow import *
import numpy as np
import random
import time
import networkx as nx
import matplotlib.pyplot as plt




def read_dimacs(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    num_vertices = 0
    num_edges = 0
    edges = []

    for line in lines:
        tokens = line.strip().split()
        if tokens[0] == 'p':
            num_vertices = int(tokens[2])
            num_edges = int(tokens[3])
        elif tokens[0] == 'a':
            u, v, capacity = map(int, tokens[1:])
            edges.append((u - 1, v - 1, capacity))  # Convert to 0-indexed vertices

    #convert edges to a adjacency matrix using numpy
    adj_matrix = np.zeros((num_vertices, num_vertices))
    for edge in edges:
        u, v, capacity = edge
        adj_matrix[u][v] = capacity
    

    graph_dicnic = Graph(adj_matrix)
    graph_pushR = Graph(adj_matrix)
    
    return graph_dicnic, graph_pushR



def run_experiment(sizes):
    times_1 = []
    times_2 = []
    for size in sizes:
        g_1, g_2 = read_dimacs(f"acyclic/s_{size}.max") # if reading acyclic graphs
        #g_1, g_2 = read_dimacs(f"random/r_{size}.max") # if reading random graphs
        print("Graph Size: ", size) 

        start_time = time.time()
        max_flow_1 = g_1.Dinic() # Assuming the sink is the last vertex
        end_time = time.time()
        elapsed_time = end_time - start_time
        times_1.append(elapsed_time)
        
        print(f"Graph DINIC's Time: {elapsed_time}")

        
        start_time = time.time()
        max_flow_2 = g_2.PushRelable()  # Assuming the sink is the last vertex
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
    sizes = [100]  # Example sizes, adjust as needed
    for i in range(100, 1001, 100):
        sizes.append(i)
    times_1, times_2 = run_experiment(sizes)
    plot_results(sizes, times_1, times_2)


# EdmondKarp_graph = Graph(valid_data)
# EdmondKarp_graph.EdmondKarp()
