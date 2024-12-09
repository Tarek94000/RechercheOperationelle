def display_matrix(matrix, label):
    print(f"{label}:")
    for row in matrix:
        print(" ".join(map(str, row)))

def save_flow_to_file(graph, filename):
    with open(filename, 'w') as file:
        for row in graph.flow:
            file.write(" ".join(map(str, row)) + "\n")
