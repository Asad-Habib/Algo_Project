#!/bin/bash

# Directory to store generated graphs
output_dir="generated_graphs"
mkdir -p "$output_dir"

# Run the graph generating executable 100 times with varying numbers of nodes
for (( i=100; i<=100; i+=100 )); do
    # Generate DIMACS file name
    max_capacity=$((i * (i - 1) / 2))
    file_name="n_${i}_e_${i}_c_${max_capacity}.txt"
    file_path="$output_dir/$file_name"

    echo "Generating graph with $i nodes..."

    ./ra-max
    echo "y"
    echo "n_${i}_e_${i}_c_${max_capacity}.txt"  # Output file name
    echo "$i"  # Number of nodes
    echo "$i"  # Number of edges
    echo "$max_capacity"  # Maximum capacity
    echo  # Press enter to continue
    echo  # Press enter to continue


done

echo "Graph generation completed."
